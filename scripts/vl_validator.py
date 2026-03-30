#!/usr/bin/env python3
"""
海报 VL 验证器
使用视觉语言模型检查海报质量
"""

import json
import requests
import os

def check_poster_with_vl(image_path, prompt):
    """
    使用 VL 模型分析海报
    """
    try:
        # 转换图片为 base64
        import base64
        with open(image_path, 'rb') as f:
            image_base64 = base64.b64encode(f.read()).decode('utf-8')

        # 调用 VL 模型 API（这里需要根据实际的 VL 模型 API 调整）
        # 假设使用豆包 Vision Pro
        api_url = "https://ark.cn-beijing.volces.com/api/v3/chat/completions"
        api_key = os.getenv("VL_API_KEY", "")

        if not api_key:
            print("⚠️ 未配置 VL_API_KEY，跳过 VL 检查")
            return {"success": False, "reason": "no_api_key"}

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

        payload = {
            "model": "doubao-vision-pro-32k",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_base64}"
                            }
                        },
                        {
                            "type": "text",
                            "text": prompt
                        }
                    ]
                }
            ],
            "max_tokens": 1024
        }

        response = requests.post(api_url, headers=headers, json=payload, timeout=30)
        result = response.json()

        if "choices" in result and len(result["choices"]) > 0:
            content = result["choices"][0]["message"]["content"]
            return {"success": True, "content": content}
        else:
            return {"success": False, "reason": "api_error", "detail": result}

    except Exception as e:
        print(f"⚠️ VL 检查失败: {e}")
        return {"success": False, "reason": "exception", "detail": str(e)}

def validate_poster_layout(image_path):
    """
    验证海报布局
    """
    prompt = """请分析这张海报的布局，检查以下问题：

1. 文字是否有重叠？
2. 文字是否遮挡了背景图形？
3. 留白是否充足（>60%）？
4. 字号层次是否清晰？
5. 块面结构是否清晰？

请用 JSON 格式返回：
{
  "has_overlap": true/false,
  "blocks_background": true/false,
  "has_enough_whitespace": true/false,
  "font_hierarchy_clear": true/false,
  "blocks_clear": true/false,
  "issues": ["问题列表"],
  "score": 0-100
}"""

    result = check_poster_with_vl(image_path, prompt)

    if result["success"]:
        try:
            # 尝试解析 JSON
            import re
            json_match = re.search(r'\{[\s\S]*\}', result["content"])
            if json_match:
                analysis = json.loads(json_match.group())
                return {
                    "success": True,
                    "analysis": analysis,
                    "raw_content": result["content"]
                }
            else:
                # 解析失败，返回原始内容
                return {
                    "success": True,
                    "analysis": None,
                    "raw_content": result["content"]
                }
        except:
            return {
                "success": True,
                "analysis": None,
                "raw_content": result["content"]
            }
    else:
        return result

def analyze_background_layout(image_path):
    """
    分析背景图形布局
    """
    prompt = """请分析这张图片的图形位置，判断布局类型。

返回 JSON：
{
  "layout_type": "right_bottom" | "left_bottom" | "center" | "full",
  "graphic_location": "描述图形位置",
  "empty_areas": ["空白区域列表"]
}"""

    result = check_poster_with_vl(image_path, prompt)

    if result["success"]:
        try:
            import re
            json_match = re.search(r'\{[\s\S]*\}', result["content"])
            if json_match:
                analysis = json.loads(json_match.group())
                return {
                    "success": True,
                    "layout_type": analysis.get("layout_type", "center"),
                    "analysis": analysis,
                    "raw_content": result["content"]
                }
            else:
                # 尝试从文本中提取
                content = result["content"].lower()
                if "right" in content or "右下" in content:
                    layout_type = "right_bottom"
                elif "left" in content or "左下" in content:
                    layout_type = "left_bottom"
                elif "center" in content or "中间" in content:
                    layout_type = "center"
                else:
                    layout_type = "full"

                return {
                    "success": True,
                    "layout_type": layout_type,
                    "analysis": None,
                    "raw_content": result["content"]
                }
        except Exception as e:
            print(f"解析失败: {e}")
            return {
                "success": True,
                "layout_type": "center",
                "analysis": None,
                "raw_content": result["content"]
            }
    else:
        return {"success": False, "layout_type": "center"}

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("用法: python vl_validator.py <图片路径> [check|layout]")
        sys.exit(1)

    image_path = sys.argv[1]
    mode = sys.argv[2] if len(sys.argv) > 2 else "check"

    if mode == "check":
        result = validate_poster_layout(image_path)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif mode == "layout":
        result = analyze_background_layout(image_path)
        print(json.dumps(result, ensure_ascii=False, indent=2))
