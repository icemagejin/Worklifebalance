#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont

# 创建测试图像
img = Image.new('RGB', (1000, 1000), (255, 255, 255))
draw = ImageDraw.Draw(img)

font_path = "/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc"
font = ImageFont.truetype(font_path, 200)

date_day = "31"
month_week = "MAR TUE"

# 计算bounding box
date_day_bbox = draw.textbbox((0, 0), date_day, font=font)
print(f"数字'31'的bounding box: {date_day_bbox}")
print(f"  宽度: {date_day_bbox[2] - date_day_bbox[0]}")
print(f"  高度: {date_day_bbox[3] - date_day_bbox[1]}")

# 计算实际高度（bottom - top）
date_day_height = date_day_bbox[3] - date_day_bbox[1]
print(f"\n实际高度: {date_day_height}")

# 注意：textbbox 返回的是 (left, top, right, bottom)
# text() 的 y 参数是 bounding box 的 top
# 所以要放在数字下方，应该是 y = date_day_y + date_day_height

# 测试两种方式
date_day_y = 100

# 方式1：直接 + height
month_week_y_v1 = date_day_y + date_day_height

# 方式2：使用 textbbox 的 bottom 作为起点
month_week_y_v2 = date_day_bbox[3] + 20

print(f"\n数字位置 y: {date_day_y}")
print(f"方式1（+ height）月周位置 y: {month_week_y_v1}")
print(f"方式2（使用bbox bottom）月周位置 y: {month_week_y_v2}")

# 绘制测试
draw.text((50, date_day_y), date_day, font=font, fill=(0, 0, 0))
draw.text((50, month_week_y_v1), month_week, font=font, fill=(255, 0, 0))

img.save("/tmp/test_text_overlap.jpg")
print("\n测试图已保存到 /tmp/test_text_overlap.jpg")
print("黑色是数字，红色是月周（方式1）")
