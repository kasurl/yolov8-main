import os

img_path = "../datasets/model_construction_common/val_512"
img_list = os.listdir(img_path)
print('img_list: ', img_list)

with open("../datasets/model_construction_common/val_512.txt", 'w') as f:
    for img_name in img_list:
        f.write(img_name + '\n')
