import os
import shutil
import argparse

def classify_dataset(source_folder_1, source_folder_2, target_folder,name1='lwir',name2='visible'):

    # 检查必要的文件是否存在
    train1_path = os.path.join(source_folder_1, 'train')
    train2_path = os.path.join(source_folder_2, 'train')
    val1_path = os.path.join(source_folder_1, 'val')
    val2_path = os.path.join(source_folder_2, 'val')
    source_paths = [train1_path, train2_path, val1_path, val2_path]

    for source_path in source_paths:
        if not os.path.exists(source_path):
            raise FileNotFoundError(f"找不到源文件夹: {source_path}")

    # 创建目标文件夹
    train_target = os.path.join(target_folder, 'train')
    val_target = os.path.join(target_folder, 'val')
    train_target_1 = os.path.join(train_target, name1)
    train_target_2 = os.path.join(train_target, name2)
    val_target_1 = os.path.join(val_target, name1)
    val_target_2 = os.path.join(val_target, name2)

    target_folders = [train_target_1, train_target_2, val_target_1, val_target_2]
    for folder in target_folders:
        os.makedirs(folder,exist_ok=True)

    # 复制文件夹内容
    for i in range(len(source_paths)):
        source_path = source_paths[i]
        target_path = target_folders[i]
        print(f"正在复制 {source_path} 文件夹内容到 {target_path} 文件夹")
        for item in os.listdir(source_path):
            src_item = os.path.join(source_path, item)
            dest_item = os.path.join(target_path, item)
            if os.path.exists(dest_item):
                print(f"警告: 文件 {item} 已存在，将被覆盖")
            shutil.copy2(src_item, dest_item)

    # 统计移动的文件数量
    moved_train = len(os.listdir(train_target_1))+len(os.listdir(train_target_2))
    moved_val = len(os.listdir(val_target_1))+len(os.listdir(val_target_2))

    print(f"成功复制 {moved_train} 个文件到训练集文件夹")
    print(f"成功复制 {moved_val} 个文件到验证集文件夹")
    print(f"训练集文件路径: {train_target}")
    print(f"验证集文件路径: {val_target}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='根据train.txt和val.txt文件分类数据集')
    parser.add_argument('source_folder_1', default='.', help='需要移动的数据集1所在文件夹')
    parser.add_argument('source_folder_2', required=True, help='需要移动的数据集2所在文件夹')
    parser.add_argument('target_folder', required=True, help='目标文件夹')
    parser.add_argument('--name1', default='lwir', help='数据集1图像的名称，默认lwir')
    parser.add_argument('--name2', default='visible', help='数据集2图像的名称，默认visible')

#   python image_solve/split/combine_train_val.py --source_folder_1 /home/data/lwir_visible/lwir --source_folder_2 /home/data/lwir_visible/visible --target_folder /home/data/lwir_visible/combined --name1 lwir --name2 visible
    args = parser.parse_args()
    classify_dataset(args.txt_folder, args.source, args.target)