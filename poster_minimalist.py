#!/usr/bin/env python3
"""
极简主义海报生成器
只有数字+日期，极致留白
"""

from PIL import Image, ImageDraw, ImageFont
import os
import sys

# 获取日期参数
date_str = sys.argv[1] if len(sys.argv) > 1 else None
if not date_str:
    print("Usage: python3 poster_minimalist.py YYYY-MM-DD")
    sys.exit(1)

# 解析日期
from datetime import datetime
date_obj = datetime.strptime(date_str, "%Y-%m-%d")
year = date_obj.year
month = date_obj.month
day = date_obj.day
weekday = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"][date_obj.weekday()]

# 输出路径
output_path = f"/workspace/projects/workspace-aesthetic/posters/poster-{date_str}.jpg"

# 配置
width = 1080
height = 1920

# 创建纯色背景（浅灰白色）
img = Image.new('RGB', (width, height), (245, 243, 240))  # 米白色
draw = ImageDraw.Draw(img)

# 字体（现代无衬线，简洁利落）
font_regular_path = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"

# 字号（超大数字）
date_day_size = int(height * 0.38)  # 超大，占画面近40%
date_subtitle_size = int(width * 0.028)  # 小字，不抢焦点

# 加载字体
try:
    date_day_font = ImageFont.truetype(font_regular_path, date_day_size)
    date_subtitle_font = ImageFont.truetype(font_regular_path, date_subtitle_size)
    print("✓ 字体加载成功")
except Exception as e:
    print(f"✗ 字体加载失败：{e}")
    date_day_font = ImageFont.load_default()
    date_subtitle_font = ImageFont.load_default()

# 超大数字（居中）
date_day = str(day)
date_day_bbox = draw.textbbox((0, 0), date_day, font=date_day_font)
date_day_width = date_day_bbox[2] - date_day_bbox[0]
date_day_height = date_day_bbox[3] - date_day_bbox[1]

# 计算居中位置
date_day_x = (width - date_day_width) // 2
date_day_y = (height - date_day_height) // 2 - 30  # 稍微向上偏移

# 日期文字（小字，居中，在数字下方）
date_subtitle = f"{month}月{day}日 · {weekday}"
date_subtitle_bbox = draw.textbbox((0, 0), date_subtitle, font=date_subtitle_font)
date_subtitle_width = date_subtitle_bbox[2] - date_subtitle_bbox[0]
date_subtitle_x = (width - date_subtitle_width) // 2
date_subtitle_y = date_day_y + date_day_height + 40  # 数字下方，间距40px

# 绘制（深灰色，接近黑色但不纯黑）
text_color = (30, 30, 30)  # 深灰色

draw.text((date_day_x, date_day_y), date_day, font=date_day_font, fill=text_color)
draw.text((date_subtitle_x, date_subtitle_y), date_subtitle, font=date_subtitle_font, fill=text_color)

# 保存
img.save(output_path, quality=95)

print(f"\n✓ 极简海报已生成：{output_path}")
print(f"  文件大小：{os.path.getsize(output_path) / 1024 / 1024:.2f} MB")
print(f"  设计风格：极致极简主义")
print(f"  留白：~80%")
print(f"  信息：数字 + 日期")
