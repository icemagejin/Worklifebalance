#!/usr/bin/env python3
"""
日历海报生成脚本 - 参考优雅设计
特点：
1. 超大数字日期（粗黑体）
2. 极简布局，大量留白
3. 粗细字体对比（Sans Bold + Serif Regular）
4. 底部干支信息简洁
5. 利弊对仗（6-8字）
"""

from PIL import Image, ImageDraw, ImageFont
import sys
import os

# 配置
POSTER_WIDTH = 1080
POSTER_HEIGHT = 1920

# 字体路径
FONT_SANS_BOLD = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
FONT_SANS_REGULAR = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
FONT_SERIF_REGULAR = "/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc"
FONT_SERIF_BOLD = "/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc"

# 如果没有对应字体，使用备选
def get_font(path, size, backup=None):
    try:
        return ImageFont.truetype(path, size)
    except:
        if backup:
            try:
                return ImageFont.truetype(backup, size)
            except:
                pass
        # 返回默认字体
        return ImageFont.load_default()

def create_poster(bg_path, output_path, data):
    """
    创建海报
    
    data = {
        "month_week": "MARCH SAT",        # 英文月份+周几
        "date": "29",                      # 日期数字
        "nongli": "二月初一",              # 农历
        "bazi": "丙午 · 辛卯 · 壬寅",     # 干支
        "li": "立券交易兴",               # 利（6-8字对仗）
        "bi": "嫁娶择日宜"                # 弊（6-8字对仗）
    }
    """
    
    # 打开背景图
    if os.path.exists(bg_path):
        img = Image.open(bg_path)
        # 确保尺寸正确
        if img.size != (POSTER_WIDTH, POSTER_HEIGHT):
            img = img.resize((POSTER_WIDTH, POSTER_HEIGHT), Image.Resampling.LANCZOS)
    else:
        # 创建纯色背景
        img = Image.new('RGB', (POSTER_WIDTH, POSTER_HEIGHT), '#F5E6D3')
    
    # 转为RGBA以便添加半透明遮罩
    img = img.convert('RGBA')
    
    # 添加半透明白色遮罩（让文字更清晰）
    overlay = Image.new('RGBA', (POSTER_WIDTH, POSTER_HEIGHT), (255, 255, 255, 100))
    img = Image.alpha_composite(img, overlay)
    
    draw = ImageDraw.Draw(img)
    
    # ========== 字体配置 ==========
    # 英文月份周几 - 细无衬线
    font_month = get_font(FONT_SANS_REGULAR, 36)
    
    # 日期数字 - 超大粗黑体
    font_date = get_font(FONT_SANS_BOLD, 380, FONT_SANS_REGULAR)
    
    # 农历 - 细宋体
    font_nongli = get_font(FONT_SERIF_REGULAR, 42)
    
    # 干支 - 中号宋体
    font_bazi = get_font(FONT_SERIF_REGULAR, 48)
    
    # 利弊对仗 - 宋体
    font_li_bi = get_font(FONT_SERIF_REGULAR, 44)
    
    # ========== 颜色配置 ==========
    # 参考图的色调 - 深棕色系
    color_primary = (60, 45, 30)      # 主要文字色（深棕）
    color_secondary = (100, 80, 60)   # 次要文字色（中棕）
    color_accent = (140, 110, 80)     # 强调色（浅棕）
    
    # ========== 布局计算 ==========
    current_y = 180  # 顶部留白
    
    # 1. 英文月份周几（顶部，细字）
    month_week = data.get("month_week", "MARCH SAT")
    month_bbox = draw.textbbox((0, 0), month_week, font=font_month)
    month_width = month_bbox[2] - month_bbox[0]
    month_x = (POSTER_WIDTH - month_width) // 2
    draw.text((month_x, current_y), month_week, font=font_month, fill=color_secondary)
    current_y += 80
    
    # 2. 超大日期数字（视觉焦点）
    date_num = data.get("date", "29")
    date_bbox = draw.textbbox((0, 0), date_num, font=font_date)
    date_width = date_bbox[2] - date_bbox[0]
    date_height = date_bbox[3] - date_bbox[1]
    date_x = (POSTER_WIDTH - date_width) // 2
    draw.text((date_x, current_y), date_num, font=font_date, fill=color_primary)
    current_y += date_height + 60
    
    # 3. 农历
    nongli = data.get("nongli", "二月初一")
    nongli_bbox = draw.textbbox((0, 0), nongli, font=font_nongli)
    nongli_width = nongli_bbox[2] - nongli_bbox[0]
    nongli_x = (POSTER_WIDTH - nongli_width) // 2
    draw.text((nongli_x, current_y), nongli, font=font_nongli, fill=color_secondary)
    current_y += 100
    
    # 4. 干支（用点分隔）
    bazi = data.get("bazi", "丙午 · 辛卯 · 壬寅")
    bazi_bbox = draw.textbbox((0, 0), bazi, font=font_bazi)
    bazi_width = bazi_bbox[2] - bazi_bbox[0]
    bazi_x = (POSTER_WIDTH - bazi_width) // 2
    draw.text((bazi_x, current_y), bazi, font=font_bazi, fill=color_primary)
    
    # ========== 底部利弊对仗 ==========
    # 放在最底部，两行对仗
    li = data.get("li", "立券交易兴")
    bi = data.get("bi", "嫁娶择日宜")
    
    # 利（左对齐，或居中）
    li_bbox = draw.textbbox((0, 0), li, font=font_li_bi)
    li_width = li_bbox[2] - li_bbox[0]
    li_x = (POSTER_WIDTH - li_width) // 2
    li_y = POSTER_HEIGHT - 280
    draw.text((li_x, li_y), li, font=font_li_bi, fill=color_accent)
    
    # 弊
    bi_bbox = draw.textbbox((0, 0), bi, font=font_li_bi)
    bi_width = bi_bbox[2] - bi_bbox[0]
    bi_x = (POSTER_WIDTH - bi_width) // 2
    bi_y = POSTER_HEIGHT - 220
    draw.text((bi_x, bi_y), bi, font=font_li_bi, fill=color_accent)
    
    # 保存
    img = img.convert('RGB')
    img.save(output_path, quality=95)
    print(f"✅ 海报已生成: {output_path}")
    
    return output_path

def main():
    # 示例数据
    data = {
        "month_week": "MARCH SAT",
        "date": "29",
        "nongli": "二月初一",
        "bazi": "丙午 · 辛卯 · 壬寅",
        "li": "立券交易兴",
        "bi": "嫁娶择日宜"
    }
    
    # 如果有命令行参数
    if len(sys.argv) > 1:
        data["date"] = sys.argv[1]
    if len(sys.argv) > 2:
        data["nongli"] = sys.argv[2]
    if len(sys.argv) > 3:
        data["bazi"] = sys.argv[3]
    if len(sys.argv) > 4:
        data["li"] = sys.argv[4]
    if len(sys.argv) > 5:
        data["bi"] = sys.argv[5]
    
    # 背景图路径
    bg_path = "background.jpg"
    output_path = "poster_output.jpg"
    
    create_poster(bg_path, output_path, data)

if __name__ == "__main__":
    main()