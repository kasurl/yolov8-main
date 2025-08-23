import cv2
import numpy as np
from PIL import Image
import os
from tqdm import tqdm

input_visible_path = '../../datasets/crack_200_800/val/lwir'
output_visible_path = '../../datasets/PID/val/lwir'
input_ir_path = '../../datasets/crack_200_800/val/visible'
output_ir_path = '../../datasets/PID/val/visible'

os.makedirs(output_visible_path, exist_ok=True)
os.makedirs(output_ir_path, exist_ok=True)

ir_names = os.listdir(input_ir_path)
visible_names = os.listdir(input_visible_path)


for ir_name in tqdm(ir_names):
    img_ir = cv2.imread(os.path.join(input_ir_path, ir_name))
    img_ir = img_ir[40:480, 80:520, :]
    img_ir = cv2.resize(img_ir, (512, 512), interpolation=cv2.INTER_LINEAR)
    cv2.imwrite(os.path.join(output_ir_path, ir_name.replace('.png','.png')), img_ir)
for visible_name in tqdm(visible_names):
    img_visible = cv2.imread(os.path.join(input_visible_path, visible_name))
    img_visible = img_visible[40:480, 80:520, :]
    img_visible = cv2.resize(img_visible, (512, 512), interpolation=cv2.INTER_LINEAR)
    cv2.imwrite(os.path.join(output_visible_path, visible_name.replace('.jpg','.png')), img_visible)

    

