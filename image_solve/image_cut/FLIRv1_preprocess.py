import cv2
import numpy as np
from PIL import Image
import os
from tqdm import tqdm

input_visible_path = 'datasets/crack_data/模态4'
output_visible_path = 'datasets/crack_data/visible'
input_ir_path = 'datasets/crack_data/模态1'
output_ir_path = 'datasets/crack_data/lwir'

os.makedirs(output_visible_path, exist_ok=True)
os.makedirs(output_ir_path, exist_ok=True)

ir_names = os.listdir(input_ir_path)
visible_names = os.listdir(input_visible_path)


for ir_name in tqdm(ir_names):
    visible_name = ir_name.replace('png','png')
    if visible_name in visible_names:
        img_visible = cv2.imread(os.path.join(input_visible_path, visible_name))
        img_ir = cv2.imread(os.path.join(input_ir_path, ir_name))

        h_visi, w_visi, _ = img_visible.shape
        h_ir, w_ir, _ = img_ir.shape

        if h_visi == 1024 and w_visi == 1280:
            img_ir = img_ir[32:448, 70:590, :]
        elif h_visi == 480 and w_visi == 640:
            img_visible = img_visible[30:480, 40:640, :]
            img_ir = img_ir[30:480, 40:640, :]
        elif h_visi == 1536 and w_visi == 2048:
            img_ir = img_ir[35:419, 65:545, :]
        elif h_visi == 1600 and w_visi == 1800:
            hb = (h_visi - 2.5 * h_ir ) // 2 - 20
            wb = (w_visi - 2.5 * w_ir ) // 2 + 50
            img_visible = img_visible[hb:hb+int(2.5*h_ir), wb:wb+int(2.5*w_ir), :]
        else:
            print(f'Not known Image!:{visible_name}')

        cv2.imwrite(os.path.join(output_ir_path, ir_name.replace('.png','.png')), img_ir)
        cv2.imwrite(os.path.join(output_visible_path, visible_name.replace('.jpg','.png')), img_visible)

    

