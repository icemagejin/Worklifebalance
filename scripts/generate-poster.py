from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import os

# 创建画布 (iPhone尺寸)
width, height = 1080, 1920

# 加载生成的背景图
background_path = '/workspace/projects/workspace-aesthetic/posters/background-2026-03-26-v2.jpg'
background = Image.open(background_path)

# 检查背景图尺寸
bg_width, bg_height = background.size
print(f"背景图尺寸: {bg_width}x{bg_height}")

# 智能裁剪背景图到海报比例
poster_ratio = width / height
bg_ratio = bg_width / bg_height

if bg_ratio > poster_ratio:
    # 背景更宽，裁剪左右
    new_height = bg_height
    new_width = int(new_height * poster_ratio)
    left = (bg_width - new_width) // 2
    background = background.crop((left, 0, left + new_width, bg_height))
else:
    # 背景更高，裁剪上下
    new_width = bg_width
    new_height = int(new_width / poster_ratio)
    top = (bg_height - new_height) // 2
    background = background.crop((0, top, bg_width, top + new_height))

# 调整尺寸到海报尺寸
background = background.resize((width, height), Image.LANCZOS)

# 创建半透明白色遮罩，让文字更清晰
image = background.copy()
overlay = Image.new('RGBA', (width, height), (255, 255, 255, 80))
image.paste(overlay, (0, 0), overlay)
image = image.convert('RGB')

draw = ImageDraw.Draw(image)

# 使用中文字体，创建粗细对比
try:
    # 使用 Bold 字体作为大数字（粗）
    large_font = ImageFont.truetype("/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc", 480, index=0)
    print("✅ 使用 Noto Sans CJK Bold (大数字 - 粗体)")

    # 使用 Serif Regular 字体作为祝福语和干支（细体优雅）
    serif_font = ImageFont.truetype("/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc", 48, index=0)
    print("✅ 使用 Noto Serif CJK Regular (祝福语 - 细体优雅)")

    # 使用 Sans Regular 字体作为英文日期
    regular_font = ImageFont.truetype("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc", 36, index=0)
    print("✅ 使用 Noto Sans CJK Regular (日期)")

except Exception as e:
    print(f"❌ 无法加载中文字体: {e}")
    # 降级到默认字体
    large_font = ImageFont.load_default()
    serif_font = ImageFont.load_default()
    regular_font = ImageFont.load_default()

# 绘制超大数字 26（粗体 Sans）
draw.text((width // 2, 600), '26', fill='#1a1a1a', font=large_font, anchor='mm')

# 绘制极小字日期（常规 Sans）
draw.text((width // 2, 900), 'MARCH THURSDAY', fill='#666666', font=regular_font, anchor='mm')

# 绘制极小字干支（细体 Serif）
draw.text((width // 2, 950), '丙午·甲午', fill='#666666', font=serif_font, anchor='mm')

# 绘制对仗祝福语（细体 Serif）
blessing_1 = '丙火生辉开好运'
blessing_2 = '甲午得福展宏图'

# 居中绘制
draw.text((width // 2, 1300), blessing_1, fill='#1a1a1a', font=serif_font, anchor='mm')
draw.text((width // 2, 1370), blessing_2, fill='#1a1a1a', font=serif_font, anchor='mm')

# 保存高质量图片
output_path = '/workspace/projects/workspace-aesthetic/posters/poster-2026-03-26-final.png'
image.save(output_path, quality=95, optimize=True)

print(f"✅ 海报已生成：{output_path}")
print(f"📅 日期：2026-03-26")
print(f"🎨 主题：丙午甲午 - 火木相生")
print(f"📐 尺寸：{width}x{height}")
print(f"✨ 字体组合：Sans Bold(数字) + Serif Regular(祝福/干支) + Sans Regular(日期)")
