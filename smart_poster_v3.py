#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont
import os

# 读取布局分析结果
with open("/tmp/layout_analysis.txt", "r") as f:
    lines = f.readlines()
    layout_type = lines[0].strip()

# 配置
bg_path = "/workspace/projects/workspace-aesthetic/posters/background_2026-03-31_v2.jpg"
output_path = "/workspace/projects/workspace-aesthetic/posters/poster-2026-03-31-final-v3.jpg"

# 内容
date_day = "31"
month_week = "MAR TUE"
nongli = "农历二月十三"
bazi = "丙午年 辛卯月 甲辰日"
li = "利：扫舍除尘净心性"
bi = "弊：嫁娶之事莫当行"

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

# 字体路径
font_bold_path = "/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc"
font_regular_path = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"

# 字号
date_day_size = int(height * 0.32)
month_week_size = int(width * 0.032)
nongli_size = int(width * 0.028)
bazi_size = int(width * 0.032)
li_bi_size = int(width * 0.026)

# 加载字体
try:
    date_day_font = ImageFont.truetype(font_bold_path, date_day_size)
    month_week_font = ImageFont.truetype(font_regular_path, month_week_size)
    nongli_font = ImageFont.truetype(font_regular_path, nongli_size)
    bazi_font = ImageFont.truetype(font_regular_path, bazi_size)
    li_bi_font = ImageFont.truetype(font_regular_path, li_bi_size)
    print("✓ 字体加载成功")
except Exception as e:
    print(f"✗ 字体加载失败：{e}")

# 布局类型
if layout_type == "bottom":
    print("\n🎨 采用底部布局策略（修复重叠问题）")

    # 1. 超大数字（顶部）
    date_day_x = (width - draw.textbbox((0, 0), date_day, font=date_day_font)[2]) // 2
    date_day_y = height * 0.08

    # 预先计算数字的 bounding box
    date_day_bbox = draw.textbbox((date_day_x, date_day_y), date_day, font=date_day_font)
    print(f"  数字 bbox: {date_day_bbox}")

    # 月周在数字的 bottom 下方（不是 y + height！）
    margin_top_bottom = 25
    month_week_bbox = draw.textbbox((0, 0), month_week, font=month_week_font)
    month_week_width = month_week_bbox[2] - month_week_bbox[0]
    month_week_x = (width - month_week_width) // 2
    month_week_y = date_day_bbox[3] + margin_top_bottom  # 使用 bbox[3]（bottom）

    print(f"  数字 bottom: {date_day_bbox[3]}")
    print(f"  月周 y: {month_week_y} (bottom + margin)")

    # 3. 农历（偏左）
    nongli_bbox = draw.textbbox((0, 0), nongli, font=nongli_font)
    nongli_x = width * 0.12
    nongli_y = height * 0.45

    # 4. 干支（在农历下方）
    bazi_bbox = draw.textbbox((0, 0), bazi, font=bazi_font)
    bazi_x = nongli_x
    bazi_y = nongli_y + nongli_bbox[3] + 30  # 使用 bbox[3]

    # 5. 利弊
    li_bbox = draw.textbbox((0, 0), li, font=li_bi_font)
    li_x = nongli_x
    li_y = height * 0.63

    bi_bbox = draw.textbbox((0, 0), bi, font=li_bi_font)
    bi_x = nongli_x
    bi_y = li_y + li_bbox[3] + 25  # 使用 bbox[3]

# 绘制文字
info_color = (60, 40, 20, 255)
highlight_color = (40, 25, 10, 255)
li_bi_color = (80, 55, 30, 255)

draw.text((date_day_x, date_day_y), date_day, font=date_day_font, fill=highlight_color)
draw.text((month_week_x, month_week_y), month_week, font=month_week_font, fill=info_color)
draw.text((nongli_x, nongli_y), nongli, font=nongli_font, fill=info_color)
draw.text((bazi_x, bazi_y), bazi, font=bazi_font, fill=info_color)
draw.text((li_x, li_y), li, font=li_bi_font, fill=li_bi_color)
draw.text((bi_x, bi_y), bi, font=li_bi_font, fill=li_bi_color)

# 保存
img_with_overlay.convert('RGB').save(output_path, quality=95)

print(f"\n✓ 海报已生成：{output_path}")
print(f"  文件大小：{os.path.getsize(output_path) / 1024 / 1024:.2f} MB")
print("  修复：使用 bbox[3]（bottom）计算位置，避免重叠")
