#!/bin/bash
# 同步美学日记到 Notion

set -e

# 配置
NOTION_API_KEY="${NOTION_API_KEY:-}"
NOTION_DATABASE_ID="${NOTION_DATABASE_ID:-}"

# 检查配置
if [ -z "$NOTION_API_KEY" ] || [ -z "$NOTION_DATABASE_ID" ]; then
  echo "❌ 未配置 Notion API"
  echo "请设置环境变量："
  echo "  export NOTION_API_KEY=your_api_key"
  echo "  export NOTION_DATABASE_ID=your_database_id"
  exit 1
fi

# 日期
DATE=$(date +%Y-%m-%d)

# 日记文件路径
DIARY_FILE="/workspace/projects/workspace-aesthetic/diary/aesthetic-journal/$DATE.md"

# 检查文件是否存在
if [ ! -f "$DIARY_FILE" ]; then
  echo "❌ 日记文件不存在：$DIARY_FILE"
  exit 1
fi

# 读取日记内容
DIARY_CONTENT=$(cat "$DIARY_FILE")

# 提取标题（第一行）
TITLE=$(head -n 1 "$DIARY_FILE" | sed 's/# //')

# 使用 Notion API 创建页面
curl -s -X POST "https://api.notion.com/v1/pages" \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Content-Type: application/json" \
  -H "Notion-Version: 2022-06-28" \
  -d "{
    \"parent\": {
      \"database_id\": \"$NOTION_DATABASE_ID\"
    },
    \"properties\": {
      \"Name\": {
        \"title\": [
          {
            \"text\": {
              \"content\": \"$TITLE\"
            }
          }
        ]
      },
      \"Date\": {
        \"date\": {
          \"start\": \"$DATE\"
        }
      }
    },
    \"children\": [
      {
        \"object\": \"block\",
        \"type\": \"paragraph\",
        \"paragraph\": {
          \"rich_text\": [
            {
              \"type\": \"text\",
              \"text\": {
                \"content\": \"$(echo "$DIARY_CONTENT" | sed 's/"/\\"/g' | tr '\n' ' ' | sed 's/"/\\"/g')\"
              }
            }
          ]
        }
      }
    ]
  }" | jq '.'

echo "✅ 日记已同步到 Notion"
echo "📅 日期：$DATE"
echo "📝 标题：$TITLE"
