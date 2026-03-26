#!/bin/bash
# 生成 Aesthetics Agent 的美学日记

set -e

# 日期变量
DATE=$(date +%Y-%m-%d)
TIME=$(date +"%H:%M")
WEEKDAY_CN=$(date +%A | sed 's/Monday/周一/;s/Tuesday/周二/;s/Wednesday/周三/;s/Thursday/周四/;s/Friday/周五/;s/Saturday/周六/;s/Sunday/周日/')

# 日记目录
DIARY_DIR="/workspace/projects/workspace-aesthetic/diary/aesthetic-journal"
mkdir -p "$DIARY_DIR"

# 日记文件路径
DIARY_FILE="$DIARY_DIR/$DATE.md"

# 如果文件已存在，不重复生成
if [ -f "$DIARY_FILE" ]; then
  echo "📝 今日日记已存在：$DIARY_FILE"
  exit 0
fi

# 生成日记模板
cat > "$DIARY_FILE" << EOF
# 美学日记 - $DATE

**时间**：$TIME
**星期**：$WEEKDAY_CN
**Agent**：Aesthetics Designer 🎨

---

## 🎨 今日工作内容

- 完成的设计任务
- 参与的美学讨论
- 任何设计调整或优化

---

## 💡 今日美学感知

### 发现的美学元素
- 色彩搭配观察
- 布局设计思考
- 字体选择体会

### 设计灵感
- 从生活或作品中获得的美学启发
- 想要尝试的设计风格
- 对现有设计的改进想法

---

## 🖼️ 创作记录

如果今天创作了海报或图片：
- 作品名称
- 设计思路
- 使用的设计元素
- 满意度评分（1-5分）

---

## 📚 学习与成长

- 学到的设计技巧
- 提升的审美能力
- 需要改进的地方

---

## 🌟 今日感悟

一段关于美学的思考或感悟，可以是：
- 对美的理解
- 对设计的思考
- 对艺术的感受
- 对生活的美学观察

---

## 📌 明日计划

- 计划完成的设计任务
- 想要尝试的美学方向
- 需要关注的审美问题

---

**标签**：#美学日记 #Aesthetics #设计感悟
EOF

echo "✅ 美学日记已生成：$DIARY_FILE"
echo "📅 日期：$DATE"
echo "🎨 路径：$DIARY_DIR"
