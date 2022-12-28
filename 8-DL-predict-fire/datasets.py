import torch
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
import torch.utils.data as data
import os
from PIL import Image
import numpy as np


_NUM_CLASSES = {
    'fire_prediction_DB': 2,
}


def default_loader(path):

    slide_data = np.load(path)
    # slide_data = np.transpose(slide_data, (2, 0, 1))
    # slide_data = slide_data[:, :, :13]
    slide_data = np.float32(slide_data)
    return slide_data


def default_flist_reader(flist):
    """
    flist format: impath label\nimpath label\n ...(same to caffe's filelist)
    """
    imlist = []
    with open(flist, 'r') as rf:
        for line in rf.readlines():
            impath, imlabel, imindex = line.strip().split()
            imlist.append((impath, int(imlabel), int(imindex)))
    return imlist


def rgb2gray(rgb):
    r, g, b = rgb[:,:,0], rgb[:,:,1], rgb[:,:,2]
    gray = 0.2989 * r + 0.5870 * g + 0.1140 * b
    return gray


class ImageFilelist(data.Dataset):
    def __init__(self, flist, transform=None, target_transform=None,
                 flist_reader=default_flist_reader, loader=default_loader):
        self.imlist = flist_reader(flist)
        self.transform = transform
        self.target_transform = target_transform
        self.loader = loader

    def __getitem__(self, index):
        impath, target, index = self.imlist[index]
        img = self.loader(impath)
        if self.transform is not None:
            img = self.transform(img)
        if self.target_transform is not None:
            target = self.target_transform(target)

        return img, target, index

    def __len__(self):
        return len(self.imlist)


def fire_prediction_DB(batch_size, train_list, val_list, train=True, val=True, **kwargs):

    num_workers = kwargs.setdefault('num_workers', 1)
    kwargs.pop('input_size', None)
    print("Building data loader with {} workers".format(num_workers))
    ds = []

    if train:
        train_loader = torch.utils.data.DataLoader(
            ImageFilelist(
                flist=train_list,
                transform=transforms.Compose([
                    # transforms.RandomResizedCrop(224),
                    # transforms.RandomHorizontalFlip(),
                    transforms.ToTensor(),
                    transforms.Normalize((0.00023, 0.074, 0.20, 0.17, 0.12, 0.77, 0.50, 0.41, 0.11, 0.58, 0.47, 0.15, 0.31, 0.26, 0.086), (0.015, 0.24, 0.26, 0.22, 0.14, 0.15, 0.23, 0.23, 0.14, 0.25, 0.28, 0.20, 0.24, 0.26, 0.25)),
                ])),
            batch_size=batch_size, shuffle=True, **kwargs)
        print("Training data size: {}".format(len(train_loader.dataset)))
        ds.append(train_loader)

    if val:
        test_loader = torch.utils.data.DataLoader(
            ImageFilelist(
                flist=val_list,
                transform=transforms.Compose([
                    # transforms.CenterCrop(224),
                    transforms.ToTensor(),
                    transforms.Normalize((0.00023, 0.074, 0.20, 0.17, 0.12, 0.77, 0.50, 0.41, 0.11, 0.58, 0.47, 0.15, 0.31, 0.26, 0.086), (0.015, 0.24, 0.26, 0.22, 0.14, 0.15, 0.23, 0.23, 0.14, 0.25, 0.28, 0.20, 0.24, 0.26, 0.25)),
                ])),
            batch_size=batch_size, shuffle=False, **kwargs)
        print("Testing data size: {}".format(len(test_loader.dataset)))
        ds.append(test_loader)
    ds = ds[0] if len(ds) == 1 else ds
    return ds

