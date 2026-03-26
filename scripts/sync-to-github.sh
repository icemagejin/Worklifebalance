#!/bin/bash
# 每两天同步八字合盘海报任务到 GitHub

set -e

echo "📅 开始同步八字合盘海报任务到 GitHub..."

# 配置 Git 用户信息（如果未配置）
git config --global user.email "aesthetic-agent@openclaw.ai" 2>/dev/null || true
git config --global user.name "Aesthetic Agent" 2>/dev/null || true

# 进入工作区
cd /workspace/projects/workspace-aesthetic

# 移除嵌入的 git 仓库（添加到 .gitignore）
if ! grep -q "skills/taste-skill" .gitignore 2>/dev/null; then
  echo "skills/taste-skill/" >> .gitignore
  git rm --cached -r skills/taste-skill 2>/dev/null || true
fi

# 添加所有更改
git add -A

# 获取当前时间
CURRENT_TIME=$(date +"%Y-%m-%d %H:%M")

# 提交
git commit -m "sync: 八字合盘海报任务及审美对齐记录 - ${CURRENT_TIME}" || echo "📝 没有新的更改"

# 推送到 GitHub
git push origin master 2>/dev/null || echo "⚠️ 推送失败（可能是网络或权限问题）"

echo "✅ 同步完成！"
echo "📊 提交时间：${CURRENT_TIME}"
