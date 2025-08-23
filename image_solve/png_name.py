import os

img_path = "D:\codes\py\yolov8-main\datasets\crack_data\模态1"
img_list = os.listdir(img_path)
print('img_list: ', img_list)

with open("/datasets/segment/txt/all.txt", 'w') as f:
    for img_name in img_list:
        f.write(img_name + '\n')
