import os
from tqdm import tqdm
import shutil


def move_single_label_per_folder(source_dir, target_dir):
    # 确保目标目录存在
    os.makedirs(target_dir, exist_ok=True)

    # 存储找到的label文件路径及其所在文件夹
    label_files = []

    # 遍历源目录
    for root, dirs, files in os.walk(source_dir):
        # 检查当前文件夹是否包含label.png
        if "label.png" in files:
            label_path = os.path.join(root, "label.png")
            # 记录label文件路径和其所在文件夹
            label_files.append((label_path, root))

    # 移动文件，使用所在文件夹名作为新文件名
    for label_path, folder_path in tqdm(label_files, desc="移动label文件"):
        # 获取文件夹名称（作为新文件名）
        folder_name = os.path.basename(folder_path)
        # 目标文件路径
        target_path = os.path.join(target_dir, f"{folder_name}.png")

        # 处理可能的重名情况（虽然每个文件夹唯一，但可能有同名文件夹）
        counter = 1
        while os.path.exists(target_path):
            target_path = os.path.join(target_dir, f"{folder_name}_{counter}.png")
            counter += 1

        # 执行移动
        try:
            shutil.move(label_path, target_path)
        except Exception as e:
            print(f"移动文件 {label_path} 失败: {str(e)}")


if __name__ == "__main__":
    # 源目录和目标目录
    source_directory = r"D:\codes\py\yolov8-main\datasets\crack_data\标注文件"
    target_directory = r"D:\codes\py\yolov8-main\datasets\mask"

    move_single_label_per_folder(source_directory, target_directory)
    print(f"所有label文件已移动到 {target_directory}")