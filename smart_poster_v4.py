#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont
import os

# 读取布局分析结果
with open("/tmp/layout_analysis.txt", "r") as f:
    lines = f.readlines()
    layout_type = lines[0].strip()

# 配置
bg_path = "/workspace/projects/workspace-aesthetic/posters/background_2026-03-31_v2.jpg"
output_path = "/workspace/projects/workspace-aesthetic/posters/poster-2026-03-31-final-v4.jpg"

# 内容（优化版）
date_day = "31"
date_subtitle = "3月31日 · 周二"  # 改为中文副标题
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

# 字号（优化版）
date_day_size = int(height * 0.35)  # 稍微放大主日期
date_subtitle_size = int(width * 0.032)
nongli_size = int(width * 0.028)
bazi_size = int(width * 0.030)
li_bi_size = int(width * 0.026)

# 加载字体
try:
    date_day_font = ImageFont.truetype(font_bold_path, date_day_size)
    date_subtitle_font = ImageFont.truetype(font_regular_path, date_subtitle_size)
    nongli_font = ImageFont.truetype(font_regular_path, nongli_size)
    bazi_font = ImageFont.truetype(font_regular_path, bazi_size)
    li_bi_font = ImageFont.truetype(font_regular_path, li_bi_size)
    print("✓ 字体加载成功")
except Exception as e:
    print(f"✗ 字体加载失败：{e}")

# 布局类型
if layout_type == "bottom":
    print("\n🎨 采用底部布局策略（优化版）")

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

    print(f"  主日期: 31 (字号: {date_day_size})")
    print(f"  副标题: {date_subtitle} (字号: {date_subtitle_size})")
    print(f"  副标题位置 y: {date_subtitle_y} (数字 bottom: {date_day_bbox_drawn[3]})")

    # 3. 农历（偏左，与副标题留出空间）
    nongli_bbox = draw.textbbox((0, 0), nongli, font=nongli_font)
    nongli_x = width * 0.12
    nongli_y = height * 0.50  # 稍微下移，与副标题拉开距离

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

# 绘制文字（优化颜色）
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
print("  优化：")
print("  • 副标题改为中文：3月31日 · 周二")
print("  • 字号层次更清晰")
print("  • 间距更合理")
