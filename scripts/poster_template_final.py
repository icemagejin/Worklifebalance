#!/usr/bin/env python3
"""
日历海报生成脚本 - 最终版
参考优秀设计，实现极简美学
"""

from PIL import Image, ImageDraw, ImageFont
import sys
import os

POSTER_WIDTH = 1080
POSTER_HEIGHT = 1920

FONT_SANS_BOLD = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
FONT_SERIF_REGULAR = "/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc"

def get_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except:
        return ImageFont.load_default()

def create_poster_final(bg_path, output_path, data, layout_type="right_bottom"):
    """
    极简美学海报
    - 超大数字（420px）
    - 大量留白（>60%）
    - 强烈字体对比
    - 动态布局
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
    
    # ========== 字体（强化对比）==========
    font_month = get_font(FONT_SANS_BOLD, 28)       # 英文：极细
    font_date = get_font(FONT_SANS_BOLD, 420)      # 数字：超大粗黑
    font_nongli = get_font(FONT_SERIF_REGULAR, 36) # 农历：细宋
    font_bazi = get_font(FONT_SERIF_REGULAR, 40)   # 干支：细宋
    font_li_bi = get_font(FONT_SERIF_REGULAR, 38)  # 利弊：细宋
    
    # ========== 颜色 ==========
    color_primary = (40, 35, 30)       # 深黑（数字）
    color_secondary = (90, 80, 70)     # 中灰
    color_accent = (120, 100, 85)      # 浅灰
    
    # ========== 动态布局 ==========
    if layout_type == "right_bottom":
        x_center = 0.38  # 偏左
        y_li_bi = POSTER_HEIGHT - 580  # 上移避开右下角图形
    elif layout_type == "left_bottom":
        x_center = 0.62  # 偏右
        y_li_bi = POSTER_HEIGHT - 580
    else:
        x_center = 0.5   # 居中
        y_li_bi = POSTER_HEIGHT - 350
    
    # ========== 极简排版（大量留白）==========
    
    # 1. 英文月份周几（顶部，极小）
    month = data.get("month", "MAR")
    week = data.get("week", "SAT")
    month_week = f"{month} · {week}"
    
    mw_bbox = draw.textbbox((0, 0), month_week, font=font_month)
    mw_width = mw_bbox[2] - mw_bbox[0]
    mw_x = int((POSTER_WIDTH - mw_width) * x_center)
    draw.text((mw_x, 180), month_week, font=font_month, fill=color_secondary)
    
    # 2. 超大日期数字（核心视觉，占画面35%）
    date_num = data.get("date", "29")
    date_bbox = draw.textbbox((0, 0), date_num, font=font_date)
    date_width = date_bbox[2] - date_bbox[0]
    date_height = date_bbox[3] - date_bbox[1]
    date_x = int((POSTER_WIDTH - date_width) * x_center)
    draw.text((date_x, 320), date_num, font=font_date, fill=color_primary)
    
    # 3. 农历（数字下方，间距大）
    nongli = data.get("nongli", "二月初一")
    nl_bbox = draw.textbbox((0, 0), nongli, font=font_nongli)
    nl_width = nl_bbox[2] - nl_bbox[0]
    nl_x = int((POSTER_WIDTH - nl_width) * x_center)
    draw.text((nl_x, 800), nongli, font=font_nongli, fill=color_secondary)
    
    # 4. 干支
    bazi = data.get("bazi", "丙午 · 辛卯 · 壬寅")
    bz_bbox = draw.textbbox((0, 0), bazi, font=font_bazi)
    bz_width = bz_bbox[2] - bz_bbox[0]
    bz_x = int((POSTER_WIDTH - bz_width) * x_center)
    draw.text((bz_x, 900), bazi, font=font_bazi, fill=color_primary)
    
    # 5. 利弊（极简icon + 细字）
    li = data.get("li", "立券交易兴")
    bi = data.get("bi", "嫁娶择日宜")
    
    # 利：极小装饰
    li_text = f"–  {li}"  # 极简横线
    li_bbox = draw.textbbox((0, 0), li_text, font=font_li_bi)
    li_width = li_bbox[2] - li_bbox[0]
    li_x = int((POSTER_WIDTH - li_width) * x_center)
    draw.text((li_x, y_li_bi), li_text, font=font_li_bi, fill=color_accent)
    
    # 弊
    bi_text = f"–  {bi}"
    bi_bbox = draw.textbbox((0, 0), bi_text, font=font_li_bi)
    bi_width = bi_bbox[2] - bi_bbox[0]
    bi_x = int((POSTER_WIDTH - bi_width) * x_center)
    draw.text((bi_x, y_li_bi + 90), bi_text, font=font_li_bi, fill=color_accent)
    
    # 保存
    img = img.convert('RGB')
    img.save(output_path, quality=95)
    print(f"✅ 海报已生成: {output_path}")
    
    return output_path

if __name__ == "__main__":
    data = {
        "month": "MAR",
        "week": "SAT",
        "date": "29",
        "nongli": "二月初一",
        "bazi": "丙午 · 辛卯 · 壬寅",
        "li": "立券交易兴",
        "bi": "嫁娶择日宜"
    }
    
    create_poster_final("bg_light_ink.jpg", "test_poster_final.jpg", data, "right_bottom")