#!/bin/bash
#
# GitHub 备份脚本 - 八字合盘海报工作流
# 同步工作流文档、脚本、配置到 GitHub
#

set -e

# 工作区路径
WORKSPACE="/workspace/projects/workspace-aesthetic"

# GitHub 仓库路径（需要配置）
GITHUB_REPO="${GITHUB_REPO:-your-username/workspace-aesthetic}"

# 日志函数
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

# 检查是否在 Git 仓库中
check_git_repo() {
    cd "$WORKSPACE"
    if ! git rev-parse --git-dir > /dev/null 2>&1; then
        log "❌ 不是 Git 仓库，初始化..."
        git init
        git config user.name "Aesthetics Agent"
        git config user.email "aesthetic@openclaw.ai"
    fi
}

# 添加文件到 Git
add_files() {
    cd "$WORKSPACE"

    log "📦 添加工作流文件..."

    # 工作流文档
    git add WORKFLOW.md
    git add docs/font-strategy.md
    git add docs/vl-implementation-plan.md

    # 脚本
    git add scripts/poster_template_fd_v2.py
    git add scripts/poster_template_serif.py
    git add scripts/poster_template_fd.py
    git add scripts/vl_validator.py
    git add check_image.py

    # Cron 配置
    git add cron/jobs.json

    # 记忆文件
    git add memory/

    # README
    if [ -f README.md ]; then
        git add README.md
    fi

    # 标识文件
    if [ -f SOUL.md ]; then
        git add SOUL.md
    fi
    if [ -f USER.md ]; then
        git add USER.md
    fi
    if [ -f IDENTITY.md ]; then
        git add IDENTITY.md
    fi
    if [ -f TOOLS.md ]; then
        git add TOOLS.md
    fi

    log "✅ 文件已添加到 Git"
}

# 提交更改
commit_changes() {
    cd "$WORKSPACE"

    # 检查是否有更改
    if git diff --staged --quiet; then
        log "ℹ️  没有更改需要提交"
        return
    fi

    # 提交
    COMMIT_MSG="📦 备份八字合盘海报工作流 ($(date '+%Y-%m-%d %H:%M'))"
    git commit -m "$COMMIT_MSG"

    log "✅ 更改已提交"
}

# 推送到 GitHub
push_to_github() {
    cd "$WORKSPACE"

    # 检查是否配置了远程仓库
    if ! git remote get-url origin > /dev/null 2>&1; then
        log "⚠️  未配置远程仓库"
        log "💡 请运行: git remote add origin https://github.com/${GITHUB_REPO}.git"
        return
    fi

    # 推送
    log "📤 推送到 GitHub..."
    git push origin main || git push origin master || {
        log "⚠️  推送失败，尝试强制推送..."
        git push -f origin main || git push -f origin master
    }

    log "✅ 已推送到 GitHub"
}

# 主函数
main() {
    log "🚀 开始 GitHub 备份..."

    check_git_repo
    add_files
    commit_changes
    push_to_github

    log "🎉 GitHub 备份完成！"
}

# 执行
main
