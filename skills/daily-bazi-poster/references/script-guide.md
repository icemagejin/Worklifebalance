# 脚本说明 - poster_grouped.py

## 功能描述
现代设计海报生成器 - 微纹理背景版
生成超大数字 + 聚合日期信息的八字合盘海报

## 使用方法
```bash
python3 poster_grouped.py YYYY-MM-DD
```

## 输出
- 文件路径：`/workspace/projects/workspace-aesthetic/posters/poster-YYYY-MM-DD.jpg`
- 文件格式：JPG
- 尺寸：1080x1920
- 文件大小：约50KB

## 核心函数

### add_subtle_texture()
添加微妙的纹理效果，包含：
- 150个小圆点（随机分布）
- 20条细线（模拟纸张纹理）
- 智能避让文字区域

### 文字定位（关键）
```python
# 使用textbbox获取实际bottom位置
text_bbox = draw.textbbox((x, y), text, font=font)
actual_bottom = text_bbox[3]

# 下一行位置
next_y = actual_bottom + 80  # 80px间距
```

## 依赖库
- Pillow (PIL)
- datetime
- os
- random

## 字体要求
- 路径：`/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc`
- 类型：现代无衬线字体
- 格式：TTC

## 配置参数
| 参数 | 值 | 说明 |
|------|-----|------|
| width | 1080 | 画布宽度 |
| height | 1920 | 画布高度 |
| bg_color | (245, 243, 240) | 背景色（暖白） |
| text_color | (25, 25, 25) | 主文字颜色 |
| info_color | (100, 100, 100) | 副文字颜色 |
| date_day_size | height * 0.30 | 主数字字号 |
| date_info_size | width * 0.04 | 副标题字号 |

## 调试方法

### 查看生成日志
```bash
python3 poster_grouped.py 2026-04-04
# 输出：
# ✓ 微纹理背景已添加
# ✓ 字体加载成功
# ✓ 微纹理海报已生成：posters/poster-2026-04-04.jpg
```

### 检查文件
```bash
ls -lh /workspace/projects/workspace-aesthetic/posters/
```

### 查看图片
```bash
# 可以使用PIL查看
python3 -c "from PIL import Image; Image.open('posters/poster-2026-04-04.jpg').show()"
```

## 常见问题

### Q: 字体加载失败
A: 检查字体路径是否正确，字体文件是否存在

### Q: 文字重叠
A: 确保使用textbbox的bbox[3]作为下一行起点

### Q: 纹理太明显
A: 调整point_color和line_color，使其更接近背景色

### Q: 纹理不明显
A: 增加num_points和num_lines的值

## 优化方向
- 添加更多纹理变体
- 支持自定义配色方案
- 支持不同的字体风格
- 添加更多视觉元素（如边框、装饰线）
