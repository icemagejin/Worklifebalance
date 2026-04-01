#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont

# 创建测试图像
img = Image.new('RGB', (1000, 800), (255, 255, 255))
draw = ImageDraw.Draw(img)

font_path = "/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc"
font = ImageFont.truetype(font_path, 200)

date_day = "31"
month_week = "MAR TUE"

# 测试绘制
date_day_x = 100
date_day_y = 100

# 先绘制数字，获取它的实际 bounding box
draw.text((date_day_x, date_day_y), date_day, font=font, fill=(0, 0, 0))
date_day_bbox = draw.textbbox((date_day_x, date_day_y), date_day, font=font)

print(f"数字在 ({date_day_x}, {date_day_y}) 的 bounding box: {date_day_bbox}")
print(f"  实际 top: {date_day_bbox[1]}")
print(f"  实际 bottom: {date_day_bbox[3]}")
print(f"  实际高度: {date_day_bbox[3] - date_day_bbox[1]}")

# 月周应该在数字的 bottom 下方
margin = 30
month_week_x = 100
month_week_y = date_day_bbox[3] + margin

print(f"\n月周位置 y: {month_week_y} (数字 bottom {date_day_bbox[3]} + margin {margin})")

# 绘制月周
draw.text((month_week_x, month_week_y), month_week, font=font, fill=(255, 0, 0))

# 添加辅助线
draw.line([(0, date_day_bbox[3]), (1000, date_day_bbox[3])], fill=(0, 0, 255), width=2)
draw.line([(0, month_week_y), (1000, month_week_y)], fill=(0, 255, 0), width=2)

img.save("/tmp/test_text_overlap_v2.jpg")
print("\n测试图已保存到 /tmp/test_text_overlap_v2.jpg")
print("黑色：数字")
print("红色：月周")
print("蓝色线：数字底部")
print("绿色线：月周顶部")
