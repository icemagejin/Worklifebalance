#!/usr/bin/env python3
"""
日历海报生成脚本 v7 - 真正的动态布局
根据背景图形位置，动态调整文字位置
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

def create_poster_dynamic_v7(bg_path, output_path, data, layout_type="right_bottom"):
    """
    根据图形位置动态调整布局
    
    layout_type:
    - "right_bottom": 图形在右下角 → 文字靠左上
    - "left_bottom": 图形在左下角 → 文字靠右上
    - "center": 图形在中间 → 文字靠上下边缘
    - "full": 满幅图形 → 文字居中
    """
    
    # 打开背景
    if os.path.exists(bg_path):
        img = Image.open(bg_path)
        if img.size != (POSTER_WIDTH, POSTER_HEIGHT):
            img = img.resize((POSTER_WIDTH, POSTER_HEIGHT), Image.Resampling.LANCZOS)
    else:
        img = Image.new('RGB', (POSTER_WIDTH, POSTER_HEIGHT), '#F5F5F0')
    
    img = img.convert('RGBA')
    draw = ImageDraw.Draw(img)
    
    # 字体
    font_month = get_font(FONT_SANS_BOLD, 36)
    font_date = get_font(FONT_SANS_BOLD, 320)
    font_nongli = get_font(FONT_SERIF_REGULAR, 42)
    font_bazi = get_font(FONT_SERIF_REGULAR, 48)
    font_li_bi = get_font(FONT_SERIF_REGULAR, 44)
    
    # 颜色
    color_primary = (50, 40, 35)
    color_secondary = (80, 65, 55)
    color_accent = (100, 85, 70)
    
    # ========== 根据布局类型调整位置 ==========
    # 通用间距设置（增大！）
    y_month = 180        # 英文月份
    y_date = 380         # 日期数字
    y_nongli = 850       # 农历（大幅下移！避开数字）
    y_bazi = 950         # 干支
    
    if layout_type == "right_bottom":
        # 图形在右下角 → 文字靠左
        month_x_factor = 0.35  # 偏左
        date_x_factor = 0.4    # 稍偏左
        nongli_x_factor = 0.4
        bazi_x_factor = 0.4
        li_bi_y = POSTER_HEIGHT - 550  # 上移更多！避开右下角图形
        li_bi_x_factor = 0.35  # 靠左
        
    elif layout_type == "left_bottom":
        # 图形在左下角 → 文字靠右
        month_x_factor = 0.65
        date_x_factor = 0.6
        nongli_x_factor = 0.6
        bazi_x_factor = 0.6
        li_bi_y = POSTER_HEIGHT - 550
        li_bi_x_factor = 0.65
        
    elif layout_type == "center":
        # 图形在中间 → 文字靠上下边缘
        month_x_factor = 0.5
        date_x_factor = 0.5
        nongli_x_factor = 0.5
        bazi_x_factor = 0.5
        li_bi_y = POSTER_HEIGHT - 280
        li_bi_x_factor = 0.5
        
    else:  # full
        # 满幅 → 居中
        month_x_factor = 0.5
        date_x_factor = 0.5
        nongli_x_factor = 0.5
        bazi_x_factor = 0.5
        li_bi_y = POSTER_HEIGHT - 350
        li_bi_x_factor = 0.5
    
    # ========== 绘制文字 ==========
    
    # 1. 英文月份周几
    month = data.get("month", "MAR")
    week = data.get("week", "SAT")
    month_week = f"{month} · {week}"
    
    mw_bbox = draw.textbbox((0, 0), month_week, font=font_month)
    mw_width = mw_bbox[2] - mw_bbox[0]
    mw_x = int((POSTER_WIDTH - mw_width) * month_x_factor)
    draw.text((mw_x, y_month), month_week, font=font_month, fill=color_secondary)
    
    # 2. 日期数字
    date_num = data.get("date", "29")
    date_bbox = draw.textbbox((0, 0), date_num, font=font_date)
    date_width = date_bbox[2] - date_bbox[0]
    date_height = date_bbox[3] - date_bbox[1]
    date_x = int((POSTER_WIDTH - date_width) * date_x_factor)
    draw.text((date_x, y_date), date_num, font=font_date, fill=color_primary)
    
    # 3. 农历
    nongli = data.get("nongli", "二月初一")
    nl_bbox = draw.textbbox((0, 0), nongli, font=font_nongli)
    nl_width = nl_bbox[2] - nl_bbox[0]
    nl_x = int((POSTER_WIDTH - nl_width) * nongli_x_factor)
    draw.text((nl_x, y_nongli), nongli, font=font_nongli, fill=color_secondary)
    
    # 4. 干支
    bazi = data.get("bazi", "丙午 · 辛卯 · 壬寅")
    bz_bbox = draw.textbbox((0, 0), bazi, font=font_bazi)
    bz_width = bz_bbox[2] - bz_bbox[0]
    bz_x = int((POSTER_WIDTH - bz_width) * bazi_x_factor)
    draw.text((bz_x, y_bazi), bazi, font=font_bazi, fill=color_primary)
    
    # 5. 利弊
    li = data.get("li", "立券交易兴")
    bi = data.get("bi", "嫁娶择日宜")
    
    li_text = f"❖  {li}"
    li_bbox = draw.textbbox((0, 0), li_text, font=font_li_bi)
    li_width = li_bbox[2] - li_bbox[0]
    li_x = int((POSTER_WIDTH - li_width) * li_bi_x_factor)
    draw.text((li_x, li_bi_y), li_text, font=font_li_bi, fill=color_accent)
    
    bi_text = f"◇  {bi}"
    bi_bbox = draw.textbbox((0, 0), bi_text, font=font_li_bi)
    bi_width = bi_bbox[2] - bi_bbox[0]
    bi_x = int((POSTER_WIDTH - bi_width) * li_bi_x_factor)
    draw.text((bi_x, li_bi_y + 80), bi_text, font=font_li_bi, fill=color_accent)  # 间距增大到80
    
    # 保存
    img = img.convert('RGB')
    img.save(output_path, quality=95)
    print(f"✅ 海报已生成: {output_path}")
    print(f"📐 布局类型: {layout_type}")
    
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
    
    # 生成不同布局版本
    print("生成右下角图形布局版本...")
    create_poster_dynamic_v7("bg_light_ink.jpg", "test_poster_v7_right.jpg", data, "right_bottom")