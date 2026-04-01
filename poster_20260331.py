#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont
import os

# 配置
bg_path = "/workspace/projects/workspace-aesthetic/posters/background_2026-03-31.jpg"
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

# 半透明白色遮罩
draw = ImageDraw.Draw(img, 'RGBA')
overlay = Image.new('RGBA', (width, height), (255, 255, 255, 100))
img_with_overlay = Image.alpha_composite(img.convert('RGBA'), overlay)
draw = ImageDraw.Draw(img_with_overlay, 'RGBA')

# 字体路径
font_bold_path = "/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc"
font_regular_path = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"

# 动态字号计算
# 超大数字占画面 30-40%，动态调整
date_day_size = int(height * 0.38)

# 根据内容长度动态调整其他字号
month_week_size = 50
nongli_size = 42
bazi_size = 48
li_bi_size = 40

# 加载字体（使用粗体字体，有力度的字体）
try:
    date_day_font = ImageFont.truetype(font_bold_path, date_day_size)
    month_week_font = ImageFont.truetype(font_regular_path, month_week_size)
    nongli_font = ImageFont.truetype(font_regular_path, nongli_size)
    bazi_font = ImageFont.truetype(font_regular_path, bazi_size)
    li_bi_font = ImageFont.truetype(font_regular_path, li_bi_size)
except Exception as e:
    print(f"字体加载失败：{e}，使用默认字体")
    date_day_font = ImageFont.load_default()
    month_week_font = ImageFont.load_default()
    nongli_font = ImageFont.load_default()
    bazi_font = ImageFont.load_default()
    li_bi_font = ImageFont.load_default()

# 块面结构
# 上半块面：超大数字 + 月周
# 中间块面：农历 + 干支
# 下半块面：利弊

# 1. 上半块面 - 超大数字
date_day_bbox = draw.textbbox((0, 0), date_day, font=date_day_font)
date_day_width = date_day_bbox[2] - date_day_bbox[0]
date_day_height = date_day_bbox[3] - date_day_bbox[1]
date_day_x = (width - date_day_width) // 2
date_day_y = height * 0.08

# 2. 上半块面 - 月周（在数字上方）
month_week_bbox = draw.textbbox((0, 0), month_week, font=month_week_font)
month_week_width = month_week_bbox[2] - month_week_bbox[0]
month_week_height = month_week_bbox[3] - month_week_bbox[1]
month_week_x = (width - month_week_width) // 2
month_week_y = date_day_y + date_day_height + 30

# 3. 中间块面 - 农历（偏左，形成块面）
nongli_bbox = draw.textbbox((0, 0), nongli, font=nongli_font)
nongli_width = nongli_bbox[2] - nongli_bbox[0]
nongli_height = nongli_bbox[3] - nongli_bbox[1]
nongli_x = width * 0.15  # 偏左
nongli_y = height * 0.65

# 4. 中间块面 - 干支（在农历下方）
bazi_bbox = draw.textbbox((0, 0), bazi, font=bazi_font)
bazi_width = bazi_bbox[2] - bazi_bbox[0]
bazi_height = bazi_bbox[3] - bazi_bbox[1]
bazi_x = nongli_x  # 与农历左对齐
bazi_y = nongli_y + nongli_height + 40

# 5. 下半块面 - 利弊（偏右，与左侧形成对比）
li_bbox = draw.textbbox((0, 0), li, font=li_bi_font)
li_width = li_bbox[2] - li_bbox[0]
li_height = li_bbox[3] - li_bbox[1]
li_x = width * 0.15  # 偏左
li_y = height * 0.82

bi_bbox = draw.textbbox((0, 0), bi, font=li_bi_font)
bi_width = bi_bbox[2] - bi_bbox[0]
bi_height = bi_bbox[3] - bi_bbox[1]
bi_x = li_x  # 与利左对齐
bi_y = li_y + li_height + 35

# 绘制文字
info_color = (60, 40, 20, 255)  # 深棕色，有力度的颜色
highlight_color = (40, 25, 10, 255)  # 更深的颜色用于强调

# 绘制
draw.text((date_day_x, date_day_y), date_day, font=date_day_font, fill=highlight_color)
draw.text((month_week_x, month_week_y), month_week, font=month_week_font, fill=info_color)
draw.text((nongli_x, nongli_y), nongli, font=nongli_font, fill=info_color)
draw.text((bazi_x, bazi_y), bazi, font=bazi_font, fill=info_color)
draw.text((li_x, li_y), li, font=li_bi_font, fill=(90, 60, 35, 255))
draw.text((bi_x, bi_y), bi, font=li_bi_font, fill=(90, 60, 35, 255))

# 保存
img_with_overlay.convert('RGB').save(output_path, quality=95)

print(f"海报已生成：{output_path}")
print(f"文件大小：{os.path.getsize(output_path) / 1024 / 1024:.2f} MB")
print("设计特点：块面结构 + 粗黑体 + 动态字号")
