#!/bin/bash

# 合成八字合盘海报
DATE="2026-03-28"
NIAN="丙午"
YUE="己辰"
RI="辛未"

# 输入图片和输出图片
BG_IMAGE="/workspace/projects/workspace-aesthetic/2026-03-28-final.jpg"
OUTPUT="/workspace/projects/workspace-aesthetic/poster-2026-03-28.jpg"

# 使用 ImageMagick 合成
convert "$BG_IMAGE" \
  -font "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" \
  -pointsize 60 \
  -fill "#8B4513" \
  -gravity north \
  -annotate +0+80 "${DATE}" \
  -pointsize 80 \
  -annotate +0+180 "${NIAN} · ${YUE} · ${RI}" \
  -pointsize 40 \
  -fill "#666666" \
  -annotate +0+260 "火土金相生" \
  "$OUTPUT"

echo "海报已合成：$OUTPUT"
