---
name: daily-bazi-poster
description: 每日八字合盘海报生成技能。自动生成今日八字合盘海报，包含干支计算、宜忌生成、微纹理背景设计和飞书群聊发送。适用于需要每日定时发送美学海报的场景。
---

# 每日八字合盘海报生成

## 触发条件

当用户要求：
- "生成今日八字海报"
- "做每日八字合盘"
- "发送八字海报"
- 或定时任务触发（每天08:15）

## 完整工作流程

### 步骤1：获取今日日期信息

```python
from datetime import datetime

# 获取今日日期
date_str = datetime.now().strftime("%Y-%m-%d")
year = datetime.now().year
month = datetime.now().month
day = datetime.now().day
weekday = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"][datetime.now().weekday()]
```

### 步骤2：生成海报（使用poster_grouped.py脚本）

```bash
# 生成海报
python3 /workspace/projects/workspace-aesthetic/poster_grouped.py YYYY-MM-DD
```

**脚本特点**：
- 超大数字（height * 0.30）作为视觉焦点
- 完整日期信息聚合在数字下方
- 微纹理背景（150个小圆点 + 20条细线）
- 暖白背景色 (245, 243, 240)
- 智能文字避让，无重叠

**输出路径**：`/workspace/projects/workspace-aesthetic/posters/poster-YYYY-MM-DD.jpg`

### 步骤3：发送到飞书群聊

```python
# 使用message工具发送图片
message(
    action="send",
    channel="feishu",
    media="/workspace/projects/workspace-aesthetic/posters/poster-YYYY-MM-DD.jpg"
)
```

**目标群聊**：`oc_95076f564f595dc80ae416c8221ad806`（美学群）

### 步骤4：记录到日记

```bash
# 记录到memory/YYYY-MM-DD.md
# 记录内容：任务完成情况、时间、设计要点、遇到的问题
```

## 设计规范

### 色彩方案
- 背景色：(245, 243, 240) - 暖白
- 纹理色：(235, 233, 230) - 比背景稍深
- 主数字：(25, 25, 25) - 超深色
- 日期信息：(100, 100, 100) - 中灰色

### 字体配置
- 字体：Noto Sans Regular（现代无衬线）
- 主数字字号：height * 0.30
- 日期信息字号：width * 0.04

### 布局策略
- 超大数字居中（y = height * 0.25）
- 日期信息居中，在数字下方
- 使用textbbox实际bottom位置，避免重叠
- 间距：80px

### 微纹理配置
- 150个小圆点（半径2px）
- 20条细线（几乎水平）
- 智能避让文字区域（15%-60%高度不放置纹理）

## 技术要点

### 文字定位（重要！）

```python
# 错误做法 ❌
next_y = y + height  # 会导致文字重叠

# 正确做法 ✅
text_bbox = draw.textbbox((x, y), text, font=font)
next_y = text_bbox[3] + margin  # 使用实际bottom位置
```

## 定时任务配置

### Cron表达式
```json
{
  "schedule": {
    "expr": "15 8 * * *",  // 每天8:15（上海时间）
    "kind": "cron",
    "tz": "Asia/Shanghai"
  }
}
```

### Cron配置文件
路径：`/workspace/projects/workspace-aesthetic/cron/jobs.json`

## 文件结构

```
/workspace/projects/workspace-aesthetic/
├── poster_grouped.py          # 海报生成脚本
├── posters/
│   └── poster-YYYY-MM-DD.jpg  # 输出海报
├── memory/
│   └── YYYY-MM-DD.md          # 每日记录
├── HEARTBEAT.md               # 工作流文档
└── cron/
    └── jobs.json              # 定时任务配置
```

## 注意事项

### 主动执行
- 在群聊中，收到heartbeat prompt时应主动检查并执行任务
- 不要等待用户提醒，要有自我驱动的任务管理意识

### 验证检查
- 生成海报后，必须检查图片质量
- 确认文字不重叠
- 确认背景纹理正常

### 错误处理
- 如果脚本失败，检查字体路径
- 如果发送失败，检查chat_id和权限
- 如果文件不存在，检查路径和权限

## 历史优化

### 2026-04-04 微纹理方案
- 添加微纹理背景（150个小圆点 + 20条细线）
- 修复文字重叠bug（使用textbbox实际bottom位置）
- 更新发送时间：9:10 -> 8:15

### 2026-03-31 工作流优化
- PIL文字定位bug修复
- 表达优化（英文 -> 中文副标题）
- 完整工作流文档

## 参考资料

- HEARTBEAT.md：`/workspace/projects/workspace-aesthetic/HEARTBEAT.md`
- poster_grouped.py：`/workspace/projects/workspace-aesthetic/poster_grouped.py`
- Cron配置：`/workspace/projects/workspace-aesthetic/cron/jobs.json`

---

_Aesthetics Designer | 每日八字合盘海报技能_
