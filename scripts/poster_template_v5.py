#!/usr/bin/env python3
"""
日历海报生成脚本 v5 - 动态布局
核心：根据背景图形位置，智能调整文字排版

流程：
1. 生成/获取背景图（水墨写意，位置不固定）
2. 分析图形位置（使用 VL 模型或图像分析）
3. 智能排版（避开图形区域）
4. 添加利弊icon
5. 自我验证
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import sys
import os
import random

POSTER_WIDTH = 1080
POSTER_HEIGHT = 1920

FONT_SANS_BOLD = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
FONT_SERIF_REGULAR = "/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc"

def get_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except:
        return ImageFont.load_default()

def analyze_image_regions(img):
    """
    分析图像，找出图形集中区域
    返回：图形位置（top-left, top-right, center, bottom-left, bottom-right）
    """
    # 转为灰度
    gray = img.convert('L')
    
    # 分成9宫格
    w, h = gray.size
    regions = {
        'top_left': (0, 0, w//3, h//3),
        'top_center': (w//3, 0, 2*w//3, h//3),
        'top_right': (2*w//3, 0, w, h//3),
        'center_left': (0, h//3, w//3, 2*h//3),
        'center': (w//3, h//3, 2*w//3, 2*h//3),
        'center_right': (2*w//3, h//3, w, 2*h//3),
        'bottom_left': (0, 2*h//3, w//3, h),
        'bottom_center': (w//3, 2*h//3, 2*w//3, h),
        'bottom_right': (2*w//3, 2*h//3, w, h)
    }
    
    # 计算每个区域的"活跃度"（非白色像素比例）
    activity = {}
    for name, (x1, y1, x2, y2) in regions.items():
        region = gray.crop((x1, y1, x2, y2))
        # 统计非白色像素
        pixels = list(region.getdata())
        non_white = sum(1 for p in pixels if p < 240)
        activity[name] = non_white / len(pixels)
    
    # 找出最活跃区域（图形所在位置）
    max_region = max(activity, key=activity.get)
    
    return max_region, activity

def get_layout_for_region(region):
    """
    根据图形位置，返回文字布局方案
    """
    layouts = {
        'top_left': {
            'description': '图形在左上角',
            'text_positions': {
                'month_week': 'top_right',
                'date': 'center',
                'nongli': 'center',
                'bazi': 'center',
                'li_bi': 'bottom_center'
            }
        },
        'top_center': {
            'description': '图形在顶部中间',
            'text_positions': {
                'month_week': 'top_left',
                'date': 'center_left',
                'nongli': 'center_left',
                'bazi': 'center_left',
                'li_bi': 'bottom_center'
            }
        },
        'top_right': {
            'description': '图形在右上角',
            'text_positions': {
                'month_week': 'top_left',
                'date': 'center',
                'nongli': 'center',
                'bazi': 'center',
                'li_bi': 'bottom_center'
            }
        },
        'center': {
            'description': '图形在中间',
            'text_positions': {
                'month_week': 'top_center',
                'date': 'top_center_below',
                'nongli': 'bottom_center_above',
                'bazi': 'bottom_center',
                'li_bi': 'bottom_center'
            }
        },
        'bottom_left': {
            'description': '图形在左下角',
            'text_positions': {
                'month_week': 'top_center',
                'date': 'center',
                'nongli': 'center',
                'bazi': 'center',
                'li_bi': 'top_right'
            }
        },
        'bottom_right': {
            'description': '图形在右下角',
            'text_positions': {
                'month_week': 'top_center',
                'date': 'center',
                'nongli': 'center',
                'bazi': 'center',
                'li_bi': 'top_left'
            }
        }
    }
    
    return layouts.get(region, layouts['center'])

def create_poster_dynamic(bg_path, output_path, data):
    """
    动态布局海报生成
    """
    
    # 打开背景
    if os.path.exists(bg_path):
        img = Image.open(bg_path)
        if img.size != (POSTER_WIDTH, POSTER_HEIGHT):
            img = img.resize((POSTER_WIDTH, POSTER_HEIGHT), Image.Resampling.LANCZOS)
    else:
        img = Image.new('RGB', (POSTER_WIDTH, POSTER_HEIGHT), '#F5F5F0')
    
    # 分析图形位置
    region, activity = analyze_image_regions(img)
    layout = get_layout_for_region(region)
    
    print(f"📊 图形位置: {region}")
    print(f"📝 布局方案: {layout['description']}")
    
    # 转为RGBA
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
    
    # ========== 根据布局动态放置文字 ==========
    positions = layout['text_positions']
    
    # 1. 英文月份周几
    month = data.get("month", "MAR")
    week = data.get("week", "SAT")
    month_week = f"{month} · {week}"
    
    mw_bbox = draw.textbbox((0, 0), month_week, font=font_month)
    mw_width = mw_bbox[2] - mw_bbox[0]
    
    if positions['month_week'] == 'top_center':
        mw_x = (POSTER_WIDTH - mw_width) // 2
        mw_y = 200
    elif positions['month_week'] == 'top_left':
        mw_x = 100
        mw_y = 200
    elif positions['month_week'] == 'top_right':
        mw_x = POSTER_WIDTH - mw_width - 100
        mw_y = 200
    else:
        mw_x = (POSTER_WIDTH - mw_width) // 2
        mw_y = 200
    
    draw.text((mw_x, mw_y), month_week, font=font_month, fill=color_secondary)
    
    # 2. 日期数字
    date_num = data.get("date", "29")
    date_bbox = draw.textbbox((0, 0), date_num, font=font_date)
    date_width = date_bbox[2] - date_bbox[0]
    date_height = date_bbox[3] - date_bbox[1]
    
    if positions['date'] == 'center':
        date_x = (POSTER_WIDTH - date_width) // 2
        date_y = 380
    elif positions['date'] == 'top_center_below':
        date_x = (POSTER_WIDTH - date_width) // 2
        date_y = 300
    elif positions['date'] == 'center_left':
        date_x = 150
        date_y = 400
    else:
        date_x = (POSTER_WIDTH - date_width) // 2
        date_y = 380
    
    draw.text((date_x, date_y), date_num, font=font_date, fill=color_primary)
    
    # 3. 农历
    nongli = data.get("nongli", "二月初一")
    nl_bbox = draw.textbbox((0, 0), nongli, font=font_nongli)
    nl_width = nl_bbox[2] - nl_bbox[0]
    nl_x = (POSTER_WIDTH - nl_width) // 2
    nl_y = date_y + date_height + 150
    draw.text((nl_x, nl_y), nongli, font=font_nongli, fill=color_secondary)
    
    # 4. 干支
    bazi = data.get("bazi", "丙午 · 辛卯 · 壬寅")
    bz_bbox = draw.textbbox((0, 0), bazi, font=font_bazi)
    bz_width = bz_bbox[2] - bz_bbox[0]
    bz_x = (POSTER_WIDTH - bz_width) // 2
    bz_y = nl_y + 80
    draw.text((bz_x, bz_y), bazi, font=font_bazi, fill=color_primary)
    
    # 5. 利弊（带精致icon）
    li = data.get("li", "立券交易兴")
    bi = data.get("bi", "嫁娶择日宜")
    
    # 利（用小型装饰符号，更优雅）
    # 使用 Unicode 装饰符号
    li_icon = "❖"  # 菱形装饰
    li_text = f"{li_icon}  {li}"
    li_bbox = draw.textbbox((0, 0), li_text, font=font_li_bi)
    li_width = li_bbox[2] - li_bbox[0]
    li_x = (POSTER_WIDTH - li_width) // 2
    li_y = POSTER_HEIGHT - 300
    draw.text((li_x, li_y), li_text, font=font_li_bi, fill=color_accent)
    
    # 弊（用另一种装饰符号）
    bi_icon = "◇"  # 空心菱形
    bi_text = f"{bi_icon}  {bi}"
    bi_bbox = draw.textbbox((0, 0), bi_text, font=font_li_bi)
    bi_width = bi_bbox[2] - bi_bbox[0]
    bi_x = (POSTER_WIDTH - bi_width) // 2
    bi_y = POSTER_HEIGHT - 230
    draw.text((bi_x, bi_y), bi_text, font=font_li_bi, fill=color_accent)
    
    # 保存
    img = img.convert('RGB')
    img.save(output_path, quality=95)
    print(f"✅ 海报已生成: {output_path}")
    
    return output_path, layout

def validate_poster(image_path, layout):
    """验证海报"""
    print(f"\n🔍 验证海报...")
    print(f"  布局方案: {layout['description']}")
    # TODO: 用 VL 模型验证
    return True

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
    
    output, layout = create_poster_dynamic("bg-new.jpg", "test_poster_v5.jpg", data)
    validate_poster(output, layout)