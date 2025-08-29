import cv2
import numpy as np
from PIL import Image
import os
from tqdm import tqdm

input_visible_path = '../../datasets/data_ray/mask/train'
output_visible_path = '../../datasets/PID/mask/train'
input_ir_path = '../../datasets/data_ray/mask/val'
output_ir_path = '../../datasets/PID/mask/val'

os.makedirs(output_visible_path, exist_ok=True)
os.makedirs(output_ir_path, exist_ok=True)

ir_names = os.listdir(input_ir_path)
visible_names = os.listdir(input_visible_path)


for ir_name in tqdm(ir_names):
    img_ir = cv2.imread(os.path.join(input_ir_path, ir_name))
    if img_ir is None:
        print("无法加载图像" + os.path.join(input_ir_path, ir_name) + "，请检查文件路径和文件是否存在")
    else:
        img_ir = img_ir[40:480, 80:520, :]
        img_ir = cv2.resize(img_ir, (512, 512), interpolation=cv2.INTER_LINEAR)
        cv2.imwrite(os.path.join(output_ir_path, ir_name.replace('.png','.png')), img_ir)
for visible_name in tqdm(visible_names):
    img_visible = cv2.imread(os.path.join(input_visible_path, visible_name))
    img_visible = img_visible[40:480, 80:520, :]
    img_visible = cv2.resize(img_visible, (512, 512), interpolation=cv2.INTER_LINEAR)
    cv2.imwrite(os.path.join(output_visible_path, visible_name.replace('.jpg','.png')), img_visible)

    

