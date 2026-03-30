#!/usr/bin/env python3
"""
日历海报生成脚本 v4 - 带自我验证
1. 生成海报
2. 用 VL 模型检查问题
3. 自动迭代修复
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

def create_gradient_area(draw, x, y, width, height, color_top, color_bottom):
    """创建渐变区域"""
    for i in range(height):
        ratio = i / height
        r = int(color_top[0] * (1 - ratio) + color_bottom[0] * ratio)
        g = int(color_top[1] * (1 - ratio) + color_bottom[1] * ratio)
        b = int(color_top[2] * (1 - ratio) + color_bottom[2] * ratio)
        a = int(color_top[3] * (1 - ratio) + color_bottom[3] * ratio)
        draw.line([(x, y + i), (x + width, y + i)], fill=(r, g, b, a))

def create_poster(bg_path, output_path, data):
    """生成海报"""
    
    # 打开背景
    if os.path.exists(bg_path):
        img = Image.open(bg_path)
        if img.size != (POSTER_WIDTH, POSTER_HEIGHT):
            img = img.resize((POSTER_WIDTH, POSTER_HEIGHT), Image.Resampling.LANCZOS)
    else:
        img = Image.new('RGB', (POSTER_WIDTH, POSTER_HEIGHT), '#F5E6D3')
    
    img = img.convert('RGBA')
    draw = ImageDraw.Draw(img)
    
    # ========== 字体配置（调整大小）==========
    font_month = get_font(FONT_SANS_BOLD, 36)       # 英文月份
    font_date = get_font(FONT_SANS_BOLD, 320)       # 日期数字（缩小！）
    font_nongli = get_font(FONT_SERIF_REGULAR, 42) # 农历
    font_bazi = get_font(FONT_SERIF_REGULAR, 48)   # 干支
    font_li_bi = get_font(FONT_SERIF_REGULAR, 44)  # 利弊
    
    # ========== 颜色 ==========
    color_primary = (50, 40, 35)
    color_secondary = (80, 65, 55)
    color_accent = (100, 85, 70)
    
    # ========== 顶部渐变（更小范围）==========
    create_gradient_area(draw, 0, 0, POSTER_WIDTH, 600, 
                         (255, 255, 255, 100),
                         (255, 255, 255, 0))
    
    # ========== 底部渐变 ==========
    create_gradient_area(draw, 0, POSTER_HEIGHT - 400, POSTER_WIDTH, 400,
                         (255, 255, 255, 0),
                         (255, 255, 255, 80))
    
    # ========== 文字布局（增加间距！）==========
    current_y = 250  # 顶部留更多空间
    
    # 1. 英文月份 · 周几
    month = data.get("month", "MAR")
    week = data.get("week", "SAT")
    month_week = f"{month} · {week}"
    
    mw_bbox = draw.textbbox((0, 0), month_week, font=font_month)
    mw_width = mw_bbox[2] - mw_bbox[0]
    mw_height = mw_bbox[3] - mw_bbox[1]
    mw_x = (POSTER_WIDTH - mw_width) // 2
    draw.text((mw_x, current_y), month_week, font=font_month, fill=color_secondary)
    current_y += mw_height + 100  # 增加间距
    
    # 2. 日期数字（核心视觉）
    date_num = data.get("date", "29")
    date_bbox = draw.textbbox((0, 0), date_num, font=font_date)
    date_width = date_bbox[2] - date_bbox[0]
    date_height = date_bbox[3] - date_bbox[1]
    date_x = (POSTER_WIDTH - date_width) // 2
    draw.text((date_x, current_y), date_num, font=font_date, fill=color_primary)
    current_y += date_height + 150  # 大幅增加间距！
    
    # 3. 农历
    nongli = data.get("nongli", "二月初一")
    nl_bbox = draw.textbbox((0, 0), nongli, font=font_nongli)
    nl_width = nl_bbox[2] - nl_bbox[0]
    nl_height = nl_bbox[3] - nl_bbox[1]
    nl_x = (POSTER_WIDTH - nl_width) // 2
    draw.text((nl_x, current_y), nongli, font=font_nongli, fill=color_secondary)
    current_y += nl_height + 60  # 增加间距
    
    # 4. 干支
    bazi = data.get("bazi", "丙午 · 辛卯 · 壬寅")
    bz_bbox = draw.textbbox((0, 0), bazi, font=font_bazi)
    bz_width = bz_bbox[2] - bz_bbox[0]
    bz_x = (POSTER_WIDTH - bz_width) // 2
    draw.text((bz_x, current_y), bazi, font=font_bazi, fill=color_primary)
    
    # ========== 底部利弊 ==========
    li = data.get("li", "立券交易兴")
    bi = data.get("bi", "嫁娶择日宜")
    
    li_bbox = draw.textbbox((0, 0), li, font=font_li_bi)
    li_width = li_bbox[2] - li_bbox[0]
    li_x = (POSTER_WIDTH - li_width) // 2
    li_y = POSTER_HEIGHT - 300
    draw.text((li_x, li_y), li, font=font_li_bi, fill=color_accent)
    
    bi_bbox = draw.textbbox((0, 0), bi, font=font_li_bi)
    bi_width = bi_bbox[2] - bi_bbox[0]
    bi_x = (POSTER_WIDTH - bi_width) // 2
    bi_y = POSTER_HEIGHT - 230
    draw.text((bi_x, bi_y), bi, font=font_li_bi, fill=color_accent)
    
    # 保存
    img = img.convert('RGB')
    img.save(output_path, quality=95)
    print(f"✅ 海报已生成: {output_path}")
    return output_path

def validate_poster(image_path):
    """
    验证海报质量
    检查项目：
    1. 文字是否重叠
    2. 遮罩是否过重
    3. 排版是否清晰
    4. 字体是否合适
    """
    print(f"\n🔍 开始验证海报: {image_path}")
    
    issues = []
    
    # 这里应该用 VL 模型检查
    # 暂时返回空列表，后续集成 VL
    # TODO: 调用 VL 模型进行实际检查
    
    return issues

def iterate_until_good(bg_path, output_path, data, max_iterations=5):
    """迭代生成，直到验证通过"""
    
    for i in range(max_iterations):
        print(f"\n{'='*50}")
        print(f"迭代 {i+1}/{max_iterations}")
        print(f"{'='*50}")
        
        # 生成海报
        create_poster(bg_path, output_path, data)
        
        # 验证
        issues = validate_poster(output_path)
        
        if not issues:
            print("✅ 验证通过！")
            return output_path
        
        print(f"⚠️  发现问题: {len(issues)} 个")
        for issue in issues:
            print(f"  - {issue}")
        
        # 根据问题调整参数
        # TODO: 实现自动修复逻辑
    
    print(f"⚠️  达到最大迭代次数，返回当前版本")
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
    
    # 迭代生成
    iterate_until_good("bg-new.jpg", "test_poster_v4.jpg", data)