import os
import re
from tqdm import tqdm


def rename_files_keep_numbers(folder_path):
    """
    将文件夹下所有文件重命名，只保留文件名开头的数字部分
    例如：14_json.png -> 14.png
    """
    # 获取文件夹中所有文件
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

    # 正则表达式匹配文件名开头的数字
    number_pattern = re.compile(r'^\d+')

    # 遍历所有文件并处理
    for filename in tqdm(files, desc="重命名文件"):
        # 分离文件名和扩展名
        base_name, ext = os.path.splitext(filename)

        # 查找开头的数字
        match = number_pattern.match(base_name)

        if match:
            # 提取数字部分
            number_part = match.group()
            # 新文件名
            new_filename = f"{number_part}{ext}"

            # 构建完整路径
            old_path = os.path.join(folder_path, filename)
            new_path = os.path.join(folder_path, new_filename)

            # 如果新文件名已存在，添加序号避免覆盖
            counter = 1
            while os.path.exists(new_path):
                new_filename = f"{number_part}_{counter}{ext}"
                new_path = os.path.join(folder_path, new_filename)
                counter += 1

            # 重命名文件
            os.rename(old_path, new_path)
        else:
            # 没有数字开头的文件将被跳过
            print(f"跳过文件 '{filename}'：未找到开头的数字部分")


if __name__ == "__main__":
    # 目标文件夹路径
    target_folder = r"D:\codes\py\yolov8-main\datasets\mask"  # 替换为你的文件夹路径

    # 验证文件夹是否存在
    if not os.path.isdir(target_folder):
        print(f"错误：文件夹 '{target_folder}' 不存在！")
    else:
        rename_files_keep_numbers(target_folder)
        print("文件重命名完成！")