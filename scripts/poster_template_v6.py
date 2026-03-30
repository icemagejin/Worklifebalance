#!/usr/bin/env python3
"""
日历海报生成脚本 v6 - VL 驱动的智能布局
使用 VL 模型进行：
1. 图形位置检测
2. 排版建议
3. 美学验证
"""

from PIL import Image, ImageDraw, ImageFont
import sys
import os
import json
import base64
import requests

POSTER_WIDTH = 1080
POSTER_HEIGHT = 1920

# VL 模型配置
VL_MODEL = "qwen-vl-max"
VL_API = "https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation"

FONT_SANS_BOLD = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
FONT_SERIF_REGULAR = "/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc"

def get_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except:
        return ImageFont.load_default()

def image_to_base64(image_path):
    """将图片转为 base64"""
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode('utf-8')

def call_vl_model(image_path, prompt):
    """
    调用 VL 模型分析图片
    """
    # 读取图片
    img_base64 = image_to_base64(image_path)
    
    # 构建请求
    # 这里需要根据实际的 API 配置
    # 暂时返回模拟结果
    
    print(f"🔮 VL 分析中: {prompt}")
    
    # 模拟返回
    return {
        "图形位置": "右下角",
        "空白区域": ["顶部", "左侧", "中间偏上"],
        "排版建议": "日期数字居中偏上，农历和干支在中间，利弊在底部居中",
        "美学评分": 7,
        "改进建议": "可以增加文字与图形的距离，让布局更透气"
    }

def analyze_background_with_vl(bg_path):
    """
    用 VL 模型分析背景图
    返回：图形位置、空白区域、排版建议
    """
    prompt = """
    分析这张背景图：
    1. 主要图形在哪个位置？（左上/右上/左下/右下/中间/散布）
    2. 哪些区域是空白的适合放文字？
    3. 给出文字排版建议：
       - 日期数字应该放在哪里？
       - 农历和干支应该放在哪里？
       - 利弊文字应该放在哪里？
    4. 美学评分（1-10分）
    5. 改进建议
    
    请以 JSON 格式返回。
    """
    
    result = call_vl_model(bg_path, prompt)
    return result

def create_layout_from_vl_analysis(analysis):
    """
    根据 VL 分析结果生成布局参数
    """
    layout = {
        'month_week': {'x': None, 'y': 200},
        'date': {'x': None, 'y': 400},
        'nongli': {'x': None, 'y': 750},
        'bazi': {'x': None, 'y': 850},
        'li_bi': {'x': None, 'y': POSTER_HEIGHT - 300}
    }
    
    # 根据 VL 分析调整位置
    # 这里需要更复杂的逻辑
    
    return layout

def create_poster_with_vl(bg_path, output_path, data):
    """
    VL 驱动的海报生成
    """
    
    # 1. 用 VL 分析背景
    print("\n📊 Step 1: 分析背景图...")
    analysis = analyze_background_with_vl(bg_path)
    print(f"  图形位置: {analysis.get('图形位置', '未知')}")
    print(f"  空白区域: {analysis.get('空白区域', [])}")
    print(f"  排版建议: {analysis.get('排版建议', '无')}")
    
    # 2. 根据 VL 建议生成布局
    print("\n📐 Step 2: 生成布局...")
    layout = create_layout_from_vl_analysis(analysis)
    
    # 3. 创建海报
    print("\n🎨 Step 3: 绘制海报...")
    
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
    
    # 颜色（根据背景调整）
    color_primary = (50, 40, 35)
    color_secondary = (80, 65, 55)
    color_accent = (100, 85, 70)
    
    # 文字
    month = data.get("month", "MAR")
    week = data.get("week", "SAT")
    month_week = f"{month} · {week}"
    
    mw_bbox = draw.textbbox((0, 0), month_week, font=font_month)
    mw_width = mw_bbox[2] - mw_bbox[0]
    mw_x = (POSTER_WIDTH - mw_width) // 2
    draw.text((mw_x, 200), month_week, font=font_month, fill=color_secondary)
    
    date_num = data.get("date", "29")
    date_bbox = draw.textbbox((0, 0), date_num, font=font_date)
    date_width = date_bbox[2] - date_bbox[0]
    date_height = date_bbox[3] - date_bbox[1]
    date_x = (POSTER_WIDTH - date_width) // 2
    draw.text((date_x, 400), date_num, font=font_date, fill=color_primary)
    
    nongli = data.get("nongli", "二月初一")
    nl_bbox = draw.textbbox((0, 0), nongli, font=font_nongli)
    nl_width = nl_bbox[2] - nl_bbox[0]
    nl_x = (POSTER_WIDTH - nl_width) // 2
    draw.text((nl_x, 750), nongli, font=font_nongli, fill=color_secondary)
    
    bazi = data.get("bazi", "丙午 · 辛卯 · 壬寅")
    bz_bbox = draw.textbbox((0, 0), bazi, font=font_bazi)
    bz_width = bz_bbox[2] - bz_bbox[0]
    bz_x = (POSTER_WIDTH - bz_width) // 2
    draw.text((bz_x, 850), bazi, font=font_bazi, fill=color_primary)
    
    li = data.get("li", "立券交易兴")
    bi = data.get("bi", "嫁娶择日宜")
    
    li_text = f"❖  {li}"
    li_bbox = draw.textbbox((0, 0), li_text, font=font_li_bi)
    li_width = li_bbox[2] - li_bbox[0]
    li_x = (POSTER_WIDTH - li_width) // 2
    draw.text((li_x, POSTER_HEIGHT - 300), li_text, font=font_li_bi, fill=color_accent)
    
    bi_text = f"◇  {bi}"
    bi_bbox = draw.textbbox((0, 0), bi_text, font=font_li_bi)
    bi_width = bi_bbox[2] - bi_bbox[0]
    bi_x = (POSTER_WIDTH - bi_width) // 2
    draw.text((bi_x, POSTER_HEIGHT - 230), bi_text, font=font_li_bi, fill=color_accent)
    
    # 保存
    img = img.convert('RGB')
    img.save(output_path, quality=95)
    print(f"✅ 海报已生成: {output_path}")
    
    # 4. VL 验证
    print("\n🔍 Step 4: VL 验证...")
    validation = call_vl_model(output_path, """
    验证这张海报：
    1. 文字是否清晰可读？
    2. 排版是否美观？
    3. 文字和背景图形是否有冲突？
    4. 整体评分（1-10分）
    5. 如果不满意，给出具体的改进建议
    
    请以 JSON 格式返回。
    """)
    
    print(f"  评分: {validation.get('美学评分', '?')}/10")
    print(f"  建议: {validation.get('改进建议', '无')}")
    
    return output_path, analysis, validation

def iterate_until_good_vl(bg_path, output_path, data, max_iterations=5):
    """
    VL 驱动的迭代生成
    """
    for i in range(max_iterations):
        print(f"\n{'='*60}")
        print(f"迭代 {i+1}/{max_iterations}")
        print(f"{'='*60}")
        
        output, analysis, validation = create_poster_with_vl(bg_path, output_path, data)
        
        score = validation.get('美学评分', 0)
        if score >= 8:
            print("\n✅ 验证通过！")
            return output
        
        print(f"\n⚠️  评分 {score}/10，需要改进...")
        print(f"改进建议: {validation.get('改进建议', '无')}")
        
        # TODO: 根据建议调整参数
    
    print("\n⚠️  达到最大迭代次数")
    return output

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
    
    iterate_until_good_vl("bg_light_ink.jpg", "test_poster_v6.jpg", data)