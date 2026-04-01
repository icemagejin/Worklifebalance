#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont
import os

# 读取布局分析结果
with open("/tmp/layout_analysis.txt", "r") as f:
    lines = f.readlines()
    layout_type = lines[0].strip()

# 配置
bg_path = "/workspace/projects/workspace-aesthetic/posters/background_2026-03-31_v2.jpg"
output_path = "/workspace/projects/workspace-aesthetic/posters/poster-2026-03-31-final.jpg"

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

# 半透明白色遮罩（更轻薄，保留背景的轻盈感）
draw = ImageDraw.Draw(img, 'RGBA')
overlay = Image.new('RGBA', (width, height), (255, 255, 255, 80))
img_with_overlay = Image.alpha_composite(img.convert('RGBA'), overlay)
draw = ImageDraw.Draw(img_with_overlay, 'RGBA')

# 字体路径（使用粗体字体，有力度）
font_bold_path = "/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc"
font_regular_path = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"

# 动态字号计算（根据图片尺寸和布局类型）
# 超大数字占画面 35%，根据布局调整
if layout_type == "bottom":
    date_day_size = int(height * 0.35)
else:
    date_day_size = int(height * 0.38)

# 其他字号也根据内容长度和空间动态调整
month_week_size = int(width * 0.035)  # 相对于宽度
nongli_size = int(width * 0.030)
bazi_size = int(width * 0.034)
li_bi_size = int(width * 0.028)

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
    date_day_font = ImageFont.load_default()
    month_week_font = ImageFont.load_default()
    nongli_font = ImageFont.load_default()
    bazi_font = ImageFont.load_default()
    li_bi_font = ImageFont.load_default()

# 根据布局类型动态排版
if layout_type == "bottom":
    print("\n🎨 采用底部布局策略：")
    print("  - 大数字在顶部 (10-45%)")
    print("  - 月周在数字下方")
    print("  - 农历+干支在中上部 (50-65%)")
    print("  - 利弊在中间 (70-85%)")
    print("  - 避开底部右下角图形")

    # 1. 上半块面 - 超大数字（顶部区域）
    date_day_bbox = draw.textbbox((0, 0), date_day, font=date_day_font)
    date_day_width = date_day_bbox[2] - date_day_bbox[0]
    date_day_height = date_day_bbox[3] - date_day_bbox[1]
    date_day_x = (width - date_day_width) // 2
    date_day_y = height * 0.10

    # 2. 月周（在数字下方）
    month_week_bbox = draw.textbbox((0, 0), month_week, font=month_week_font)
    month_week_width = month_week_bbox[2] - month_week_bbox[0]
    month_week_height = month_week_bbox[3] - month_week_bbox[1]
    month_week_x = (width - month_week_width) // 2
    month_week_y = date_day_y + date_day_height + 25

    # 3. 中间块面 - 农历（偏左，避开右下角图形）
    nongli_bbox = draw.textbbox((0, 0), nongli, font=nongli_font)
    nongli_width = nongli_bbox[2] - nongli_bbox[0]
    nongli_height = nongli_bbox[3] - nongli_bbox[1]
    nongli_x = width * 0.12  # 偏左12%
    nongli_y = height * 0.52  # 中上部

    # 4. 干支（在农历下方，左对齐）
    bazi_bbox = draw.textbbox((0, 0), bazi, font=bazi_font)
    bazi_width = bazi_bbox[2] - bazi_bbox[0]
    bazi_height = bazi_bbox[3] - bazi_bbox[1]
    bazi_x = nongli_x  # 与农历左对齐
    bazi_y = nongli_y + nongli_height + 35

    # 5. 利弊（在干支下方，左对齐）
    li_bbox = draw.textbbox((0, 0), li, font=li_bi_font)
    li_width = li_bbox[2] - li_bbox[0]
    li_height = li_bbox[3] - li_bbox[1]
    li_x = nongli_x  # 继续左对齐
    li_y = height * 0.72

    bi_bbox = draw.textbbox((0, 0), bi, font=li_bi_font)
    bi_width = bi_bbox[2] - bi_bbox[0]
    bi_height = bi_bbox[3] - bi_bbox[1]
    bi_x = nongli_x  # 左对齐
    bi_y = li_y + li_height + 30

elif layout_type == "left":
    print("\n🎨 采用左侧布局策略：")
    print("  - 文字放在右侧")
    print("  - 右对齐或居中偏右")

    # 左侧布局：文字偏右
    date_day_size = int(height * 0.35)
    date_day_font = ImageFont.truetype(font_bold_path, date_day_size)

    date_day_bbox = draw.textbbox((0, 0), date_day, font=date_day_font)
    date_day_width = date_day_bbox[2] - date_day_bbox[0]
    date_day_x = width * 0.70  # 偏右
    date_day_y = height * 0.10

    month_week_x = width * 0.70
    month_week_y = date_day_y + date_day_bbox[3] + 25

    nongli_x = width * 0.55
    nongli_y = height * 0.52
    bazi_x = nongli_x
    bazi_y = nongli_y + 50
    li_x = nongli_x
    li_y = height * 0.72
    bi_x = nongli_x
    bi_y = li_y + 50

elif layout_type == "right":
    print("\n🎨 采用右侧布局策略：")
    print("  - 文字放在左侧")
    print("  - 左对齐或居中偏左")

    # 右侧布局：文字偏左
    date_day_size = int(height * 0.35)
    date_day_font = ImageFont.truetype(font_bold_path, date_day_size)

    date_day_bbox = draw.textbbox((0, 0), date_day, font=date_day_font)
    date_day_width = date_day_bbox[2] - date_day_bbox[0]
    date_day_x = width * 0.15  # 偏左
    date_day_y = height * 0.10

    month_week_x = width * 0.15
    month_week_y = date_day_y + date_day_bbox[3] + 25

    nongli_x = width * 0.15
    nongli_y = height * 0.52
    bazi_x = nongli_x
    bazi_y = nongli_y + 50
    li_x = nongli_x
    li_y = height * 0.72
    bi_x = nongli_x
    bi_y = li_y + 50

else:  # center or top
    print("\n🎨 采用居中布局策略：")
    print("  - 文字居中分布")
    print("  - 上下结构")

    date_day_bbox = draw.textbbox((0, 0), date_day, font=date_day_font)
    date_day_width = date_day_bbox[2] - date_day_bbox[0]
    date_day_height = date_day_bbox[3] - date_day_bbox[1]
    date_day_x = (width - date_day_width) // 2
    date_day_y = height * 0.10

    month_week_bbox = draw.textbbox((0, 0), month_week, font=month_week_font)
    month_week_width = month_week_bbox[2] - month_week_bbox[0]
    month_week_x = (width - month_week_width) // 2
    month_week_y = date_day_y + date_day_height + 25

    nongli_bbox = draw.textbbox((0, 0), nongli, font=nongli_font)
    nongli_width = nongli_bbox[2] - nongli_bbox[0]
    nongli_height = nongli_bbox[3] - nongli_bbox[1]
    nongli_x = (width - nongli_width) // 2
    nongli_y = height * 0.52

    bazi_bbox = draw.textbbox((0, 0), bazi, font=bazi_font)
    bazi_width = bazi_bbox[2] - bazi_bbox[0]
    bazi_height = bazi_bbox[3] - bazi_bbox[1]
    bazi_x = (width - bazi_width) // 2
    bazi_y = nongli_y + nongli_height + 35

    li_bbox = draw.textbbox((0, 0), li, font=li_bi_font)
    li_width = li_bbox[2] - li_bbox[0]
    li_height = li_bbox[3] - li_bbox[1]
    li_x = (width - li_width) // 2
    li_y = height * 0.72

    bi_bbox = draw.textbbox((0, 0), bi, font=li_bi_font)
    bi_width = bi_bbox[2] - bi_bbox[0]
    bi_height = bi_bbox[3] - bi_bbox[1]
    bi_x = (width - bi_width) // 2
    bi_y = li_y + li_height + 30

# 绘制文字（深棕色，有力度的颜色）
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
print("  设计特点：动态布局 + 块面结构 + 粗字体")
