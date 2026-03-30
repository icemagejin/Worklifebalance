#!/usr/bin/env python3
"""
日历海报 - Frontend Design 版（修复重叠）
修复：调整数字位置和字号，避免与农历重叠
"""

from PIL import Image, ImageDraw, ImageFont
import sys
import os
import json

POSTER_WIDTH = 1080
POSTER_HEIGHT = 1920

# Frontend Design 原则字体选择
FONT_DISPLAY = "/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc"
FONT_BODY = "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"
FONT_EN = "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"

def get_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except:
        return ImageFont.load_default()

def create_poster_frontend_design_v2(bg_path, output_path, data, layout_type="center"):
    """
    Frontend Design 版海报（修复重叠）
    """

    # 打开背景
    if os.path.exists(bg_path):
        img = Image.open(bg_path)
        if img.size != (POSTER_WIDTH, POSTER_HEIGHT):
            img = img.resize((POSTER_WIDTH, POSTER_HEIGHT), Image.Resampling.LANCZOS)
    else:
        img = Image.new('RGB', (POSTER_WIDTH, POSTER_HEIGHT), '#FAFAFA')

    img = img.convert('RGBA')
    draw = ImageDraw.Draw(img)

    # ========== 修复：调整字号和位置 ==========

    # 展示字体：思源宋体粗体
    # - 减小字号：520px → 480px
    font_display = get_font(FONT_DISPLAY, 480)

    # 正文字体：文泉驿正黑锐利
    font_body = get_font(FONT_BODY, 40)

    # 英文字体：文泉驿正黑
    font_en = get_font(FONT_EN, 24)

    # ========== 颜色 ==========

    color_primary = (20, 15, 10)
    color_secondary = (55, 45, 35)
    color_accent = (40, 32, 25)

    # ========== 修复：调整位置 ==========

    # 英文月份（顶部，极小）
    month = data.get("month", "MAR")
    week = data.get("week", "MON")
    month_week = f"{month} · {week}"

    mw_bbox = draw.textbbox((0, 0), month_week, font=font_en)
    mw_width = mw_bbox[2] - mw_bbox[0]
    mw_x = (POSTER_WIDTH - mw_width) // 2
    draw.text((mw_x, 110), month_week, font=font_en, fill=color_secondary)

    # 超大数字（修复：向上移）
    date_num = data.get("date", "30")
    date_bbox = draw.textbbox((0, 0), date_num, font=font_display)
    date_width = date_bbox[2] - date_bbox[0]
    date_x = (POSTER_WIDTH - date_width) // 2
    # 向上移：320 → 280
    draw.text((date_x, 280), date_num, font=font_display, fill=color_primary)

    # 信息块面（修复：向下移）
    nongli = data.get("nongli", "二月十二")
    bazi = data.get("bazi", "丙午 · 辛卯 · 癸卯")

    info_x = POSTER_WIDTH // 2
    # 向下移：850 → 900
    draw.text((info_x, 900), nongli, font=font_body, fill=color_primary, anchor="mm")
    # 向下移：950 → 1000
    draw.text((info_x, 1000), bazi, font=font_body, fill=color_secondary, anchor="mm")

    # 利弊块面（底部）
    li = data.get("li", "立券交易兴")
    bi = data.get("bi", "嫁娶远出行")

    li_bi_y = POSTER_HEIGHT - 250
    draw.text((info_x, li_bi_y), f"宜  {li}", font=font_body, fill=color_accent, anchor="mm")
    draw.text((info_x, li_bi_y + 85), f"忌  {bi}", font=font_body, fill=color_accent, anchor="mm")

    # 保存
    img = img.convert('RGB')
    img.save(output_path, quality=95)
    print(f"✅ 海报已生成: {output_path}")
    print(f"🔧 修复：调整字号和位置，避免重叠")
    print(f"   数字字号: 520px → 480px")
    print(f"   数字位置: y=320 → y=280（向上移）")
    print(f"   农历位置: y=850 → y=900（向下移）")
    print(f"   干支位置: y=950 → y=1000（向下移）")

    return output_path

if __name__ == "__main__":
    data = {
        "month": "MAR",
        "week": "MON",
        "date": "30",
        "nongli": "二月十二",
        "bazi": "丙午 · 辛卯 · 癸卯",
        "li": "立券交易兴",
        "bi": "嫁娶远出行"
    }

    create_poster_frontend_design_v2("/tmp/bg_2026-03-30_pure.jpg", "/tmp/poster_2026-03-30_fd2.jpg", data, "center")
