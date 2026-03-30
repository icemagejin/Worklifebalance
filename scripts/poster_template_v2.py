#!/usr/bin/env python3
"""
日历海报生成脚本 v2 - 优雅设计
参考：极简日历风格

改进：
1. 不用遮罩，让背景自然呈现
2. 英文月份·周几（中间加点）
3. 更优雅的字体搭配
4. 文字加阴影提升可读性
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import sys
import os

POSTER_WIDTH = 1080
POSTER_HEIGHT = 1920

# 优雅字体
FONT_SANS_BOLD = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
FONT_SERIF_REGULAR = "/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc"

def get_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except:
        return ImageFont.load_default()

def draw_text_with_shadow(draw, pos, text, font, fill, shadow_color=(0,0,0,60), shadow_offset=3):
    """绘制带阴影的文字，提升在背景上的可读性"""
    x, y = pos
    
    # 阴影层（轻微模糊效果通过偏移实现）
    for dx in range(-shadow_offset, shadow_offset+1, 2):
        for dy in range(-shadow_offset, shadow_offset+1, 2):
            draw.text((x+dx, y+dy), text, font=font, fill=shadow_color)
    
    # 主文字
    draw.text(pos, text, font=font, fill=fill)

def create_poster(bg_path, output_path, data):
    """
    创建优雅日历海报
    """
    
    # 打开背景
    if os.path.exists(bg_path):
        img = Image.open(bg_path)
        if img.size != (POSTER_WIDTH, POSTER_HEIGHT):
            img = img.resize((POSTER_WIDTH, POSTER_HEIGHT), Image.Resampling.LANCZOS)
    else:
        img = Image.new('RGB', (POSTER_WIDTH, POSTER_HEIGHT), '#F5E6D3')
    
    img = img.convert('RGBA')
    draw = ImageDraw.Draw(img)
    
    # ========== 字体 ==========
    # 英文月份周几 - 细字
    font_month = get_font(FONT_SANS_BOLD, 32)
    
    # 日期数字 - 超大粗体
    font_date = get_font(FONT_SANS_BOLD, 400)
    
    # 农历 - 优雅宋体
    font_nongli = get_font(FONT_SERIF_REGULAR, 38)
    
    # 干支 - 宋体
    font_bazi = get_font(FONT_SERIF_REGULAR, 44)
    
    # 利弊 - 宋体
    font_li_bi = get_font(FONT_SERIF_REGULAR, 40)
    
    # ========== 颜色 ==========
    # 参考图的色调 - 深色文字在浅色背景上
    color_primary = (50, 40, 35)       # 主文字（深棕黑）
    color_secondary = (80, 65, 55)     # 次要文字
    color_accent = (100, 85, 70)       # 强调色
    
    # ========== 布局 ==========
    current_y = 200
    
    # 1. 英文月份 · 周几（用点分隔！）
    month = data.get("month", "MAR")
    week = data.get("week", "SAT")
    month_week = f"{month} · {week}"  # 用点分隔！
    
    mw_bbox = draw.textbbox((0, 0), month_week, font=font_month)
    mw_width = mw_bbox[2] - mw_bbox[0]
    mw_x = (POSTER_WIDTH - mw_width) // 2
    
    draw_text_with_shadow(draw, (mw_x, current_y), month_week, font_month, color_secondary)
    current_y += 80
    
    # 2. 超大日期数字
    date_num = data.get("date", "29")
    date_bbox = draw.textbbox((0, 0), date_num, font=font_date)
    date_width = date_bbox[2] - date_bbox[0]
    date_height = date_bbox[3] - date_bbox[1]
    date_x = (POSTER_WIDTH - date_width) // 2
    
    draw_text_with_shadow(draw, (date_x, current_y), date_num, font_date, color_primary, shadow_offset=4)
    current_y += date_height + 50
    
    # 3. 农历
    nongli = data.get("nongli", "二月初一")
    nl_bbox = draw.textbbox((0, 0), nongli, font=font_nongli)
    nl_width = nl_bbox[2] - nl_bbox[0]
    nl_x = (POSTER_WIDTH - nl_width) // 2
    
    draw_text_with_shadow(draw, (nl_x, current_y), nongli, font_nongli, color_secondary)
    current_y += 80
    
    # 4. 干支
    bazi = data.get("bazi", "丙午 · 辛卯 · 壬寅")
    bz_bbox = draw.textbbox((0, 0), bazi, font=font_bazi)
    bz_width = bz_bbox[2] - bz_bbox[0]
    bz_x = (POSTER_WIDTH - bz_width) // 2
    
    draw_text_with_shadow(draw, (bz_x, current_y), bazi, font_bazi, color_primary)
    
    # ========== 底部利弊 ==========
    li = data.get("li", "立券交易兴")
    bi = data.get("bi", "嫁娶择日宜")
    
    # 利
    li_bbox = draw.textbbox((0, 0), li, font=font_li_bi)
    li_width = li_bbox[2] - li_bbox[0]
    li_x = (POSTER_WIDTH - li_width) // 2
    li_y = POSTER_HEIGHT - 260
    
    draw_text_with_shadow(draw, (li_x, li_y), li, font_li_bi, color_accent)
    
    # 弊
    bi_bbox = draw.textbbox((0, 0), bi, font=font_li_bi)
    bi_width = bi_bbox[2] - bi_bbox[0]
    bi_x = (POSTER_WIDTH - bi_width) // 2
    bi_y = POSTER_HEIGHT - 200
    
    draw_text_with_shadow(draw, (bi_x, bi_y), bi, font_li_bi, color_accent)
    
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
    
    if len(sys.argv) > 1:
        data["date"] = sys.argv[1]
    
    create_poster("bg-new.jpg", "test_poster_v2.jpg", data)