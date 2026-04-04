# 调试指南 - Daily Bazi Poster

## 问题诊断流程

### 1. 脚本执行失败

#### 症状：脚本报错，无法生成海报

**检查步骤**：
```bash
# 1. 检查脚本是否存在
ls -la /workspace/projects/workspace-aesthetic/poster_grouped.py

# 2. 检查Python环境
python3 --version

# 3. 检查依赖库
python3 -c "from PIL import Image, ImageDraw, ImageFont; print('PIL OK')"

# 4. 检查字体
ls -la /usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc

# 5. 尝试执行脚本（带调试信息）
python3 -u poster_grouped.py 2026-04-04
```

**常见原因**：
- 脚本路径错误 → 使用绝对路径
- 字体缺失 → 安装Noto字体或修改字体路径
- PIL未安装 → `pip install pillow`
- 权限问题 → 检查文件读写权限

---

### 2. 文字重叠

#### 症状：数字"4"底下盖住了"4月4日·周六·2026"

**检查代码**：
```python
# 错误做法 ❌
date_info_y = date_day_y + date_day_height + 60

# 正确做法 ✅
date_day_rendered_bbox = draw.textbbox((date_day_x, date_day_y), date_day, font=date_day_font)
date_day_actual_bottom = date_day_rendered_bbox[3]
date_info_y = date_day_actual_bottom + 80  # 使用实际bottom位置
```

**验证方法**：
1. 生成海报后查看图片
2. 检查数字和副标题是否有重叠
3. 如果重叠，检查是否使用了textbbox

---

### 3. 纯色背景（无纹理）

#### 症状：背景是纯色，没有小圆点和细线

**检查代码**：
```python
# 确保调用了纹理函数
add_subtle_texture(img, draw)

# 检查纹理参数
point_color = (235, 233, 230)  # 应该比背景色稍深
line_color = (240, 238, 235)   # 应该比背景色稍深
```

**验证方法**：
1. 放大查看图片四周
2. 检查是否有小圆点
3. 检查是否有细微的线条
4. 如果看不见，调整颜色使其更明显

---

### 4. 发送失败

#### 症状：海报生成成功，但发送到飞书失败

**检查步骤**：
```python
# 1. 检查文件是否存在
import os
print(os.path.exists("/workspace/projects/workspace-aesthetic/posters/poster-2026-04-04.jpg"))

# 2. 检查文件大小
print(os.path.getsize("/workspace/projects/workspace-aesthetic/posters/poster-2026-04-04.jpg"))

# 3. 测试message工具
message(action="send", channel="feishu", media="/path/to/image.jpg")
```

**常见原因**：
- 文件路径错误 → 使用绝对路径
- 文件不存在 → 先生成海报
- 文件损坏 → 重新生成
- 飞书权限问题 → 检查应用权限配置
- chat_id错误 → 确认目标群聊ID

---

### 5. 定时任务不执行

#### 症状：到了指定时间，任务没有自动执行

**检查步骤**：
```bash
# 1. 检查cron配置
cat /workspace/projects/workspace-aesthetic/cron/jobs.json

# 2. 检查任务是否启用
# 查看 "enabled": true

# 3. 检查时间表达式
# "expr": "15 8 * * *"  表示每天8:15

# 4. 检查时区
# "tz": "Asia/Shanghai"
```

**常见原因**：
- 任务被禁用 → 设置 `enabled: true`
- 时间表达式错误 → 检查cron语法
- 时区错误 → 确认时区设置
- 系统时间错误 → 检查系统时间

---

### 6. 图片质量差

#### 症状：生成的海报模糊、失真、颜色异常

**检查步骤**：
```python
# 1. 检查保存质量
img.save(output_path, quality=95)  # 确保quality=95

# 2. 检查图片尺寸
width, height = img.size
print(f"尺寸: {width}x{height}")  # 应该是1080x1920

# 3. 检查颜色模式
print(img.mode)  # 应该是RGB
```

**常见原因**：
- 保存质量低 → 设置quality=95
- 尺寸错误 → 检查width和height配置
- 颜色模式错误 → 确保是RGB模式
- 字体渲染问题 → 检查字体是否正确加载

---

## 调试技巧

### 查看完整错误信息
```bash
python3 -u poster_grouped.py 2026-04-04 2>&1 | tee debug.log
```

### 分步调试
```python
# 在脚本中添加调试输出
print(f"调试：字体路径 = {font_path}")
print(f"调试：字体加载 = {date_day_font}")
print(f"调试：数字位置 = {date_day_x}, {date_day_y}")
print(f"调试：实际bottom = {date_day_actual_bottom}")
```

### 可视化调试
```python
# 绘制辅助线
draw.line([(0, date_day_y), (width, date_day_y)], fill=(255, 0, 0), width=2)  # 数字顶部红线
draw.line([(0, date_day_actual_bottom), (width, date_day_actual_bottom)], fill=(0, 255, 0), width=2)  # 数字底部绿线
draw.line([(0, date_info_y), (width, date_info_y)], fill=(0, 0, 255), width=2)  # 副标题顶部蓝线
```

---

## 性能优化

### 加速生成
```python
# 使用更少的纹理点
num_points = 100  # 原值150
num_lines = 15    # 原值20
```

### 减小文件大小
```python
# 降低保存质量
img.save(output_path, quality=85)  # 原值95
```

---

## 常用命令

### 快速生成
```bash
python3 poster_grouped.py $(date +%Y-%m-%d)
```

### 批量生成
```bash
for day in {1..30}; do
  python3 poster_grouped.py 2026-04-$(printf "%02d" $day)
done
```

### 清理旧海报
```bash
find /workspace/projects/workspace-aesthetic/posters/ -name "poster-*.jpg" -mtime +30 -delete
```

---

## 获取帮助

如果遇到以上问题都无法解决：
1. 查看SKILL.md的完整文档
2. 查看references/下的参考文档
3. 检查memory/下的历史记录
4. 联系开发者

---

_调试指南 | Daily Bazi Poster_
