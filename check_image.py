from PIL import Image
import os

output_path = "poster-2026-03-28.jpg"
img = Image.open(output_path)
width, height = img.size

print(f"图片尺寸：{width}x{height}")
file_size = os.path.getsize(output_path)
print(f"文件大小：{file_size / 1024:.2f} KB")

# 检查文字区域
text_area = img.crop((0, 0, width, int(height * 0.4)))
pixels = list(text_area.getdata())
dark_pixels = sum(1 for pixel in pixels if sum(pixel[:3]) < 600)

print(f"深色像素：{dark_pixels} / {len(pixels)} ({dark_pixels/len(pixels)*100:.1f}%)")

if dark_pixels < 100:
    print("警告：深色像素很少，文字可能没有被正确合成！")
else:
    print("文字已合成")
