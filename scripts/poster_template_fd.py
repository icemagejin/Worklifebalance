#!/usr/bin/env python3
"""
日历海报 - Frontend Design 版
基于 Frontend Design Skill 原则：
- 避免通用字体
- 选择独特、有特色的字体
- 展示字体有视觉冲击力
- 正文字体清晰易读
- 粗细有对比
"""

from PIL import Image, ImageDraw, ImageFont
import sys
import os
import json

POSTER_WIDTH = 1080
POSTER_HEIGHT = 1920

# Frontend Design 原则字体选择
# 展示字体：思源宋体粗体（优雅、有书法感、东方美学）
FONT_DISPLAY = "/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc"

# 正文字体：文泉驿正黑锐利（现代、锐利、有力度）
FONT_BODY = "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"

# 英文字体：文泉驿正黑
FONT_EN = "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"

def get_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except:
        return ImageFont.load_default()

def create_poster_frontend_design(bg_path, output_path, data, layout_type="center"):
    """
    Frontend Design 版海报
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

    # ========== Frontend Design 字体原则 ==========

    # 展示字体（超大数字）：思源宋体粗体
    # - 优雅、有书法感
    # - 东方美学
    # - 视觉冲击力
    font_display = get_font(FONT_DISPLAY, 520)  # 更大，更有冲击力

    # 正文字体：文泉驿正黑锐利
    # - 现代、锐利、有力度
    # - 与展示字体形成对比
    # - 清晰易读
    font_body = get_font(FONT_BODY, 42)

    # 英文字体：文泉驿正黑
    font_en = get_font(FONT_EN, 26)

    # ========== Frontend Design 颜色原则 ==========

    # 主色：深墨色（更有质感）
    color_primary = (20, 15, 10)

    # 次色：中深灰
    color_secondary = (55, 45, 35)

    # 强调色：深棕
    color_accent = (40, 32, 25)

    # ========== Frontend Design 空间原则 ==========

    # 不只是居中，要有空间层次
    # 大量留白（>60%）
    # 块面结构清晰

    # 英文月份（顶部，极小）
    month = data.get("month", "MAR")
    week = data.get("week", "MON")
    month_week = f"{month} · {week}"

    mw_bbox = draw.textbbox((0, 0), month_week, font=font_en)
    mw_width = mw_bbox[2] - mw_bbox[0]
    mw_x = (POSTER_WIDTH - mw_width) // 2
    draw.text((mw_x, 120), month_week, font=font_en, fill=color_secondary)

    # 超大数字（核心视觉焦点）
    date_num = data.get("date", "30")
    date_bbox = draw.textbbox((0, 0), date_num, font=font_display)
    date_width = date_bbox[2] - date_bbox[0]
    date_height = date_bbox[3] - date_bbox[1]
    date_x = (POSTER_WIDTH - date_width) // 2
    draw.text((date_x, 320), date_num, font=font_display, fill=color_primary)

    # 信息块面（中间）
    nongli = data.get("nongli", "二月十二")
    bazi = data.get("bazi", "丙午 · 辛卯 · 癸卯")

    # 居中块面
    info_x = POSTER_WIDTH // 2
    draw.text((info_x, 850), nongli, font=font_body, fill=color_primary, anchor="mm")
    draw.text((info_x, 950), bazi, font=font_body, fill=color_secondary, anchor="mm")

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
    print(f"🎨 Frontend Design 原则:")
    print(f"   展示字体: 思源宋体粗体（优雅、书法感）")
    print(f"   正文字体: 文泉驿正黑锐利（现代、锐利）")
    print(f"   颜色: 深墨色系")
    print(f"   空间: 大量留白，块面清晰")

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

    create_poster_frontend_design("/tmp/bg_2026-03-30_pure.jpg", "/tmp/poster_2026-03-30_fd.jpg", data, "center")
