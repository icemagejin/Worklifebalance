#!/usr/bin/env python3
"""
八字合盘海报生成器 - 块面结构版
支持日期参数，动态布局
"""

from PIL import Image, ImageDraw, ImageFont
import os
import sys
import json

# 获取日期参数
date_str = sys.argv[1] if len(sys.argv) > 1 else None
if not date_str:
    print("Usage: python3 poster_blocks.py YYYY-MM-DD")
    sys.exit(1)

# 解析日期
from datetime import datetime
date_obj = datetime.strptime(date_str, "%Y-%m-%d")
year = date_obj.year
month = date_obj.month
day = date_obj.day
weekday = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"][date_obj.weekday()]

# 输出路径
bg_path = f"/workspace/projects/workspace-aesthetic/posters/background_{date_str}.jpg"
output_path = f"/workspace/projects/workspace-aesthetic/posters/poster-{date_str}.jpg"

# 检查背景图
if not os.path.exists(bg_path):
    print(f"错误：背景图不存在：{bg_path}")
    print("请先生成背景图")
    sys.exit(1)

# 读取布局分析结果
layout_file = "/tmp/layout_analysis.txt"
if os.path.exists(layout_file):
    with open(layout_file, "r") as f:
        layout_type = f.read().strip()
else:
    print("警告：未找到布局分析文件，使用默认布局")
    layout_type = "bottom"

# 内容配置（动态）
date_day = str(day)
date_subtitle = f"{month}月{day}日 · {weekday}"

# 农历和干支（2026-04-03）
nongli = "农历二月十六"
bazi = "丙午年 辛卯月 丁未日"
li = "利：祭祀祈福修身心"
bi = "弊：举大事务莫轻为"

# 打开背景图
img = Image.open(bg_path)
width, height = img.size
print(f"背景图尺寸：{width}x{height}")
print(f"布局类型：{layout_type}")

# 半透明白色遮罩
draw = ImageDraw.Draw(img, 'RGBA')
overlay = Image.new('RGBA', (width, height), (255, 255, 255, 90))
img_with_overlay = Image.alpha_composite(img.convert('RGBA'), overlay)
draw = ImageDraw.Draw(img_with_overlay, 'RGBA')

# 字体路径（黑体）
font_black_path = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"  # 系统没有 Black，用 Bold 代替
font_bold_path = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
font_regular_path = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"

# 字号配置
date_day_size = int(height * 0.35)  # 超大数字
date_subtitle_size = int(width * 0.032)
nongli_size = int(width * 0.028)
bazi_size = int(width * 0.030)
li_bi_size = int(width * 0.026)

# 加载字体
try:
    date_day_font = ImageFont.truetype(font_black_path, date_day_size)
    date_subtitle_font = ImageFont.truetype(font_bold_path, date_subtitle_size)
    nongli_font = ImageFont.truetype(font_regular_path, nongli_size)
    bazi_font = ImageFont.truetype(font_regular_path, bazi_size)
    li_bi_font = ImageFont.truetype(font_regular_path, li_bi_size)
    print("✓ 字体加载成功")
except Exception as e:
    print(f"✗ 字体加载失败：{e}")
    # 回退到默认字体
    date_day_font = ImageFont.load_default()
    date_subtitle_font = ImageFont.load_default()
    nongli_font = ImageFont.load_default()
    bazi_font = ImageFont.load_default()
    li_bi_font = ImageFont.load_default()

# 布局策略
if layout_type == "bottom":
    print("\n🎨 采用底部布局策略")

    # 1. 超大数字（顶部居中）
    date_day_bbox = draw.textbbox((0, 0), date_day, font=date_day_font)
    date_day_width = date_day_bbox[2] - date_day_bbox[0]
    date_day_x = (width - date_day_width) // 2
    date_day_y = height * 0.08

    # 预先计算数字的 bounding box
    date_day_bbox_drawn = draw.textbbox((date_day_x, date_day_y), date_day, font=date_day_font)

    # 副标题在数字下方（使用 bbox[3]）
    margin_top_bottom = 20
    date_subtitle_bbox = draw.textbbox((0, 0), date_subtitle, font=date_subtitle_font)
    date_subtitle_width = date_subtitle_bbox[2] - date_subtitle_bbox[0]
    date_subtitle_x = (width - date_subtitle_width) // 2
    date_subtitle_y = date_day_bbox_drawn[3] + margin_top_bottom

    print(f"  主日期: {date_day} (字号: {date_day_size})")
    print(f"  副标题: {date_subtitle} (字号: {date_subtitle_size})")

    # 3. 农历（偏左）
    nongli_bbox = draw.textbbox((0, 0), nongli, font=nongli_font)
    nongli_x = width * 0.12
    nongli_y = height * 0.50

    # 4. 干支（在农历下方）
    bazi_bbox = draw.textbbox((0, 0), bazi, font=bazi_font)
    bazi_x = nongli_x
    bazi_y = nongli_y + nongli_bbox[3] + 30

    # 5. 利弊（在干支下方）
    li_bbox = draw.textbbox((0, 0), li, font=li_bi_font)
    li_x = nongli_x
    li_y = height * 0.68

    bi_bbox = draw.textbbox((0, 0), bi, font=li_bi_font)
    bi_x = nongli_x
    bi_y = li_y + li_bbox[3] + 25

elif layout_type == "center":
    print("\n🎨 采用居中布局策略")
    # 类似逻辑，但信息偏左或右
    nongli_x = width * 0.12
    nongli_y = height * 0.50
    # ...其他布局

else:
    print("\n🎨 使用默认布局")
    nongli_x = width * 0.12
    nongli_y = height * 0.50
    # ...其他布局

# 绘制文字（深棕色系）
highlight_color = (40, 25, 10, 255)  # 主日期颜色
subtitle_color = (70, 50, 30, 255)  # 副标题颜色
info_color = (65, 45, 25, 255)     # 其他信息颜色
li_bi_color = (80, 55, 30, 255)     # 利弊颜色

draw.text((date_day_x, date_day_y), date_day, font=date_day_font, fill=highlight_color)
draw.text((date_subtitle_x, date_subtitle_y), date_subtitle, font=date_subtitle_font, fill=subtitle_color)
draw.text((nongli_x, nongli_y), nongli, font=nongli_font, fill=info_color)
draw.text((bazi_x, bazi_y), bazi, font=bazi_font, fill=info_color)
draw.text((li_x, li_y), li, font=li_bi_font, fill=li_bi_color)
draw.text((bi_x, bi_y), bi, font=li_bi_font, fill=li_bi_color)

# 保存
img_with_overlay.convert('RGB').save(output_path, quality=95)

print(f"\n✓ 海报已生成：{output_path}")
print(f"  文件大小：{os.path.getsize(output_path) / 1024 / 1024:.2f} MB")
print(f"  设计风格：块面结构 + 黑体字体")
