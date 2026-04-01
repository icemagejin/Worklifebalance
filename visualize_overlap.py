#!/usr/bin/env python3
from PIL import Image, ImageDraw
import numpy as np

# 读取背景图
bg_path = "/workspace/projects/workspace-aesthetic/posters/background_2026-03-31_v2.jpg"
bg = Image.open(bg_path)
width, height = bg.size
print(f"背景图尺寸：{width}x{height}")

# 读取海报
poster_path = "/workspace/projects/workspace-aesthetic/posters/poster-2026-03-31-final-v2.jpg"
poster = Image.open(poster_path)
poster = poster.resize((width, height))

# 检测背景图的图形区域（暗色区域）
bg_gray = np.array(bg.convert('L'))
bg_dark_mask = bg_gray < 180  # 更宽松的阈值

# 创建可视化
draw = ImageDraw.Draw(poster, 'RGBA')

# 用红色半透明标记图形区域
overlay = Image.new('RGBA', (width, height), (0, 0, 0, 0))
overlay_pixels = np.array(overlay)

# 将掩码应用到overlay
for y in range(height):
    for x in range(width):
        if bg_dark_mask[y, x]:
            overlay_pixels[y, x] = [255, 0, 0, 80]  # 红色半透明

overlay_img = Image.fromarray(overlay_pixels, 'RGBA')
combined = Image.alpha_composite(poster.convert('RGBA'), overlay_img)

# 保存可视化结果
output_path = "/workspace/projects/workspace-aesthetic/posters/visualize_overlap.jpg"
combined.convert('RGB').save(output_path)

print(f"\n✓ 可视化结果已保存：{output_path}")
print("  红色半透明区域表示背景图形位置")
print("  可以直观看到文字与图形的重叠情况")
