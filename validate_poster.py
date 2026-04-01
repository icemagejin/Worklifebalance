#!/usr/bin/env python3
from PIL import Image
import numpy as np

# 读取生成的海报
poster_path = "/workspace/projects/workspace-aesthetic/posters/poster-2026-03-31-final.jpg"
poster = Image.open(poster_path)
width, height = poster.size
print(f"海报尺寸：{width}x{height}")

# 读取背景图（原图）
bg_path = "/workspace/projects/workspace-aesthetic/posters/background_2026-03-31_v2.jpg"
bg = Image.open(bg_path)
bg = bg.resize((width, height))  # 确保尺寸一致

# 转换为RGB
poster_arr = np.array(poster.convert('RGB'))
bg_arr = np.array(bg.convert('RGB'))

# 检测文字区域（与背景相比有显著差异的区域）
diff = np.abs(poster_arr.astype(int) - bg_arr.astype(int))
diff_sum = diff.sum(axis=2)
text_mask = diff_sum > 30  # 差异大于30的像素视为文字

text_pixels = np.sum(text_mask)
print(f"\n文字区域像素数：{text_pixels} / {width*height} ({text_pixels/(width*height)*100:.1f}%)")

# 检查文字区域是否覆盖了背景的主要图形区域
# 原图的暗色区域（图形）
bg_gray = np.array(bg.convert('L'))
bg_dark_mask = bg_gray < 200  # 暗色区域

# 文字与图形重叠的像素
overlap = text_mask & bg_dark_mask
overlap_pixels = np.sum(overlap)
print(f"文字与图形重叠像素：{overlap_pixels} / {text_pixels} ({overlap_pixels/text_pixels*100:.1f}%)")

# 如果重叠比例过高，提示警告
if overlap_pixels / text_pixels > 0.3:
    print("\n⚠️  警告：文字与图形重叠比例较高（>30%）")
    print("   建议：调整文字位置，避开图形区域")
elif overlap_pixels / text_pixels > 0.1:
    print("\n✓ 文字与图形重叠比例适中（10-30%）")
    print("   建议：可以接受，但可以进一步优化")
else:
    print("\n✓ 文字与图形重叠比例低（<10%）")
    print("   评价：排版良好，文字避开了图形")

# 分析文字分布
text_coords = np.where(text_mask)
if len(text_coords[0]) > 0:
    text_y_min = text_coords[0].min()
    text_y_max = text_coords[0].max()
    text_x_min = text_coords[1].min()
    text_x_max = text_coords[1].max()

    print(f"\n文字分布范围：")
    print(f"  水平：{text_x_min}-{text_x_max} ({text_x_min/width*100:.0f}%-{text_x_max/width*100:.0f}%)")
    print(f"  垂直：{text_y_min}-{text_y_max} ({text_y_min/height*100:.0f}%-{text_y_max/height*100:.0f}%)")

# 分析图形分布
bg_dark_coords = np.where(bg_dark_mask)
if len(bg_dark_coords[0]) > 0:
    bg_dark_y_min = bg_dark_coords[0].min()
    bg_dark_y_max = bg_dark_coords[0].max()
    bg_dark_x_min = bg_dark_coords[1].min()
    bg_dark_x_max = bg_dark_coords[1].max()

    print(f"\n图形分布范围：")
    print(f"  水平：{bg_dark_x_min}-{bg_dark_x_max} ({bg_dark_x_min/width*100:.0f}%-{bg_dark_x_max/width*100:.0f}%)")
    print(f"  垂直：{bg_dark_y_min}-{bg_dark_y_max} ({bg_dark_y_min/height*100:.0f}%-{bg_dark_y_max/height*100:.0f}%)")

    # 检查垂直方向的分离
    text_bottom = text_y_max
    bg_top = bg_dark_y_min
    vertical_gap = bg_top - text_bottom
    print(f"\n文字底部与图形顶部的垂直距离：{vertical_gap}像素 ({vertical_gap/height*100:.1f}%)")

    if vertical_gap > 0:
        print("✓ 文字与图形在垂直方向上有分离")
    else:
        print("⚠️  文字与图形在垂直方向上有重叠")

print(f"\n验证完成")
