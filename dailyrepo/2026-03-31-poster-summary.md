# 2026-03-31 八字合盘海报制作总结

## 遇到的问题

### 1. 工作流不完整 ❌
- **问题**：跳过了 VL 分析步骤，直接生成海报
- **后果**：
  - 生成了方图（2048x2048）而不是竖图（1080x1920）
  - 没有分析背景图形位置
  - 无法智能避让图形
- **教训**：必须严格按照 HEARTBEAT.md 的完整工作流执行

### 2. 文字重叠问题 ❌
- **问题**：MAR TUE 叠在 31 下面
- **原因**：错误地使用 `y + height` 计算位置
- **正确的做法**：使用 `textbbox()` 的 `bbox[3]`（bottom）作为下一行的起点
```python
# 错误的做法
month_week_y = date_day_y + date_day_height

# 正确的做法
date_day_bbox = draw.textbbox((date_day_x, date_day_y), date_day, font=date_day_font)
month_week_y = date_day_bbox[3] + margin  # 使用 bbox[3]（bottom）
```

### 3. 表达不自然 ❌
- **问题**：副标题 "MAR TUE" 表达奇怪
- **改进**：改为中文 "3月31日 · 周二"
- **原因**：更符合中文表达习惯，信息更清晰

### 4. 排版层次不清晰 ❌
- **问题**：字号对比不够明显，间距不够合理
- **改进**：
  - 主日期：806px（height * 0.35）
  - 副标题：55px（width * 0.032）
  - 农历：~48px（width * 0.028）
  - 干支：~52px（width * 0.030）
  - 利弊：~45px（width * 0.026）
- **间距**：
  - 主日期与副标题：20px
  - 副标题与农历：拉开距离（height * 0.50）
  - 农历与干支：30px
  - 干支与利弊：根据位置动态调整

## 学到的经验

### 1. PIL 文字定位
```python
# 绘制文字前，先计算 bounding box
text_bbox = draw.textbbox((x, y), text, font=font)
# text_bbox 返回 (left, top, right, bottom)

# 计算下一行位置时，使用 bbox[3]（bottom）
next_y = text_bbox[3] + margin
```

### 2. 颜色层次
- 主日期：最深 (40, 25, 10) - 突出重点
- 副标题：稍浅 (70, 50, 30) - 次要信息
- 正文：中等 (65, 45, 25) - 辅助信息
- 利弊：稍深 (80, 55, 30) - 重要信息

### 3. 布局策略
- 根据 VL 分析结果动态调整
- 图形在底部 → 文字集中在顶部
- 图形在左侧 → 文字偏右
- 图形在右侧 → 文字偏左
- 始终保证留白充足

### 4. 验证方法
- 用像素差异检测文字区域
- 检测文字与图形的重叠比例
- 分析垂直分离距离
- 目标：重叠比例 < 15%

## 明天要做的改进

### 1. 严格遵守工作流
- [ ] 获取今日干支 + 宜忌
- [ ] 生成利弊对仗（6-8字，字数相等）
- [ ] 生成1080x1920竖版背景图
- [ ] **VL分析背景图形位置** ← 重要！
- [ ] 智能排版（避让图形）
- [ ] VL验证文字不重叠

### 2. 代码优化
- [ ] 整合工作流脚本，一键执行
- [ ] 自动验证脚本
- [ ] 参数化配置（字号、间距、颜色）

### 3. 设计优化
- [ ] 尝试不同的副标题格式
- [ ] 探索更多配色方案
- [ ] 优化留白比例

## 关键代码片段

### 正确的文字定位
```python
# 先计算 bounding box
text_bbox = draw.textbbox((x, y), text, font=font)

# 下一行使用 bbox[3]
next_y = text_bbox[3] + margin
```

### VL 分析布局
```python
# 分析背景图形分布
top_dark = np.sum(top_region < 200) / top_region.size * 100
middle_dark = np.sum(middle_region < 200) / middle_region.size * 100
bottom_dark = np.sum(bottom_region < 200) / bottom_region.size * 100

# 判断布局类型
if bottom_dark > 30:
    layout_type = "bottom"
    # 文字集中在顶部
```

### 智能排版
```python
if layout_type == "bottom":
    date_day_y = height * 0.08  # 顶部
    nongli_y = height * 0.50     # 中上部
    li_y = height * 0.68         # 中上部
    # 避开底部图形区域
```

## 总结

今天的问题主要在于：
1. 工作流不完整（跳过 VL 分析）
2. PIL API 使用错误（text 定位）
3. 设计细节不够（表达、层次、间距）

**核心教训**：
- 严格按照工作流执行，不能跳过步骤
- 理解 API 的正确用法（textbbox vs text）
- 注重设计细节（表达自然、层次清晰、间距合理）

**明天目标**：
- 严格按照完整工作流
- 使用正确的 PIL API
- 注重设计细节，每天进步一点
