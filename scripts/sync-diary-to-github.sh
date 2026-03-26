#!/bin/bash
# 将美学日记同步到 GitHub 的 dailyrepo 文件夹

set -e

echo "📅 开始同步美学日记到 GitHub dailyrepo..."

# 配置 Git 用户信息
git config --global user.email "aesthetic-agent@openclaw.ai" 2>/dev/null || true
git config --global user.name "Aesthetic Agent" 2>/dev/null || true

# 进入工作区
cd /workspace/projects/workspace-aesthetic

# 确保 dailyrepo 目录存在
mkdir -p dailyrepo/aesthetic-journal

# 复制今天的日记到 dailyrepo/aesthetic-journal
TODAY=$(date +%Y-%m-%d)
DIARY_FILE="diary/aesthetic-journal/$TODAY.md"

if [ -f "$DIARY_FILE" ]; then
  cp "$DIARY_FILE" "dailyrepo/aesthetic-journal/"
  echo "✅ 已复制今日日记到 dailyrepo/aesthetic-journal/"
else
  echo "⚠️ 今日日记不存在，跳过复制"
fi

# 添加所有更改
git add -A

# 获取当前时间
CURRENT_TIME=$(date +"%Y-%m-%d %H:%M")

# 提交
git commit -m "sync: 美学日记同步 - ${CURRENT_TIME}" || echo "📝 没有新的更改"

# 推送到 GitHub
git push origin master 2>/dev/null || echo "⚠️ 推送失败（可能是网络或权限问题）"

echo "✅ 同步完成！"
echo "📊 提交时间：${CURRENT_TIME}"
