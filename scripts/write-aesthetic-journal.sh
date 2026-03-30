#!/bin/bash
# 美学日记生成脚本

WORKSPACE="/workspace/projects/workspace-aesthetic"
DATE=$(date +%Y-%m-%d)
MEMORY_DIR="$WORKSPACE/memory"
MEMORY_FILE="$MEMORY_DIR/$DATE.md"

# 创建 memory 目录（如果不存在）
mkdir -p "$MEMORY_DIR"

# 检查今天的日记是否已存在
if [ -f "$MEMORY_FILE" ]; then
    echo "[$(date)] 美学日记已存在: $MEMORY_FILE"
    exit 0
fi

# 生成美学日记模板
cat > "$MEMORY_FILE" << EOF
# 🎨 美学日记 - $DATE

## 今日创作

_今天完成了什么视觉创作任务？_

---

## 创作思考

_我对今天创作的反思：_
- _什么做得好？_
- _什么需要改进？_
- _遇到了什么挑战？_

---

## 审美对齐

_与弗尼的审美对齐思考：_
- _今天我是否准确理解了需求？_
- _有没有偏离预期的地方？原因是什么？_
- _从弗尼的反馈中学到了什么？_
- _如何更好地理解"极简 水墨 诧寂风"这种美学风格？_

---

## 明日改进计划

_基于今天的经验，明天我会：_
1. _
2. _
3. _

---
EOF

echo "[$(date)] ✅ 美学日记已创建: $MEMORY_FILE"

