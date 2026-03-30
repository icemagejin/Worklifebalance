#!/usr/bin/env python3
"""
八字合盘海报生成器 - 完整版（带 VL 检查）
"""

import sys
import os
import json
import requests
import base64
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

# 添加路径
sys.path.append(os.path.dirname(__file__))
from vl_validator import analyze_background_layout, validate_poster_layout

POSTER_WIDTH = 1080
POSTER_HEIGHT = 1920

FONT_SANS_BOLD = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
FONT_SANS_BLACK = "/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc"

def get_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except:
        return ImageFont.load_default()

def generate_bg_image():
    """
    生成轻盈淡雅水墨背景
    """
    print("🎨 生成背景图...")

    # 使用 coze-image-gen 生成背景
    # 这里需要调用 coze-image-gen 工具
    # 由于在 Python 脚本中，我们直接调用 API

    bg_prompt = """
Minimalist Chinese ink wash painting, very light and ethereal,
soft ink strokes in one corner only, mostly white space,
pastel colors, elegant, no text, no characters, 1080x1920
"""

    # 调用 coze 图像生成 API
    api_url = "https://api.coze.com/open_api/v2/chat"
    api_key = os.getenv("COZE_API_KEY", "")

    if not api_key:
        print("⚠️ 未配置 COZE_API_KEY，使用默认背景")
        # 创建默认白色背景
        bg = Image.new('RGB', (POSTER_WIDTH, POSTER_HEIGHT), '#FAFAFA')
        bg_path = "/tmp/bg_default.jpg"
        bg.save(bg_path, quality=95)
        return bg_path

    try:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "bot_id": "7380000000000000",
            "user": "aesthetic_agent",
            "query": bg_prompt,
            "stream": False
        }

        response = requests.post(api_url, headers=headers, json=payload, timeout=60)
        result = response.json()

        # 解析图片 URL
        if "messages" in result and len(result["messages"]) > 0:
            for msg in result["messages"]:
                if "content" in msg and "type" in msg:
                    if msg["type"] == "answer":
                        content = msg["content"]
                        # 提取图片 URL
                        import re
                        url_match = re.search(r'https://[^\s"]+\.(jpg|png|jpeg)', content)
                        if url_match:
                            img_url = url_match.group()

                            # 下载图片
                            img_response = requests.get(img_url, timeout=30)
                            bg_path = "/tmp/bg_generated.jpg"
                            with open(bg_path, 'wb') as f:
                                f.write(img_response.content)

                            print(f"✅ 背景图已生成: {bg_path}")
                            return bg_path

    except Exception as e:
        print(f"⚠️ 背景生成失败: {e}")

    # 失败时使用默认背景
    bg = Image.new('RGB', (POSTER_WIDTH, POSTER_HEIGHT), '#FAFAFA')
    bg_path = "/tmp/bg_default.jpg"
    bg.save(bg_path, quality=95)
    return bg_path

def create_poster(bg_path, output_path, data, layout_type="center"):
    """
    生成海报
    """
    print(f"📝 生成海报 (布局: {layout_type})...")

    # 打开背景
    if os.path.exists(bg_path):
        img = Image.open(bg_path)
        if img.size != (POSTER_WIDTH, POSTER_HEIGHT):
            img = img.resize((POSTER_WIDTH, POSTER_HEIGHT), Image.Resampling.LANCZOS)
    else:
        img = Image.new('RGB', (POSTER_WIDTH, POSTER_HEIGHT), '#FAFAFA')

    img = img.convert('RGBA')
    draw = ImageDraw.Draw(img)

    # 字体
    font_month = get_font(FONT_SANS_BOLD, 32)
    font_date = get_font(FONT_SANS_BLACK, 420)
    font_info = get_font(FONT_SANS_BOLD, 38)
    font_li_bi = get_font(FONT_SANS_BOLD, 36)

    # 颜色
    color_primary = (30, 25, 20)
    color_secondary = (70, 60, 50)
    color_accent = (50, 45, 40)

    # 根据布局调整
    if layout_type == "right_bottom":
        info_x = 120
    elif layout_type == "left_bottom":
        info_x = POSTER_WIDTH - 400
    else:
        info_x = POSTER_WIDTH // 2 - 150

    # 英文月份
    month = data.get("month", "MAR")
    week = data.get("week", "SAT")
    month_week = f"{month} · {week}"

    mw_bbox = draw.textbbox((0, 0), month_week, font=font_month)
    mw_width = mw_bbox[2] - mw_bbox[0]
    mw_x = (POSTER_WIDTH - mw_width) // 2
    draw.text((mw_x, 160), month_week, font=font_month, fill=color_secondary)

    # 数字
    date_num = data.get("date", "29")
    date_bbox = draw.textbbox((0, 0), date_num, font=font_date)
    date_width = date_bbox[2] - date_bbox[0]
    date_x = (POSTER_WIDTH - date_width) // 2
    draw.text((date_x, 280), date_num, font=font_date, fill=color_primary)

    # 农历 + 干支
    nongli = data.get("nongli", "二月初一")
    bazi = data.get("bazi", "丙午 · 辛卯 · 壬寅")

    if layout_type == "center":
        draw.text((info_x, 780), nongli, font=font_info, fill=color_primary, anchor="mm")
        draw.text((info_x, 880), bazi, font=font_info, fill=color_secondary, anchor="mm")
    else:
        draw.text((info_x, 780), nongli, font=font_info, fill=color_primary)
        draw.text((info_x, 880), bazi, font=font_info, fill=color_secondary)

    # 利弊
    li = data.get("li", "立券交易兴")
    bi = data.get("bi", "嫁娶择日宜")

    if layout_type == "right_bottom":
        li_bi_y = POSTER_HEIGHT - 550
    else:
        li_bi_y = POSTER_HEIGHT - 320

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

def get_today_data():
    """
    获取今日数据
    """
    today = datetime.now()

    # 简化版数据（实际应该从 API 获取）
    data = {
        "month": today.strftime("%b").upper(),
        "week": today.strftime("%a").upper(),
        "date": today.strftime("%d"),
        "nongli": "二月初二",  # 示例
        "bazi": "丙午 · 辛卯 · 壬寅",  # 示例
        "li": "祭祀祈福吉",
        "bi": "出行远避"
    }

    return data

def main():
    print("=" * 50)
    print("🎨 八字合盘海报生成器（带 VL 检查）")
    print("=" * 50)

    # 1. 获取今日数据
    print("\n📅 获取今日数据...")
    data = get_today_data()

    # 2. 生成背景图
    bg_path = generate_bg_image()

    # 3. VL 分析背景布局
    print("\n🔍 VL 分析背景布局...")
    layout_result = analyze_background_layout(bg_path)

    if layout_result["success"]:
        layout_type = layout_result["layout_type"]
        print(f"✅ 布局类型: {layout_type}")
        if "raw_content" in layout_result:
            print(f"   分析: {layout_result['raw_content'][:200]}...")
    else:
        layout_type = "center"
        print(f"⚠️ VL 分析失败，使用默认布局: center")

    # 4. 生成海报
    output_path = f"/workspace/projects/workspace-aesthetic/posters/poster-{datetime.now().strftime('%Y-%m-%d')}.jpg"
    create_poster(bg_path, output_path, data, layout_type)

    # 5. VL 验证海报
    print("\n🔍 VL 验证海报质量...")
    validation_result = validate_poster_layout(output_path)

    if validation_result["success"]:
        if "analysis" in validation_result and validation_result["analysis"]:
            analysis = validation_result["analysis"]
            score = analysis.get("score", 0)

            print(f"\n📊 验证结果:")
            print(f"   评分: {score}/100")
            print(f"   文字重叠: {'是' if analysis.get('has_overlap') else '否'}")
            print(f"   遮挡背景: {'是' if analysis.get('blocks_background') else '否'}")
            print(f"   留白充足: {'是' if analysis.get('has_enough_whitespace') else '否'}")

            if "issues" in analysis and analysis["issues"]:
                print(f"\n⚠️ 发现问题:")
                for issue in analysis["issues"]:
                    print(f"   - {issue}")

            if score < 60:
                print(f"\n❌ 评分过低 ({score})，建议调整参数重试")
                return False
            else:
                print(f"\n✅ 验证通过 (评分: {score})")
        else:
            print(f"⚠️ 无法解析验证结果")
            print(f"原始内容: {validation_result.get('raw_content', '')[:300]}...")
    else:
        print(f"⚠️ VL 验证失败: {validation_result.get('reason', 'unknown')}")

    print(f"\n🎉 海报已保存: {output_path}")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
