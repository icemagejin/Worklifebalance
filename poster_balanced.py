#!/usr/bin/env python3
"""
平衡版海报生成器
超大数字 + 适量信息 + 简约背景
"""

from PIL import Image, ImageDraw, ImageFont
import os
import sys

# 获取日期参数
date_str = sys.argv[1] if len(sys.argv) > 1 else None
if not date_str:
    print("Usage: python3 poster_balanced.py YYYY-MM-DD")
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
    print("使用默认背景")
    # 创建简约背景
    from PIL import Image as PILImage
    bg = PILImage.new('RGB', (1080, 1920), (248, 246, 243))
    # 添加一些简约的几何图形
    bg_draw = ImageDraw.Draw(bg)
    # 左上角一个淡色圆形
    bg_draw.ellipse([0, 0, 300, 300], fill=(235, 230, 225))
    bg.save(bg_path)

# 打开背景图
img = Image.open(bg_path)
width, height = img.size

# 添加半透明白色遮罩（让文字更清晰，但保留背景）
draw = ImageDraw.Draw(img, 'RGBA')
overlay = Image.new('RGBA', (width, height), (255, 255, 255, 70))
img_with_overlay = Image.alpha_composite(img.convert('RGBA'), overlay)
draw = ImageDraw.Draw(img_with_overlay, 'RGBA')

# 字体（现代无衬线）
font_regular_path = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"

# 字号配置
date_day_size = int(height * 0.32)  # 超大数字，但不是极端
date_subtitle_size = int(width * 0.032)  # 副标题
nongli_size = int(width * 0.025)  # 农历
yiji_size = int(width * 0.028)  # 宜忌

# 加载字体
try:
    date_day_font = ImageFont.truetype(font_regular_path, date_day_size)
    date_subtitle_font = ImageFont.truetype(font_regular_path, date_subtitle_size)
    nongli_font = ImageFont.truetype(font_regular_path, nongli_size)
    yiji_font = ImageFont.truetype(font_regular_path, yiji_size)
    print("✓ 字体加载成功")
except Exception as e:
    print(f"✗ 字体加载失败：{e}")
    date_day_font = ImageFont.load_default()
    date_subtitle_font = ImageFont.load_default()
    nongli_font = ImageFont.load_default()
    yiji_font = ImageFont.load_default()

# 内容
date_day = str(day)
date_subtitle = f"{month}月{day}日 · {weekday}"
nongli = "农历二月十六"
yi = "宜 祭祀祈福"
ji = "忌 大事勿用"

# 超大数字（居中）
date_day_bbox = draw.textbbox((0, 0), date_day, font=date_day_font)
date_day_width = date_day_bbox[2] - date_day_bbox[0]
date_day_height = date_day_bbox[3] - date_day_bbox[1]

date_day_x = (width - date_day_width) // 2
date_day_y = height * 0.12  # 顶部12%位置

# 副标题（数字下方）
date_subtitle_bbox = draw.textbbox((0, 0), date_subtitle, font=date_subtitle_font)
date_subtitle_width = date_subtitle_bbox[2] - date_subtitle_bbox[0]
date_subtitle_x = (width - date_subtitle_width) // 2
date_subtitle_y = date_day_y + date_day_height + 30

# 农历（左下角）
nongli_bbox = draw.textbbox((0, 0), nongli, font=nongli_font)
nongli_x = width * 0.10
nongli_y = height * 0.80

# 宜忌（左下角，农历下方）
yi_bbox = draw.textbbox((0, 0), yi, font=yiji_font)
yi_x = nongli_x
yi_y = nongli_y + nongli_bbox[3] + 20

ji_bbox = draw.textbbox((0, 0), ji, font=yiji_font)
ji_x = nongli_x
ji_y = yi_y + yi_bbox[3] + 15

# 绘制文字（深灰色系）
date_day_color = (35, 32, 30)  # 主数字，接近黑色
subtitle_color = (70, 65, 60)  # 副标题
info_color = (90, 85, 80)     # 其他信息
yi_color = (120, 100, 80)     # 宜（稍暖）
ji_color = (100, 80, 60)      # 忌（稍暗）

draw.text((date_day_x, date_day_y), date_day, font=date_day_font, fill=date_day_color)
draw.text((date_subtitle_x, date_subtitle_y), date_subtitle, font=date_subtitle_font, fill=subtitle_color)
draw.text((nongli_x, nongli_y), nongli, font=nongli_font, fill=info_color)
draw.text((yi_x, yi_y), yi, font=yiji_font, fill=yi_color)
draw.text((ji_x, ji_y), ji, font=yiji_font, fill=ji_color)

# 保存
img_with_overlay.convert('RGB').save(output_path, quality=95)

print(f"\n✓ 平衡版海报已生成：{output_path}")
print(f"  文件大小：{os.path.getsize(output_path) / 1024 / 1024:.2f} MB")
print(f"  设计风格：平衡美学")
print(f"  留白：~70%")
print(f"  信息：数字 + 日期 + 农历 + 宜忌")
