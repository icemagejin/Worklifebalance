#!/usr/bin/env python3
"""
日历海报 - 块面结构版（方案A：思源宋体 + 思源黑体）
字体优化：基于 Frontend Design 原则
"""

from PIL import Image, ImageDraw, ImageFont
import sys
import os
import json

POSTER_WIDTH = 1080
POSTER_HEIGHT = 1920

# 方案A：思源宋体 + 思源黑体（优雅对比）
FONT_DISPLAY = "/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc"  # 思源宋体粗体（展示字体）
FONT_BODY = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"  # 思源黑体常规（正文字体）
FONT_MONTH = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"  # 英文月份

def get_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except:
        return ImageFont.load_default()

def create_poster_with_blocks(bg_path, output_path, data, layout_type="center", params=None):
    """
    块面结构设计（方案A字体）
    """
    if params is None:
        params = {}

    # 打开背景
    if os.path.exists(bg_path):
        img = Image.open(bg_path)
        if img.size != (POSTER_WIDTH, POSTER_HEIGHT):
            img = img.resize((POSTER_WIDTH, POSTER_HEIGHT), Image.Resampling.LANCZOS)
    else:
        img = Image.new('RGB', (POSTER_WIDTH, POSTER_HEIGHT), '#FAFAFA')

    img = img.convert('RGBA')
    draw = ImageDraw.Draw(img)

    # ========== 可调参数 ==========
    size_month = params.get('size_month', 28)
    size_display = params.get('size_display', 480)  # 思源宋体需要更大字号
    size_body = params.get('size_body', 40)       # 思源黑体常规字体
    size_li_bi = params.get('size_li_bi', 38)

    offset_date_y = params.get('offset_date_y', 300)
    offset_info_y = params.get('offset_info_y', 800)
    offset_li_bi_y = params.get('offset_li_bi_y', POSTER_HEIGHT - 520)

    # ========== 字体（方案A：思源宋体 + 思源黑体）==========
    font_month = get_font(FONT_MONTH, size_month)
    font_display = get_font(FONT_DISPLAY, size_display)  # 思源宋体粗体（展示）
    font_body = get_font(FONT_BODY, size_body)            # 思源黑体常规（正文）
    font_li_bi = get_font(FONT_BODY, size_li_bi)

    # ========== 颜色（更有力度）==========
    color_primary = (25, 20, 15)       # 更深的黑色（思源宋体需要更深）
    color_secondary = (60, 50, 40)     # 中深
    color_accent = (45, 38, 30)        # 强调

    # ========== 块面结构 ==========
    if layout_type == "right_bottom":
        info_x = 100
    elif layout_type == "left_bottom":
        info_x = POSTER_WIDTH - 400
    else:
        info_x = POSTER_WIDTH // 2

    # ========== 上半部分：超大数字（思源宋体粗体）==========
    date_num = data.get("date", "30")
    date_bbox = draw.textbbox((0, 0), date_num, font=font_display)
    date_width = date_bbox[2] - date_bbox[0]
    date_x = (POSTER_WIDTH - date_width) // 2
    draw.text((date_x, offset_date_y), date_num, font=font_display, fill=color_primary)

    # ========== 英文月份（思源黑体常规）==========
    month = data.get("month", "MAR")
    week = data.get("week", "MON")
    month_week = f"{month} · {week}"

    mw_bbox = draw.textbbox((0, 0), month_week, font=font_month)
    mw_width = mw_bbox[2] - mw_bbox[0]
    mw_x = (POSTER_WIDTH - mw_width) // 2
    draw.text((mw_x, 150), month_week, font=font_month, fill=color_secondary)

    # ========== 中间部分：信息块面（思源黑体常规）==========
    nongli = data.get("nongli", "二月十二")
    if layout_type == "center":
        draw.text((info_x, offset_info_y), nongli, font=font_body, fill=color_primary, anchor="mm")
    else:
        draw.text((info_x, offset_info_y), nongli, font=font_body, fill=color_primary)

    bazi = data.get("bazi", "丙午 · 辛卯 · 癸卯")
    bazi_y = offset_info_y + 100
    if layout_type == "center":
        draw.text((info_x, bazi_y), bazi, font=font_body, fill=color_secondary, anchor="mm")
    else:
        draw.text((info_x, bazi_y), bazi, font=font_body, fill=color_secondary)

    # ========== 下半部分：利弊块面 ==========
    li = data.get("li", "立券交易兴")
    bi = data.get("bi", "嫁娶远出行")

    if layout_type == "right_bottom":
        li_bi_y = POSTER_HEIGHT - 520
    elif layout_type == "left_bottom":
        li_bi_y = POSTER_HEIGHT - 280
    else:
        li_bi_y = POSTER_HEIGHT - 280

    if layout_type == "center":
        draw.text((info_x, li_bi_y), f"宜  {li}", font=font_li_bi, fill=color_accent, anchor="mm")
        draw.text((info_x, li_bi_y + 90), f"忌  {bi}", font=font_li_bi, fill=color_accent, anchor="mm")
    else:
        draw.text((info_x, li_bi_y), f"宜  {li}", font=font_li_bi, fill=color_accent)
        draw.text((info_x, li_bi_y + 90), f"忌  {bi}", font=font_li_bi, fill=color_accent)

    # 保存
    img = img.convert('RGB')
    img.save(output_path, quality=95)
    print(f"✅ 海报已生成: {output_path}")
    print(f"🎨 字体方案: 思源宋体粗体（展示）+ 思源黑体常规（正文）")

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

    create_poster_with_blocks("/tmp/bg_2026-03-30_clean.jpg", "/tmp/poster_2026-03-30_serif.jpg", data, "center")
