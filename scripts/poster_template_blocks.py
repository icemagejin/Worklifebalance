#!/usr/bin/env python3
"""
日历海报 - 块面结构版
核心改进：
1. 字体有力度（黑体+粗宋）
2. 块面结构（左右分区）
3. 不只是居中，有空间划分
4. 支持命令行参数，方便 Agent 动态调整
"""

from PIL import Image, ImageDraw, ImageFont
import sys
import os
import json

POSTER_WIDTH = 1080
POSTER_HEIGHT = 1920

FONT_SANS_BOLD = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
FONT_SANS_BLACK = "/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc"  # 最粗

def get_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except:
        return ImageFont.load_default()

def create_poster_with_blocks(bg_path, output_path, data, layout_type="center", params=None):
    """
    块面结构设计

    Args:
        bg_path: 背景图路径
        output_path: 输出路径
        data: 数据字典
        layout_type: 布局类型
        params: 参数调整
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
    # 字号（可以从 params 覆盖）
    size_month = params.get('size_month', 32)
    size_date = params.get('size_date', 420)
    size_info = params.get('size_info', 38)
    size_li_bi = params.get('size_li_bi', 36)

    # 位置偏移
    offset_date_y = params.get('offset_date_y', 280)
    offset_info_y = params.get('offset_info_y', 780)
    offset_li_bi_y = params.get('offset_li_bi_y', POSTER_HEIGHT - 550)

    # ========== 字体（有力度）==========
    font_month = get_font(FONT_SANS_BOLD, size_month)
    font_date = get_font(FONT_SANS_BLACK, size_date)
    font_info = get_font(FONT_SANS_BOLD, size_info)
    font_li_bi = get_font(FONT_SANS_BOLD, size_li_bi)

    # ========== 颜色（有力度）==========
    color_primary = (30, 25, 20)       # 深黑（有力）
    color_secondary = (70, 60, 50)     # 中深
    color_accent = (50, 45, 40)        # 强调

    # ========== 块面结构 ==========
    # 上半部分：数字（大块面）
    # 中间部分：农历+干支（左侧块面或居中）
    # 下半部分：利弊（左侧块面或居中）

    # 根据图形位置调整
    if layout_type == "right_bottom":
        # 图形在右下 → 文字块面在左
        info_x = 100
    elif layout_type == "left_bottom":
        # 图形在左下 → 文字块面在右
        info_x = POSTER_WIDTH - 400
    else:
        # 其他情况 → 居中
        info_x = POSTER_WIDTH // 2

    # ========== 上半部分：超大数字（核心块面）==========
    date_num = data.get("date", "29")
    date_bbox = draw.textbbox((0, 0), date_num, font=font_date)
    date_width = date_bbox[2] - date_bbox[0]
    date_height = date_bbox[3] - date_bbox[1]
    date_x = (POSTER_WIDTH - date_width) // 2  # 数字居中
    draw.text((date_x, offset_date_y), date_num, font=font_date, fill=color_primary)

    # ========== 英文月份（顶部小块面）==========
    month = data.get("month", "MAR")
    week = data.get("week", "SAT")
    month_week = f"{month} · {week}"

    mw_bbox = draw.textbbox((0, 0), month_week, font=font_month)
    mw_width = mw_bbox[2] - mw_bbox[0]
    mw_x = (POSTER_WIDTH - mw_width) // 2
    draw.text((mw_x, 160), month_week, font=font_month, fill=color_secondary)

    # ========== 中间部分：信息块面 ==========
    # 农历
    nongli = data.get("nongli", "二月初一")
    if layout_type == "center":
        draw.text((info_x, offset_info_y), nongli, font=font_info, fill=color_primary, anchor="mm")
    else:
        draw.text((info_x, offset_info_y), nongli, font=font_info, fill=color_primary)

    # 干支
    bazi = data.get("bazi", "丙午 · 辛卯 · 壬寅")
    bazi_y = offset_info_y + 100
    if layout_type == "center":
        draw.text((info_x, bazi_y), bazi, font=font_info, fill=color_secondary, anchor="mm")
    else:
        draw.text((info_x, bazi_y), bazi, font=font_info, fill=color_secondary)

    # ========== 下半部分：利弊块面 ==========
    li = data.get("li", "立券交易兴")
    bi = data.get("bi", "嫁娶择日宜")

    if layout_type == "right_bottom":
        li_bi_y = POSTER_HEIGHT - 550
    elif layout_type == "left_bottom":
        li_bi_y = POSTER_HEIGHT - 320
    else:
        li_bi_y = POSTER_HEIGHT - 320

    # 利弊块面
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

    return output_path

def print_usage():
    print("用法: python poster_template_blocks.py <背景图路径> <输出路径> <数据JSON> [布局类型] [参数JSON]")
    print("")
    print("参数:")
    print("  背景图路径:  必填，背景图片文件路径")
    print("  输出路径:    必填，输出图片路径")
    print("  数据JSON:    必填，JSON格式的数据（包含 month, week, date, nongli, bazi, li, bi）")
    print("  布局类型:    可选，center|right_bottom|left_bottom，默认 center")
    print("  参数JSON:    可选，参数调整（size_date, size_info, offset_date_y 等）")
    print("")
    print("示例:")
    print('  python poster_template_blocks.py bg.jpg output.jpg \'{"month":"MAR","week":"SAT","date":"29","nongli":"二月初一","bazi":"丙午 · 辛卯 · 壬寅","li":"立券交易兴","bi":"嫁娶择日宜"}\' right_bottom')
    print('  python poster_template_blocks.py bg.jpg output.jpg \'{"month":"MAR","week":"SAT","date":"29"}\' center \'{"size_date": 450}\'')

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print_usage()
        sys.exit(1)

    bg_path = sys.argv[1]
    output_path = sys.argv[2]
    data_json = sys.argv[3]
    layout_type = sys.argv[4] if len(sys.argv) > 4 else "center"
    params_json = sys.argv[5] if len(sys.argv) > 5 else None

    try:
        data = json.loads(data_json)
        params = json.loads(params_json) if params_json else {}
    except json.JSONDecodeError as e:
        print(f"❌ JSON 解析失败: {e}")
        sys.exit(1)

    create_poster_with_blocks(bg_path, output_path, data, layout_type, params)
