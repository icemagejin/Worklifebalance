#!/usr/bin/env python3
"""
现代设计海报 - 信息聚合版
超大数字 + 聚合的日期信息
"""

from PIL import Image, ImageDraw, ImageFont
import os
import sys

# 获取日期参数
date_str = sys.argv[1] if len(sys.argv) > 1 else None
if not date_str:
    print("Usage: python3 poster_grouped.py YYYY-MM-DD")
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

# 创建纯色背景
img = Image.new('RGB', (width, height), (245, 243, 240))
draw = ImageDraw.Draw(img)

# 字体（现代无衬线）
font_regular_path = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"

# 字号配置
date_day_size = int(height * 0.30)  # 超大数字
date_info_size = int(width * 0.04)  # 日期信息（月份+星期+年份）

# 加载字体
try:
    date_day_font = ImageFont.truetype(font_regular_path, date_day_size)
    date_info_font = ImageFont.truetype(font_regular_path, date_info_size)
    print("✓ 字体加载成功")
except Exception as e:
    print(f"✗ 字体加载失败：{e}")
    date_day_font = ImageFont.load_default()
    date_info_font = ImageFont.load_default()

# 内容
date_day = str(day)
date_info = f"{month}月{day}日 {weekday} · {year}"

# 超大日期（居中）
date_day_bbox = draw.textbbox((0, 0), date_day, font=date_day_font)
date_day_width = date_day_bbox[2] - date_day_bbox[0]
date_day_height = date_day_bbox[3] - date_day_bbox[1]

date_day_x = (width - date_day_width) // 2
date_day_y = height * 0.25  # 稍微向下

# 日期信息（数字下方，居中）
date_info_bbox = draw.textbbox((0, 0), date_info, font=date_info_font)
date_info_width = date_info_bbox[2] - date_info_bbox[0]
date_info_x = (width - date_info_width) // 2
date_info_y = date_day_y + date_day_height + 60  # 数字下方，间距60px

# 绘制文字
date_day_color = (25, 25, 25)  # 超深色
date_info_color = (100, 100, 100)  # 中灰色

draw.text((date_day_x, date_day_y), date_day, font=date_day_font, fill=date_day_color)
draw.text((date_info_x, date_info_y), date_info, font=date_info_font, fill=date_info_color)

# 保存
img.save(output_path, quality=95)

print(f"\n✓ 信息聚合海报已生成：{output_path}")
print(f"  文件大小：{os.path.getsize(output_path) / 1024 / 1024:.2f} MB")
print(f"  设计风格：现代设计 + 信息聚合")
print(f"  信息：超大数字 + 完整日期信息")
print(f"  布局：居中对齐，信息清晰")
