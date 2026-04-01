#!/usr/bin/env python3
from PIL import Image
import numpy as np

# 读取背景图
img = Image.open("/workspace/projects/workspace-aesthetic/posters/background_2026-03-31_v2.jpg")
width, height = img.size
print(f"图片尺寸：{width}x{height}")

# 转换为灰度图
gray = img.convert('L')
gray_arr = np.array(gray)

# 计算垂直方向的像素密度（检测图形主要集中在哪个垂直区域）
# 将图像分为上、中、下三部分
top_region = gray_arr[0:int(height*0.33), :]
middle_region = gray_arr[int(height*0.33):int(height*0.66), :]
bottom_region = gray_arr[int(height*0.66):, :]

# 计算每个区域的暗色像素比例（像素值小于200视为暗色/有图形）
top_dark = np.sum(top_region < 200) / top_region.size * 100
middle_dark = np.sum(middle_region < 200) / middle_region.size * 100
bottom_dark = np.sum(bottom_region < 200) / bottom_region.size * 100

print(f"\n垂直区域暗色像素比例：")
print(f"  上部（0-33%）：{top_dark:.1f}%")
print(f"  中部（33-66%）：{middle_dark:.1f}%")
print(f"  下部（66-100%）：{bottom_dark:.1f}%")

# 计算水平方向的像素密度（检测图形主要集中在哪个水平区域）
# 将图像分为左、中、右三部分
left_region = gray_arr[:, 0:int(width*0.33)]
center_region = gray_arr[:, int(width*0.33):int(width*0.66)]
right_region = gray_arr[:, int(width*0.66):]

left_dark = np.sum(left_region < 200) / left_region.size * 100
center_dark = np.sum(center_region < 200) / center_region.size * 100
right_dark = np.sum(right_region < 200) / right_region.size * 100

print(f"\n水平区域暗色像素比例：")
print(f"  左侧（0-33%）：{left_dark:.1f}%")
print(f"  中间（33-66%）：{center_dark:.1f}%")
print(f"  右侧（66-100%）：{right_dark:.1f}%")

# 判断布局类型
layout_type = "center"
if top_dark > middle_dark and top_dark > bottom_dark:
    layout_type = "top"
elif bottom_dark > top_dark and bottom_dark > middle_dark:
    layout_type = "bottom"
elif left_dark > center_dark and left_dark > right_dark:
    layout_type = "left"
elif right_dark > center_dark and right_dark > left_dark:
    layout_type = "right"

print(f"\n📊 布局类型：{layout_type}")

# 确定空白区域（文字应该放在哪里）
empty_region = []
if bottom_dark < 10:
    empty_region.append("底部空白充足")
if top_dark < 10:
    empty_region.append("顶部空白充足")
if middle_dark < 10:
    empty_region.append("中间空白充足")

print(f"\n✅ 适合放置文字的区域：{', '.join(empty_region) if empty_region else '无明显空白区域'}")

# 输出布局建议
print(f"\n🎨 排版建议：")
if layout_type == "bottom":
    print("  - 图形主要集中在底部")
    print("  - 文字可以放在上方和中上部")
    print("  - 利弊可以放在中间区域")
elif layout_type == "left":
    print("  - 图形主要集中在左侧")
    print("  - 文字可以放在右侧")
    print("  - 建议右对齐或居中偏右")
elif layout_type == "right":
    print("  - 图形主要集中在右侧")
    print("  - 文字可以放在左侧")
    print("  - 建议左对齐或居中偏左")
elif layout_type == "center":
    print("  - 图形分布较均匀")
    print("  - 建议采用上下结构")
    print("  - 大数字在上方，其他信息在下方")
else:
    print("  - 图形主要集中在顶部")
    print("  - 文字可以放在下方")
    print("  - 利弊和干支信息可以放在底部")

# 保存分析结果到文件供脚本使用
with open("/tmp/layout_analysis.txt", "w") as f:
    f.write(f"{layout_type}\n")
    f.write(f"top_dark={top_dark:.1f}\n")
    f.write(f"middle_dark={middle_dark:.1f}\n")
    f.write(f"bottom_dark={bottom_dark:.1f}\n")
    f.write(f"left_dark={left_dark:.1f}\n")
    f.write(f"center_dark={center_dark:.1f}\n")
    f.write(f"right_dark={right_dark:.1f}\n")

print(f"\n分析结果已保存到 /tmp/layout_analysis.txt")
