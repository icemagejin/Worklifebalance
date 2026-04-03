#!/usr/bin/env python3
"""
现代设计感海报生成器
纯色背景 + 超大数字 + 精致排版
"""

from PIL import Image, ImageDraw, ImageFont
import os
import sys

# 获取日期参数
date_str = sys.argv[1] if len(sys.argv) > 1 else None
if not date_str:
    print("Usage: python3 poster_modern.py YYYY-MM-DD")
    sys.exit(1)

# 解析日期
from datetime import datetime
date_obj = datetime.strptime(date_str, "%Y-%m-%d")
year = date_obj.year
month = date_obj.month
day = date_obj.day
weekday = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"][date_obj.weekday()]

# 输出路径
output_path = f"/workspace/projects/workspace-aesthetic/posters/poster-{date_str}.jpg"

# 配置
width = 1080
height = 1920

# 创建渐变背景（纯色渐变，避免图形压字）
img = Image.new('RGB', (width, height), (245, 243, 240))
draw = ImageDraw.Draw(img)

# 添加一个超大极淡的装饰圆形（在右上角，不影响文字）
draw.ellipse([width-400, -100, width+100, 300], fill=(235, 230, 225))
draw.ellipse([width-300, -50, width, 200], fill=(240, 238, 235))

# 字体（现代无衬线）
font_regular_path = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"

# 字号配置 - 现代设计感
date_day_size = int(height * 0.30)  # 超大数字
date_month_size = int(width * 0.06)  # 月份大字
date_weekday_size = int(width * 0.03)  # 星期小字
date_year_size = int(width * 0.035)  # 年份

# 加载字体
try:
    date_day_font = ImageFont.truetype(font_regular_path, date_day_size)
    date_month_font = ImageFont.truetype(font_regular_path, date_month_size)
    date_weekday_font = ImageFont.truetype(font_regular_path, date_weekday_size)
    date_year_font = ImageFont.truetype(font_regular_path, date_year_size)
    print("✓ 字体加载成功")
except Exception as e:
    print(f"✗ 字体加载失败：{e}")
    date_day_font = ImageFont.load_default()
    date_month_font = ImageFont.load_default()
    date_weekday_font = ImageFont.load_default()
    date_year_font = ImageFont.load_default()

# 现代排版方案
date_day = str(day)
date_month = f"{month:02d}"  # 两位数月份，如 04
date_weekday = weekday
date_year = str(year)

# 超大日期（居中）
date_day_bbox = draw.textbbox((0, 0), date_day, font=date_day_font)
date_day_width = date_day_bbox[2] - date_day_bbox[0]
date_day_height = date_day_bbox[3] - date_day_bbox[1]

date_day_x = (width - date_day_width) // 2
date_day_y = height * 0.20  # 稍微向下

# 月份（左上角，竖向排列或横向）
date_month_bbox = draw.textbbox((0, 0), date_month, font=date_month_font)
date_month_x = width * 0.08
date_month_y = height * 0.18

# 星期（右上角）
date_weekday_bbox = draw.textbbox((0, 0), date_weekday, font=date_weekday_font)
date_weekday_width = date_weekday_bbox[2] - date_weekday_bbox[0]
date_weekday_x = width - date_weekday_width - width * 0.08
date_weekday_y = height * 0.22

# 年份（右下角）
date_year_bbox = draw.textbbox((0, 0), date_year, font=date_year_font)
date_year_width = date_year_bbox[2] - date_year_bbox[0]
date_year_x = width - date_year_width - width * 0.08
date_year_y = height * 0.85

# 绘制文字（现代配色）
date_day_color = (25, 25, 25)  # 超深色
month_color = (80, 80, 80)     # 中灰色
weekday_color = (120, 120, 120)  # 浅灰色
year_color = (100, 100, 100)   # 灰色

draw.text((date_day_x, date_day_y), date_day, font=date_day_font, fill=date_day_color)
draw.text((date_month_x, date_month_y), date_month, font=date_month_font, fill=month_color)
draw.text((date_weekday_x, date_weekday_y), date_weekday, font=date_weekday_font, fill=weekday_color)
draw.text((date_year_x, date_year_y), date_year, font=date_year_font, fill=year_color)

# 保存
img.save(output_path, quality=95)

print(f"\n✓ 现代设计海报已生成：{output_path}")
print(f"  文件大小：{os.path.getsize(output_path) / 1024 / 1024:.2f} MB")
print(f"  设计风格：现代设计感")
print(f"  信息：超大日期 + 月份 + 星期 + 年份")
print(f"  布局：对称简约")
