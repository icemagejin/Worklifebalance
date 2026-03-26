#!/bin/bash
# 八字合盘海报生成脚本
# 生成时间：每天 09:10

set -e

DATE=$(date +%Y-%m-%d)
TIME=$(date +"%H:%M")
YEAR_CN=$(date +%Y)
MONTH_CN=$(date +%m | sed 's/^0//')
DAY_CN=$(date +%d | sed 's/^0//')
WEEKDAY_EN=$(date +%A | tr '[:lower:]' '[:upper:]')
MONTH_EN=$(date +%B | tr '[:lower:]' '[:upper:]')

# 输出文件路径
OUTPUT_DIR="/workspace/projects/workspace-aesthetic/posters"
mkdir -p "$OUTPUT_DIR"
OUTPUT_FILE="$OUTPUT_DIR/daily-poster-$DATE.json"

# 生成今日八字合盘海报任务描述
cat > "$OUTPUT_FILE" << EOF
{
  "date": "$DATE",
  "time": "$TIME",
  "task": "八字合盘海报生成",
  "steps": [
    {
      "step": 1,
      "action": "计算今日干支",
      "year_zhi": "丙午",
      "month_zhi": "壬辰",
      "day_zhi": "甲午"
    },
    {
      "step": 2,
      "action": "与大Boss八字合盘分析",
      "boss_bazi": "乙丑 丙戌 戊申",
      "analysis": "吉：丙火旺盛，乙木得火相助 → 事业上升\n凶：戊申土金受克 → 需谨慎决策"
    },
    {
      "step": 3,
      "action": "生成对仗祝福语（6+6）",
      "couplets": [
        "茶酒喜相迎，求谋并嫁娶",
        "好合有天成，祸福如神验"
      ]
    },
    {
      "step": 4,
      "action": "生成体现今日干支的背景图",
      "style": "现代国画写意",
      "elements": "一笔暖色光晕+几笔墨线",
      "constraint": "绝对禁止文字",
      "theme": "火木相生（丙午甲午）"
    },
    {
      "step": 5,
      "action": "合成完整海报",
      "elements": [
        "超大数字'$DAY_CN'",
        "极小字'$MONTH_EN $WEEKDAY_EN'",
        "极小字'丙午·甲午'",
        "两行6字对仗祝福语"
      ],
      "design_style": "极简留白，iPhone全屏"
    }
  ]
}
EOF

echo "✅ 八字合盘海报任务已生成：$OUTPUT_FILE"
echo "📅 日期：$DATE"
echo "🕐 干支：丙午年 壬辰月 甲午日"
EOF