import torch
import numpy as np

def img_transform(img):
    # same transformation that the NIST example applies, torchvision ones should be the same
    # but didn't work on round 1
    h, w, c = img.shape
    #resize to 224x224
    dx = int((w - 224) / 2)
    dy = int((w - 224) / 2)
    img = img[dy:dy+224, dx:dx+224, :]

    #cxhxw + normalization
    img = np.transpose(img, (2, 0, 1))
    img = np.expand_dims(img, 0)
    img = img - np.min(img)
    img = img / np.max(img)

    return torch.FloatTensor(img)
