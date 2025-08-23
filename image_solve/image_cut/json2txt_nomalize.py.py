import torch
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
import os
import numpy as np
from PIL import Image

class RoadCrackDataset(Dataset):
    def __init__(self, images_dir, masks_dir, transform=None):
        self.images_dir = images_dir
        self.masks_dir = masks_dir
        self.transform = transform
        self.image_filenames = [os.path.join(images_dir, f) for f in os.listdir(images_dir)]
        self.mask_filenames = [os.path.join(masks_dir, f) for f in os.listdir(masks_dir)]

    def __len__(self):
        return len(self.image_filenames)

    def __getitem__(self, idx):
        if torch.is_tensor(idx):
            idx = idx.tolist()

        img_name = self.image_filenames[idx]
        mask_name = self.mask_filenames[idx]
        image = Image.open(img_name).convert("RGB")
        mask = Image.open(mask_name).convert("L")

        if self.transform:
            image = self.transform(image)
            mask = self.transform(mask)

        return image, mask

# 示例转换
transform = transforms.Compose([
    transforms.Resize((256, 256)),
    transforms.ToTensor(),
])

# 创建数据集实例
dataset = RoadCrackDataset(
    images_dir="path/to/road_cracks/train/images/",
    masks_dir="path/to/road_cracks/train/masks/",
    transform=transform
)

# 创建数据加载器
dataloader = DataLoader(dataset, batch_size=4, shuffle=True, num_workers=4)