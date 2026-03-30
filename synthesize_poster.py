from PIL import Image, ImageDraw, ImageFont

bg_path = "bg-new.jpg"
img = Image.open(bg_path)
width, height = img.size

draw = ImageDraw.Draw(img, 'RGBA')
overlay = Image.new('RGBA', (width, height), (255, 255, 255, 140))
img_with_overlay = Image.alpha_composite(img.convert('RGBA'), overlay)
draw = ImageDraw.Draw(img_with_overlay, 'RGBA')

font_path = "/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc"

month_week = "MAR SAT"
date_main = "28"
nongli = "二月初十"
bazi = "丙午 · 辛卯 · 辛丑"
jingyu = "火旺收敛静守"
fuyu = "木柔扶持兴旺"

# 字号
month_week_font = ImageFont.truetype(font_path, 42)
date_main_font = ImageFont.truetype(font_path, 200)
nongli_font = ImageFont.truetype(font_path, 38)
bazi_font = ImageFont.truetype(font_path, 48)
jing_fu_font = ImageFont.truetype(font_path, 34)

# 计算位置
current_y = height * 0.12

# 1. 英文月周
month_week_bbox = draw.textbbox((0, 0), month_week, font=month_week_font)
month_week_width = month_week_bbox[2] - month_week_bbox[0]
month_week_height = month_week_bbox[3] - month_week_bbox[1]
month_week_x = (width - month_week_width) // 2
month_week_y = current_y
current_y = month_week_y + month_week_height + 60

# 2. 主日期
date_main_bbox = draw.textbbox((0, 0), date_main, font=date_main_font)
date_main_width = date_main_bbox[2] - date_main_bbox[0]
date_main_height = date_main_bbox[3] - date_main_bbox[1]
date_main_x = (width - date_main_width) // 2
date_main_y = current_y
current_y = date_main_y + date_main_height + 120

# 3. 农历
nongli_bbox = draw.textbbox((0, 0), nongli, font=nongli_font)
nongli_width = nongli_bbox[2] - nongli_bbox[0]
nongli_height = nongli_bbox[3] - nongli_bbox[1]
nongli_x = (width - nongli_width) // 2
nongli_y = current_y
current_y = nongli_y + nongli_height + 80

# 4. 八字
bazi_bbox = draw.textbbox((0, 0), bazi, font=bazi_font)
bazi_width = bazi_bbox[2] - bazi_bbox[0]
bazi_height = bazi_bbox[3] - bazi_bbox[1]
bazi_x = (width - bazi_width) // 2
bazi_y = current_y

# 5. 警语福语 - 去掉emoji，改用简洁符号
jingyu_x = (width - draw.textbbox((0,0), "警语：" + jingyu, font=jing_fu_font)[2]) // 2
jingyu_y = height * 0.84

fuyu_x = (width - draw.textbbox((0,0), "福语：" + fuyu, font=jing_fu_font)[2]) // 2
fuyu_y = jingyu_y + 65

# 绘制
info_color = (85, 55, 30, 255)

draw.text((month_week_x, month_week_y), month_week, font=month_week_font, fill=info_color)
draw.text((date_main_x, date_main_y), date_main, font=date_main_font, fill=(65, 40, 18, 255))
draw.text((nongli_x, nongli_y), nongli, font=nongli_font, fill=info_color)
draw.text((bazi_x, bazi_y), bazi, font=bazi_font, fill=info_color)

draw.text((jingyu_x, jingyu_y), "警语：" + jingyu, font=jing_fu_font, fill=(135, 90, 50, 255))
draw.text((fuyu_x, fuyu_y), "福语：" + fuyu, font=jing_fu_font, fill=(155, 110, 70, 255))

img_with_overlay.convert('RGB').save("poster-2026-03-28-final.jpg", quality=95)

print("去掉emoji，改用文字标记")
