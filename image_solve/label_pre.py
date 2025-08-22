import os
import shutil

def adjust_coordinates(original_coords, original_size=(640, 480), new_size=(480, 384),x_cut=98,y_cut=45):
    """调整单个目标坐标"""
    # 计算宽和高的缩放比例

    # 解包原始坐标
    xmin, ymin, xmax, ymax = original_coords

    # 计算新坐标
    new_xmin = (xmin * original_size[0] -x_cut )/new_size[0]
    new_ymin = (ymin * original_size[1] -y_cut )/new_size[1]
    new_xmax = (xmax * original_size[0] -x_cut )/new_size[0]
    new_ymax = (ymax * original_size[1] -y_cut )/new_size[1]

    # 返回调整后的坐标，保留两位小数
    return (
        round(new_xmin, 6),
        round(new_ymin, 6),
        round(new_xmax, 6),
        round(new_ymax, 6)
    )


def process_annotation_file(input_file, output_file):
    """处理单个标注文件"""
    try:
        with open(input_file, 'r') as f:
            lines = f.readlines()

        adjusted_lines = []
        for line in lines:
            # 假设标注格式为: 类别 xmin ymin xmax ymax (空格分隔)
            parts = line.strip().split()
            if len(parts) != 5:
                print(f"警告: 文件 {input_file} 中的行 '{line.strip()}' 格式不正确，已跳过")
                continue

            # 提取类别和坐标
            class_id = parts[0]
            coords = tuple(map(float, parts[1:5]))

            # 调整坐标
            new_coords = adjust_coordinates(coords)

            # 组合成新的行
            if (new_coords[0] > 0 and new_coords[1]>0 and new_coords[2]>0 and new_coords[3]>0):
                new_line = f"{class_id} {' '.join(map(str, new_coords))}\n"
                adjusted_lines.append(new_line)

        # 保存调整后的标注
        with open(output_file, 'w') as f:
            f.writelines(adjusted_lines)

        return True

    except Exception as e:
        print(f"处理文件 {input_file} 时出错: {str(e)}")
        return False


def process_all_annotations(input_dir, output_dir):
    """处理目录中所有标注文件"""
    # 创建输出目录（如果不存在）
    os.makedirs(output_dir, exist_ok=True)

    # 获取所有txt文件
    txt_files = [f for f in os.listdir(input_dir) if f.endswith('.txt')]

    if not txt_files:
        print(f"在目录 {input_dir} 中未找到任何txt文件")
        return

    total = len(txt_files)
    success = 0

    print(f"找到 {total} 个标注文件，开始处理...")

    for txt_file in txt_files:
        input_path = os.path.join(input_dir, txt_file)
        output_path = os.path.join(output_dir, txt_file)

        if process_annotation_file(input_path, output_path):
            success += 1

    print(f"处理完成: 成功 {success}/{total} 个文件")


if __name__ == "__main__":
    # 配置输入输出目录
    input_directory = "/home/kamarl/PycharmProjects/PID/dataset/labels/val"  # 原始标注文件所在目录
    output_directory = "/home/kamarl/PycharmProjects/PID/dataset/label/val"   # 调整后标注文件保存目录

    # 如果输出目录已存在，先清空（可选）
    if os.path.exists(output_directory):
        shutil.rmtree(output_directory)

    # 处理所有标注文件
    #process_annotation_file(input_directory, output_directory)
    process_all_annotations(input_directory, output_directory)