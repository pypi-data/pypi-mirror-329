
import os
import torchvision.transforms as T
from torchvision.io import read_image, ImageReadMode
from PIL import Image
import numpy as np
import torch
import random

# ANCHOR: Data


def fix_seed(s=0):
    torch.manual_seed(s)
    torch.cuda.manual_seed_all(s)
    random.seed(s)
    np.random.seed(s)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False


def min_max_norm(u):
    if u.sum() == 0 or len(u) < 2:
        return u
    u -= u.min()
    u /= u.max()
    return u


def min_max_norm_matrix(u, axis=None):
    if type(u) is torch.Tensor:
        umin = u.min(dim=-1, keepdim=True).values.min(dim=-
                                                      2, keepdim=True).values
        u -= umin
        umax = u.max(dim=-1, keepdim=True).values.max(dim=-
                                                      2, keepdim=True).values
        u /= umax
        if torch.isnan(u).all():
            u = torch.ones_like(u)
    else:
        # narrays
        u -= u.min(axis=axis, keepdims=True)
        u /= u.max(axis=axis, keepdims=True)
        if np.isnan(u).all():
            u = np.ones_like(u)
    return torch.nan_to_num(u)


tensor_tran = T.ToTensor()


def read_image_to_tensor_from_path(img_path, mode=ImageReadMode.RGB) -> torch.Tensor:
    if img_path.endswith(".tif"):
        return tensor_tran(Image.open(img_path))
    else:
        # same as https://github.com/pytorch/vision/blob/bf01bab6125c5f1152e4f336b470399e52a8559d/torchvision/datasets/folder.py#L260
        # which is the default way of torchvision reading image
        return read_image(img_path, mode=mode).float() / 255.0


def get_tensor_from_flask_file_storage(task_ticket, image, datamodule):
    image_save_path = os.path.join(
        os.environ["COMPONENT_TMP_PATH"], f"predict_{task_ticket}_{image.filename}")
    os.makedirs(os.path.dirname(image_save_path), exist_ok=True)
    image.save(image_save_path)
    image_tensor = read_image_to_tensor_from_path(image_save_path)

    image_tensor = datamodule.no_aug_transform(image_tensor)[None, :, :, :]
    return image_tensor, image_save_path
