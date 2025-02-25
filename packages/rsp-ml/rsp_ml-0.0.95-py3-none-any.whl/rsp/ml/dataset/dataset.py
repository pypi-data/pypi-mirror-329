from torch.utils.data import Dataset
from pathlib import Path
from platformdirs import user_cache_dir
from tqdm import tqdm
from glob import glob
from threading import Thread
from typing import List
from huggingface_hub import hf_hub_download, list_repo_files
import numpy as np
import os
import json
import pkg_resources
import urllib
import tarfile
import cv2 as cv
import csv
import torch
import rsp.ml.multi_transforms.multi_transforms as multi_transforms
import time
import pandas as pd
try:
    import rsp.common.console as console
except Exception as e:
    print(e)

#__example__ from rsp.ml.dataset import ReplaceBackgroundRGB
#__example__ from rsp.ml.dataset import TUCRID
#__example__
#__example__ backgrounds = TUCRID.load_backgrounds()
class ReplaceBackground(multi_transforms.MultiTransform):
    """
    Transformation for background replacement based on HSV values. ReplaceBackground is an abstract class. Please inherit!
    """
    def __init__(self):
        """
        Initializes a new instance.
        """
        super().__init__()

    def __call__(self, inputs):
        """
        Applies the transformation to the input data.
        """
        raise Exception('This is an abstract class. Please override the __call__ method.')

    def hsv_filter(self, img, hmin, hmax, smin, smax, vmin, vmax, inverted):
        """
        Filters the input image based on HSV values.

        Parameters
        ----------
        img : np.array
            Input image
        hmin : int
            Minimum hue value
        hmax : int
            Maximum hue value
        smin : int
            Minimum saturation value
        smax : int
            Maximum saturation value
        vmin : int
            Minimum value value
        vmax : int
            Maximum value value
        inverted : bool
            Invert the mask
        """
        hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
        lower = (hmin, smin, vmin)
        upper = (hmax, smax, vmax)
        mask = cv.inRange(hsv, lower, upper)
        if inverted:
            mask = 255 - mask
        return mask

    def change_background(self, img, bg, mask):
        """
        Changes the background of the input image.

        Parameters
        ----------
        img : np.array
            Input image
        bg : np.array
            Background image
        mask : np.array
            Mask
        """
        w, h = img.shape[1], img.shape[0]
        bg_w, bg_h = bg.shape[1], bg.shape[0]
        scale = np.min([w / bg_w, h / bg_h])
        new_w, new_h = int(np.round(scale * bg_w)), int(np.round(scale * bg_h))

        bg = cv.resize(bg, (new_w, new_h))

        img[mask > 0] = bg[mask > 0]

        return img

class ReplaceBackgroundRGB(ReplaceBackground):
    """
    Transformation for background replacement based on HSV values. ReplaceBackgroundRGB is a concrete class for RGB images.
    """
    def __init__(
            self,
            backgrounds:List[np.array],
            hsv_filter:List[tuple[int, int, int, int, int, int]] = [(69, 87, 139, 255, 52, 255)],
            p:float = 1.
        ):
        """
        Initializes a new instance.

        Parameters
        ----------
        backgrounds : List[np.array]
            List of background images
        hsv_filter : List[tuple[int, int, int, int, int, int]]
            List of HSV filters
        p : float, default = 1.
            Probability of applying the transformation
        """
        super().__init__()
        self.backgrounds = backgrounds
        self.__hsv_filter__ = hsv_filter
        self.p = p

        self.__toTensor__ = multi_transforms.ToTensor()
        self.__toPILImage__ = multi_transforms.ToPILImage()
        self.__toCVImage__ = multi_transforms.ToCVImage()

    def __call__(self, inputs):
        self.__get_size__(inputs)
        self.__reset__()

        if self.__replace_background__:
            is_tensor = isinstance(inputs[0], torch.Tensor)
            if not is_tensor:
                inputs = self.__toTensor__(inputs)

            results = []
            for i, input in enumerate(self.__toCVImage__(inputs)):
                img = np.asarray(input * 255, dtype=np.uint8)

                mask = np.ones((input.shape[0], input.shape[1]))
                for f in self.__hsv_filter__:
                    hsv_mask = self.hsv_filter(img.copy(), f[0], f[1], f[2], f[3], f[4], f[5], inverted = False)
                    hsv_mask = hsv_mask / 255

                    mask = cv.bitwise_and(mask, hsv_mask)

                mask = np.asarray(mask, dtype=np.uint8)

                bg = np.asarray(self.__background__ / 255, dtype=np.float32)

                result = self.change_background(input, bg, mask)

                results.append(result)

            results = self.__toTensor__(results)

            if not is_tensor:
                results = self.__toPILImage__(results)
        else:
            results = inputs
        return results

    def __reset__(self):
        self.__replace_background__ = np.random.random() < self.p
        idx = np.random.randint(0, len(self.backgrounds))
        self.__background__ = self.backgrounds[idx]

class ReplaceBackgroundRGBD(ReplaceBackground):
    """
    Transformation for background replacement based on HSV values. ReplaceBackgroundRGBD is a concrete class for RGBD images.

    Parameters
    ----------
    backgrounds : List[np.array]
        List of background images
    hsv_filter : List[tuple[int, int, int, int, int, int]]
        List of HSV filters
    p : float, default = 1.
        Probability of applying the transformation
    rotate : float, default = 5
        Maximum rotation angle
    max_scale : float, default = 2
        Maximum scaling factor
    """
    def __init__(
            self,
            backgrounds:List[np.array],
            hsv_filter:List[tuple[int, int, int, int, int, int]] = [(69, 87, 139, 255, 52, 255)],
            p:float = 1.,
            rotate:float = 5,
            max_scale:float = 2):
        super().__init__()
        self.backgrounds = backgrounds
        self.__hsv_filter__ = hsv_filter
        self.p = p

        self.__toTensor__ = multi_transforms.ToTensor()
        self.__toPILImage__ = multi_transforms.ToPILImage()
        self.__toCVImage__ = multi_transforms.ToCVImage()

        self.transforms = multi_transforms.Compose([
            multi_transforms.Rotate(rotate),
            multi_transforms.RandomCrop(max_scale = max_scale),
            multi_transforms.RandomHorizontalFlip(),
            multi_transforms.RandomVerticalFlip()
        ])

    def __call__(self, inputs):
        self.__get_size__(inputs)
        self.__reset__()

        if self.__replace_background__:
            is_tensor = isinstance(inputs[0], torch.Tensor)
            if not is_tensor:
                inputs = self.__toTensor__(inputs)

            is_color_image = inputs[0].shape[0] == 3
            is_depth_image = inputs[0].shape[0] == 4

            if is_color_image:
                self.__masks__ = []

            results = []
            for i, input in enumerate(self.__toCVImage__(inputs)):
                img = np.asarray(input * 255, dtype=np.uint8)
                img_rgb = img[:, :, 0:3]

                mask = np.ones((input.shape[0], input.shape[1]))
                for f in self.__hsv_filter__:
                    hsv_mask = self.hsv_filter(img_rgb.copy(), f[0], f[1], f[2], f[3], f[4], f[5], inverted = False)
                    hsv_mask = hsv_mask / 255

                    mask = cv.bitwise_and(mask, hsv_mask)

                mask = np.asarray(mask, dtype=np.uint8)

                bg_color = np.asarray(self.__background__[0] / 255, dtype=np.float32)
                bg = bg_color
                
                if is_depth_image:
                    bg_depth = np.asarray(self.__background__[1] / 255, dtype=np.float32)
                    bg_depth = np.expand_dims(bg_depth, 2)
                    bg = np.concatenate([bg_color, bg_depth], axis = 2)

                result = self.change_background(input, bg, mask)

                results.append(result)

            results = self.__toTensor__(results)

            if not is_tensor:
                results = self.__toPILImage__(results)
        else:
            results = inputs
        return results

    def __reset__(self):
        self.__replace_background__ = np.random.random() < self.p
        idx = np.random.randint(0, len(self.backgrounds))
        self.__background__ = self.backgrounds[idx]

#__example__ from rsp.ml.dataset import TUCRID
#__example__ from rsp.ml.dataset import ReplaceBackgroundRGBD
#__example__ import rsp.ml.multi_transforms as multi_transforms
#__example__ import cv2 as cv
#__example__
#__example__ backgrounds = TUCRID.load_backgrounds_color()
#__example__ transforms = multi_transforms.Compose([
#__example__     ReplaceBackgroundRGBD(backgrounds),
#__example__     multi_transforms.Stack()
#__example__ ])
#__example__ 
#__example__ ds = TUCRID('train', transforms=transforms)
#__example__ 
#__example__ for X, T in ds:
#__example__   for x in X.permute(0, 2, 3, 1):
#__example__     img_color = x[:, :, :3].numpy()
#__example__     img_depth = x[:, :, 3].numpy()
#__example__ 
#__example__     cv.imshow('color', img_color)
#__example__     cv.imshow('depth', img_depth)
#__example__ 
#__example__     cv.waitKey(30)
class TUCRID(Dataset):
    """
    Dataset class for the Robot Interaction Dataset by University of Technology Chemnitz (TUCRID).
    """
    REPO_ID = 'SchulzR97/TUCRID'
    CACHE_DIRECTORY = Path(user_cache_dir('rsp-ml', 'Robert Schulz')).joinpath('datasets', 'TUCRID')
    COLOR_DIRECTORY = CACHE_DIRECTORY.joinpath('color')
    DEPTH_DIRECTORY = CACHE_DIRECTORY.joinpath('depth')
    BACKGROUND_DIRECTORY = CACHE_DIRECTORY.joinpath('background')
    PHASES = ['train', 'val']

    def __init__(
            self,
            phase:str,
            load_depth_data:bool = True,
            sequence_length:int = 30,
            num_classes:int = 10,
            transforms:multi_transforms.Compose = multi_transforms.Compose([]),
            cache_dir:str = None
    ):
        """
        Initializes a new instance.

        Parameters
        ----------
        phase : str
            Dataset phase [train|val]
        load_depth_data : bool, default = True
            Load depth data
        sequence_length : int, default = 30
            Length of the sequences
        num_classes : int, default = 10
            Number of classes
        transforms : rsp.ml.multi_transforms.Compose = default = rsp.ml.multi_transforms.Compose([])
            Transformations, that will be applied to each input sequence. See documentation of `rsp.ml.multi_transforms` for more details.
        """
        assert phase in TUCRID.PHASES, f'Phase "{phase}" not in {TUCRID.PHASES}'

        if cache_dir is not None:
            TUCRID.CACHE_DIRECTORY = Path(cache_dir)

        self.phase = phase
        self.load_depth_data = load_depth_data
        self.sequence_length = sequence_length
        self.num_classes = num_classes
        self.transforms = transforms

        self.__download__()
        self.__load__()
        pass

    def __len__(self):
        return len(self.sequences)
    
    def __getitem__(self, idx):
        sequence = self.sequences[idx]
        id = sequence['id']
        action = sequence['action']
        link = sequence['link']

        color_files = sorted(glob(f'{TUCRID.COLOR_DIRECTORY}/{link}/*.jpg'))
        assert len(color_files) >= self.sequence_length, f'Not enough frames for {id}.'

        if len(color_files) > self.sequence_length:
            start_idx = np.random.randint(0, len(color_files) - self.sequence_length)
            end_idx = start_idx + self.sequence_length
        else:
            start_idx = 0
            end_idx = start_idx + self.sequence_length

        color_images = []
        depth_images = []
        for color_file in color_files[start_idx:end_idx]:

            color_file = Path(color_file)

            img = cv.imread(str(color_file))
            color_images.append(img)

            if self.load_depth_data:
                depth_file = TUCRID.DEPTH_DIRECTORY.joinpath(f'{link}/{color_file.name}')
                img = cv.imread(str(depth_file), cv.IMREAD_UNCHANGED)
                depth_images.append(img)
        
        X = torch.tensor(np.array(color_images), dtype=torch.float32) / 255
        if self.load_depth_data:
            X_depth = torch.tensor(np.array(depth_images), dtype=torch.float32).unsqueeze(3) / 255
            X = torch.cat([X, X_depth], dim=3)
        X = X.permute(0, 3, 1, 2)
        T = torch.zeros((self.num_classes), dtype=torch.float32)
        T[action] = 1

        self.transforms.__reset__()
        X = self.transforms(X)
        
        return X, T

    def __download__(self):                        
        TUCRID.CACHE_DIRECTORY.mkdir(exist_ok=True, parents=True)

        TUCRID.__download_metadata__()

        TUCRID.__download_backgrounds__()

        TUCRID.__download_sequences__(self.load_depth_data)

    def __download_file__(filename, retries = 10):
        attempts = 0
        while True:
            try:
                hf_hub_download(
                    repo_id=TUCRID.REPO_ID,
                    repo_type='dataset',
                    local_dir=TUCRID.CACHE_DIRECTORY,
                    filename=str(filename)
                )
                break
            except Exception as e:
                if attempts < retries:
                    attempts += 1
                else:
                    raise e

    def __download_metadata__():
        for phase in TUCRID.PHASES:
            if not f'{phase}.json' in os.listdir(TUCRID.CACHE_DIRECTORY):
                TUCRID.__download_file__(f'{phase}.json')

    def __download_backgrounds__():
        # color
        background_color_dir = TUCRID.BACKGROUND_DIRECTORY.joinpath('color')
        if not background_color_dir.exists() or len(os.listdir(background_color_dir)) == 0:
            TUCRID.__download_file__('background/color.tar.gz')
            background_color_tarfile = TUCRID.BACKGROUND_DIRECTORY.joinpath('color.tar.gz')
            with tarfile.open(background_color_tarfile, 'r:gz') as tar:
                tar.extractall(background_color_dir)
            os.remove(background_color_tarfile)

        # depth
        background_depth_dir = TUCRID.BACKGROUND_DIRECTORY.joinpath('depth')
        if not background_depth_dir.exists() or len(os.listdir(background_depth_dir)) == 0:
            TUCRID.__download_file__('background/depth.tar.gz')
            background_depth_tarfile = TUCRID.BACKGROUND_DIRECTORY.joinpath('depth.tar.gz')
            with tarfile.open(background_depth_tarfile, 'r:gz') as tar:
                tar.extractall(background_depth_dir)
            os.remove(background_depth_tarfile)

    def __download_sequences__(load_depth_data):
        repo_files = [Path(file) for file in list_repo_files(TUCRID.REPO_ID, repo_type='dataset')]
        color_files = [file for file in repo_files if file.parent.name == 'color']

        prog = tqdm(color_files)
        for color_file in prog:
            prog.set_description(f'Downloading {color_file}')
            local_dir = TUCRID.COLOR_DIRECTORY.joinpath(color_file.name.replace('.tar.gz', ''))
            if local_dir.exists() and len(os.listdir(local_dir)) > 0:
                continue
            TUCRID.__download_file__(color_file)
            tar_color = TUCRID.COLOR_DIRECTORY.joinpath(color_file.name)
            with tarfile.open(tar_color, 'r:gz') as tar:
                tar.extractall(local_dir)
            os.remove(tar_color)

        if load_depth_data:
            depth_files = [file for file in repo_files if file.parent.name == 'depth']
            prog = tqdm(depth_files)
            for depth_file in prog:
                prog.set_description(f'Downloading {depth_file}')
                local_dir = TUCRID.DEPTH_DIRECTORY.joinpath(depth_file.name.replace('.tar.gz', ''))
                if local_dir.exists() and len(os.listdir(local_dir)) > 0:
                    continue
                TUCRID.__download_file__(depth_file)
                tar_depth = TUCRID.DEPTH_DIRECTORY.joinpath(depth_file.name)
                with tarfile.open(tar_depth, 'r:gz') as tar:
                    tar.extractall(local_dir)
                os.remove(tar_depth)

    def __load__(self):
        with open(TUCRID.CACHE_DIRECTORY.joinpath(f'{self.phase}.json'), 'r') as f:
            self.sequences = json.load(f)

    def load_backgrounds(load_depth_data:bool = True):
        """
        Loads the background images.

        Parameters
        ----------
        load_depth_data : bool, default = True
            If set to `True`, the depth images will be loaded as well.
        """
        bg_color_dir = TUCRID.BACKGROUND_DIRECTORY.joinpath('color')
        bg_depth_dir = TUCRID.BACKGROUND_DIRECTORY.joinpath('depth')

        if not bg_color_dir.exists() or len(os.listdir(bg_color_dir)) == 0:
            TUCRID.__download_backgrounds__()
        if load_depth_data and (not bg_depth_dir.exists() or len(os.listdir(bg_depth_dir)) == 0):
            TUCRID.__download_backgrounds__()

        bg_color_files = sorted(glob(f'{bg_color_dir}/*'))

        backgrounds = []
        for fname_color in bg_color_files:
            fname_color = Path(fname_color)
            bg_color = cv.imread(str(fname_color))

            if load_depth_data:
                fname_depth = TUCRID.BACKGROUND_DIRECTORY.joinpath('depth', fname_color.name.replace('_color', '_depth'))
                bg_depth = cv.imread(str(fname_depth), cv.IMREAD_UNCHANGED)
                backgrounds.append((bg_color, bg_depth))
            else:
                backgrounds.append(bg_color)
        return backgrounds

#__example__ from rsp.ml.dataset import Kinetics
#__example__ 
#__example__ ds = Kinetics(split='train', type=400)
#__example__
#__example__ for X, T in ds:
#__example__     print(X)
class Kinetics(Dataset):
    """
    Dataset class for the Kinetics dataset.
    """
    def __init__(
        self,
        split:str,
        type:int = 400,
        frame_size = (400, 400),
        transforms:multi_transforms.Compose = multi_transforms.Compose([]),
        cache_dir:str = None,
        num_threads:int = 0
    ):
        """
        Initializes a new instance.
        
        Parameters
        ----------
        split : str
            Dataset split [train|val]
        type : int, default = 400
            Type of the kineticts dataset. Currently only 400 is supported.
        frame_size : (int, int), default = (400, 400)
            Size of the frames. The frames will be resized to this size.
        transforms : rsp.ml.multi_transforms.Compose = default = rsp.ml.multi_transforms.Compose([])
            Transformations, that will be applied to each input sequence. See documentation of `rsp.ml.multi_transforms` for more details.
        cache_dir : str, default = None
            Directory to store the downloaded files. If set to `None`, the default cache directory will be used
        num_threads : int, default = 0
            Number of threads to use for downloading the files.
        """
        super().__init__()

        assert split in ['train', 'val'], f'{split} is not a valid split.'
        assert type in [400], f'{type} is not a valid type.'

        self.split = split
        self.type = type
        self.frame_size = frame_size
        self.sequence_length = 10
        self.transforms = transforms
        self.num_threads = num_threads

        if cache_dir is None:
            self.__cache_dir__ = Path(user_cache_dir("rsp-ml", "Robert Schulz")).joinpath('dataset', 'kinetics')
        else:
            self.__cache_dir__ = Path(cache_dir)
        self.__cache_dir__.mkdir(parents=True, exist_ok=True)

        self.__toTensor__ = multi_transforms.ToTensor()
        self.__stack__ = multi_transforms.Stack()

        self.__download__()
        self.__annotations__, self.action_labels = self.__load_annotations_labels__()
        self.__files__ = self.__list_files__()

    def __getitem__(self, index):
        youtube_id, fname = self.__files__[index]

        annotation = self.__annotations__[youtube_id]

        if annotation['time_end'] - annotation['time_start'] > self.sequence_length:
            start_idx = np.random.randint(annotation['time_start'], annotation['time_end']-self.sequence_length)
            end_idx = start_idx + self.sequence_length
        else:
            start_idx = annotation['time_start']
            end_idx = annotation['time_end']

        cap = cv.VideoCapture(fname)
        cap.set(cv.CAP_PROP_POS_FRAMES, start_idx)

        frames = []
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            frame = cv.resize(frame, self.frame_size)
            frames.append(frame)
            if len(frames) >= end_idx - start_idx:
                break
        frames = np.array(frames) / 255

        if len(frames) == 0:
            X = torch.zeros((self.sequence_length, 3, *self.frame_size), dtype=torch.float32)
            console.warning(f'No frames found for {youtube_id}.')
        else:
            X = torch.tensor(frames).permute(0, 3, 1, 2)
        T = torch.zeros((len(self.action_labels)))
        cls = self.action_labels.index(annotation['label'])
        T[cls] = 1

        return X, T

    def __len__(self):
        return len(self.__files__)
    
    def __get_labels__(self):
        labels = {}
        df = pd.DataFrame(self.__annotations__)
        for i, (key, _) in enumerate(df.groupby('label')):
            key = key.replace('"', '')
            labels[key] = i
        return labels

    def __download__(self):
        def get_fname_resource(resource_name):
            fname = pkg_resources.resource_filename('rsp', resource_name)
            return Path(fname)
        
        def download_file(link, fname, retries = 10):
            attempt = 0
            while attempt < retries:
                try:
                    urllib.request.urlretrieve(link, fname)
                    break
                except urllib.error.ContentTooShortError as e:
                    attempt += 1
                except Exception as e:
                    attempt += 1

        def unpack(src, dest, remove = True):
            with tarfile.open(src, "r:gz") as tar:
                tar.extractall(path=dest)
            if remove:
                os.remove(src)

        anno_link_file = get_fname_resource(f'ml/dataset/links/kinetics/annotations/k{self.type}_annotations.txt')
        with open(anno_link_file, 'r') as file:
            links = file.read().split('\n')
            cache_anno_dir = Path(self.__cache_dir__).joinpath('annotations')
            cache_anno_dir.mkdir(parents=True, exist_ok=True)
            for link in links:
                fname = link.split('/')[-1]
                fname = cache_anno_dir.joinpath(f'k{self.type}_{fname}')
                if fname.exists():
                    continue
                download_file(link, fname)

        path_link_files = [
            get_fname_resource(f'ml/dataset/links/kinetics/paths/k{self.type}_train_path.txt'),
            get_fname_resource(f'ml/dataset/links/kinetics/paths/k{self.type}_test_path.txt'),
            get_fname_resource(f'ml/dataset/links/kinetics/paths/k{self.type}_val_path.txt')
        ]

        cache_archives_dir = self.__cache_dir__.joinpath('archives')
        cache_archives_dir.mkdir(parents=True, exist_ok=True)

        cache_videos_dir = self.__cache_dir__.joinpath('videos')
        cache_videos_dir.mkdir(parents=True, exist_ok=True)

        threads = []

        prog1 = tqdm(path_link_files)
        for link_file in prog1:
            prog1.set_description(f'Downloading {link_file.stem}')

            with open(link_file, 'r') as file:
                links = file.read().split('\n')
            prog2 = tqdm(links)
            for link in prog2:
                prog2.set_description(link)

                def process_link(link):
                    split, fname = link.split('/')[-2:]

                    video_dir = cache_videos_dir.joinpath(split, 'k' + str(self.type) + '_' + fname.split(".")[0])
                    if video_dir.exists():
                        #continue
                        return

                    archive_file = cache_archives_dir.joinpath(split, f'k{self.type}_{fname}')
                    archive_file.parent.mkdir(parents=True, exist_ok=True)
                    if not archive_file.exists():
                        download_file(link, archive_file)

                    video_dir.mkdir(parents=True, exist_ok=True)
                    try:
                        unpack(archive_file, video_dir, remove=True)
                    except Exception as e:
                        video_dir.rmdir()
                        os.remove(archive_file)
                        download_file(link, archive_file)
                        unpack(archive_file, video_dir, remove=True)

                if self.num_threads == 0:
                    process_link(link)
                else:
                    thread = Thread(target=process_link, args=(link,))
                    while len(threads) >= self.num_threads:
                        threads = [t for t in threads if t.is_alive()]
                        time.sleep(0.1)
                    thread.start()
                    threads.append(thread)

    def __load_annotations_labels__(self):
        annotations_file = self.__cache_dir__.joinpath('annotations', f'k{self.type}_{self.split}.csv')
        annotations = {}
        labels = []
        with open(annotations_file, newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for i, row in enumerate(spamreader):
                if i == 0:
                    continue
                label, youtube_id, time_start, time_end, split, is_cc = row[0], row[1], int(row[2]), int(row[3]), row[4], int(row[5])
                label = label.replace('"', '')
                annotations[youtube_id] = {
                    'label': label,
                    #'youtube_id': youtube_id,
                    'time_start': time_start,
                    'time_end': time_end,
                    'split': split,
                    'is_cc': is_cc
                }
                if label not in labels:
                    labels.append(label)
        return annotations, sorted(labels)

    def __list_files__(self):
        videos_dir = self.__cache_dir__.joinpath('videos', self.split)
        links = glob(f'{videos_dir}/k{self.type}*/*.mp4')
        files = []#{}
        for link in links:
            youtube_id = Path(link).name[:-18]
            #files[youtube_id] = link
            files.append((youtube_id, link))
        return files

if __name__ == '__main__':
    k400 = Kinetics('train', num_threads=2, cache_dir='/Volumes/USB-Freigabe/KINETICS400')#cache_dir='/Volumes/ROBERT512GB/KINETICS400')

    for i, (X, T) in enumerate(k400):
        print(i)
        pass