import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from glob import glob
from matplotlib import gridspec


# ---------------------- 全局配置（符合SCI论文规范） ----------------------
def setup_sci_plot_style():
    plt.rcParams.update({
        'font.family': 'serif',
        'font.serif': ['Times New Roman', 'DejaVu Serif'],
        'font.size': 9,
        'axes.linewidth': 0.7,
        'xtick.major.width': 0.7,
        'ytick.major.width': 0.7,
        'xtick.major.size': 3,
        'ytick.major.size': 3,
        'savefig.dpi': 600,
        'savefig.format': 'tif',
        'savefig.bbox': 'tight',
        'savefig.pad_inches': 0.05
    })


# ---------------------- 裂缝特征提取 ----------------------
def extract_red_crack_features(bgr_img):
    hsv_img = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2HSV)

    # 红色检测范围
    lower_red1 = np.array([0, 80, 30])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([170, 80, 30])
    upper_red2 = np.array([180, 255, 255])

    mask1 = cv2.inRange(hsv_img, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv_img, lower_red2, upper_red2)
    red_mask = cv2.bitwise_or(mask1, mask2)

    # 形态学处理
    kernel = np.ones((3, 3), np.uint8)
    red_mask = cv2.morphologyEx(red_mask, cv2.MORPH_OPEN, kernel, iterations=1)
    red_mask = cv2.morphologyEx(red_mask, cv2.MORPH_CLOSE, kernel, iterations=1)

    return red_mask


# ---------------------- 生成四种可视化方案 ----------------------
def generate_four_visualization_options(image_folder,
                                        target_size=(512, 512),
                                        output_prefix="crack_distribution_option_",
                                        tick_interval=100):
    """生成四种不同风格的黑白裂缝分布可视化方案"""
    # 1. 加载并处理图像（一次处理，多次可视化）
    image_extensions = ["*.jpg", "*.jpeg", "*.png", "*.bmp", "*.tif"]
    image_paths = []
    for ext in image_extensions:
        image_paths.extend(glob(os.path.join(image_folder, ext)))

    if not image_paths:
        raise ValueError("未找到任何图像，请检查路径！")

    # 计算裂缝分布（只计算一次）
    crack_count = np.zeros(target_size, dtype=np.float32)
    valid_count = 0

    for path in image_paths:
        bgr_img = cv2.imread(path)
        if bgr_img is None:
            print(f"跳过无效图像：{os.path.basename(path)}")
            continue

        resized = cv2.resize(bgr_img, target_size, interpolation=cv2.INTER_NEAREST)
        crack_mask = extract_red_crack_features(resized)
        crack_count[crack_mask == 255] += 1
        valid_count += 1

    if valid_count == 0:
        raise ValueError("没有有效图像可处理！")
    if np.max(crack_count) == 0:
        raise ValueError("未检测到红色裂缝！")

    # 归一化处理
    normalized = (crack_count / np.max(crack_count)) * 1.0

    # 2. 设置SCI绘图样式
    setup_sci_plot_style()

    # 3. 生成四种方案
    options = [
        {
            "name": "standard_gray",
            "cmap": "gray",
            "description": "标准灰度图，裂缝越密越亮",
            "show_minor_ticks": False,
            "colorbar_label": "Relative Density"
        },
        {
            "name": "inverted_gray",
            "cmap": "gray_r",
            "description": "反相灰度图，裂缝越密越暗",
            "show_minor_ticks": False,
            "colorbar_label": "Relative Density"
        },
        {
            "name": "high_contrast",
            "cmap": "gray",
            "description": "高对比度灰度图，增强细节区分",
            "show_minor_ticks": True,
            "colorbar_label": "Normalized Intensity",
            "gamma": 0.7  # 增强对比度
        },
        {
            "name": "smooth_gray",
            "cmap": "gray",
            "description": "平滑灰度图，减少噪声干扰",
            "show_minor_ticks": True,
            "colorbar_label": "Relative Frequency",
            "smooth": True
        }
    ]

    # 4. 为每种方案生成图像
    for i, opt in enumerate(options, 1):
        fig = plt.figure(figsize=(6, 5))
        gs = gridspec.GridSpec(1, 2, width_ratios=[15, 1], wspace=0.03)

        # 处理数据（平滑或伽马校正）
        data = normalized.copy()
        if "gamma" in opt:
            data = data ** opt["gamma"]
        if opt.get("smooth", False):
            # 应用高斯平滑
            data = cv2.GaussianBlur(data, (5, 5), 0)

        # 主图像
        ax_img = fig.add_subplot(gs[0])
        im = ax_img.imshow(data, cmap=opt["cmap"], origin='upper',
                           extent=[0, target_size[0], target_size[1], 0])

        # 配置坐标轴
        ax_img.set_title('')
        ax_img.set_xlabel('')
        ax_img.set_ylabel('')

        # 设置整数刻度
        max_coord = max(target_size)
        ticks = np.arange(0, max_coord + 1, tick_interval)
        ax_img.set_xticks(ticks[ticks <= target_size[0]])
        ax_img.set_yticks(ticks[ticks <= target_size[1]])

        # 显示次刻度（如果需要）
        if opt["show_minor_ticks"]:
            from matplotlib.ticker import AutoMinorLocator
            ax_img.xaxis.set_minor_locator(AutoMinorLocator(2))
            ax_img.yaxis.set_minor_locator(AutoMinorLocator(2))

        # 颜色条
        ax_cbar = fig.add_subplot(gs[1])
        cbar = plt.colorbar(im, cax=ax_cbar)
        cbar.set_label(opt["colorbar_label"], rotation=270, labelpad=12)
        cbar.ax.tick_params(pad=2)

        # 保存图像
        output_path = f"{output_prefix}{i}_{opt['name']}.tif"
        plt.savefig(output_path, dpi=600, bbox_inches='tight',
                    pil_kwargs={"compression": "tiff_lzw"})
        print(f"方案 {i} 已保存至：{output_path} ({opt['description']})")
        plt.close()  # 关闭图像以释放内存

    return normalized


# ---------------------- 主函数 ----------------------
if __name__ == "__main__":
    IMAGE_FOLDER = "../datasets/PID/mask/val"  # 替换为你的图像文件夹路径

    try:
        generate_four_visualization_options(
            image_folder=IMAGE_FOLDER,
            target_size=(512, 512),
            tick_interval=100  # 整数坐标间隔
        )
    except Exception as e:
        print(f"处理失败：{str(e)}")
