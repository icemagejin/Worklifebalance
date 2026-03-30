#!/bin/bash
# 同步美学日记到 GitHub

set -e

WORKSPACE="/workspace/projects/workspace-aesthetic"
DAILYREPO="$WORKSPACE/dailyrepo/aesthetic-journal"
MEMORY_DIR="$WORKSPACE/memory"
GITHUB_TOKEN="${GITHUB_TOKEN:-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}"

# 进入目标目录
cd "$DAILYREPO"

# 检查是否有 Git 仓库
if [ ! -d ".git" ]; then
    echo "[$(date)] 初始化 Git 仓库..."
    git init
    git branch -M master
    git remote add origin https://github.com/icemagejin/dailyrepo.git
fi

# 配置Git用户信息
git config user.email "aesthetic-agent@openclaw.ai" 2>/dev/null || true
git config user.name "Aesthetics Agent" 2>/dev/null || true

# 确保远程URL包含token（如果环境变量中有token）
if [ -n "$GITHUB_TOKEN" ]; then
    REMOTE_URL=$(git remote get-url origin 2>/dev/null || echo "")
    if [[ ! "$REMOTE_URL" =~ ^https://ghp_ ]]; then
        REMOTE_URL_WITH_TOKEN=$(echo "$REMOTE_URL" | sed "s|https://github.com/|https://${GITHUB_TOKEN}@github.com/|")
        git remote set-url origin "$REMOTE_URL_WITH_TOKEN"
    fi
fi

# 同步今天的日记
DATE=$(date +%Y-%m-%d)
MEMORY_FILE="$MEMORY_DIR/$DATE.md"

if [ -f "$MEMORY_FILE" ]; then
    cp "$MEMORY_FILE" "$DAILYREPO/$DATE.md"

    # 添加文件
    git add .

    # 检查是否有变更
    if git diff --cached --quiet; then
        echo "[$(date)] 没有新的变更，无需提交"
        exit 0
    fi

    # 提交、推送
    git commit -m "sync: 美学日记同步 - $DATE $(date +%H:%M)"
    git push origin master

    echo "[$(date)] ✅ 美学日记已同步到 GitHub: $DATE.md"
else
    echo "[$(date)] ⚠️  今天的美学日记不存在: $MEMORY_FILE"
fi
