#!/usr/bin/env python3
from PIL import Image
import numpy as np

# 读取优化后的海报
poster_path = "/workspace/projects/workspace-aesthetic/posters/poster-2026-03-31-final-v2.jpg"
poster = Image.open(poster_path)
width, height = poster.size
print(f"海报尺寸：{width}x{height}")

# 读取背景图
bg_path = "/workspace/projects/workspace-aesthetic/posters/background_2026-03-31_v2.jpg"
bg = Image.open(bg_path)
bg = bg.resize((width, height))

# 转换为RGB
poster_arr = np.array(poster.convert('RGB'))
bg_arr = np.array(bg.convert('RGB'))

# 提高检测阈值，更准确地识别文字区域
diff = np.abs(poster_arr.astype(int) - bg_arr.astype(int))
diff_sum = diff.sum(axis=2)
text_mask = diff_sum > 50  # 提高阈值从30到50

text_pixels = np.sum(text_mask)
print(f"\n文字区域像素数：{text_pixels} / {width*height} ({text_pixels/(width*height)*100:.1f}%)")

# 检测文字与图形重叠
bg_gray = np.array(bg.convert('L'))
bg_dark_mask = bg_gray < 200

overlap = text_mask & bg_dark_mask
overlap_pixels = np.sum(overlap)
overlap_ratio = overlap_pixels / text_pixels * 100 if text_pixels > 0 else 0
print(f"文字与图形重叠像素：{overlap_pixels} / {text_pixels} ({overlap_ratio:.1f}%)")

# 评价
if overlap_ratio > 0.3:
    print("\n⚠️  警告：文字与图形重叠比例较高（>30%）")
elif overlap_ratio > 0.15:
    print("\n✓ 文字与图形重叠比例适中（15-30%）")
    print("   评价：可以接受")
elif overlap_ratio > 0.05:
    print("\n✓ 文字与图形重叠比例较低（5-15%）")
    print("   评价：排版良好")
else:
    print("\n✓ 文字与图形重叠比例很低（<5%）")
    print("   评价：排版优秀")

# 分析文字分布（使用更高阈值）
text_coords = np.where(text_mask)
if len(text_coords[0]) > 0:
    text_y_min = text_coords[0].min()
    text_y_max = text_coords[0].max()
    print(f"\n文字垂直分布：{text_y_min}-{text_y_max} ({text_y_min/height*100:.0f}%-{text_y_max/height*100:.0f}%)")

# 分析图形分布
bg_dark_coords = np.where(bg_dark_mask)
if len(bg_dark_coords[0]) > 0:
    bg_dark_y_min = bg_dark_coords[0].min()
    bg_dark_y_max = bg_dark_coords[0].max()
    print(f"图形垂直分布：{bg_dark_y_min}-{bg_dark_y_max} ({bg_dark_y_min/height*100:.0f}%-{bg_dark_y_max/height*100:.0f}%)")

    vertical_gap = bg_dark_y_min - text_y_max
    print(f"\n文字底部与图形顶部的垂直距离：{vertical_gap}像素 ({vertical_gap/height*100:.1f}%)")

    if vertical_gap > 50:
        print("✓ 文字与图形有明显的垂直分离（>50像素）")
    elif vertical_gap > 0:
        print("✓ 文字与图形有一定垂直分离（>0像素）")
    else:
        print("⚠️  文字与图形在垂直方向上有重叠")

print(f"\n✓ 验证完成")
