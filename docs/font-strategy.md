# 字体品味策略 - 基于 Frontend Design 原则

## 📖 学习自 Frontend Design Skill

### 核心原则

1. **避免通用字体** - 不使用 Arial、Inter、Roboto 等常见字体
2. **选择独特字体** - 使用有特色的字体，提升美学质感
3. **字体配对** - 展示字体 + 正文字体配对
4. **美学一致性** - 字体选择要符合整体美学方向

---

## 🎨 当前字体配置

### 现有字体

**展示字体（数字）**:
- Noto Sans Black (最粗黑体)
- 用途: 超大数字（420px）
- 问题: 过于通用，缺乏特色

**正文字体（中文/英文）**:
- Noto Sans Bold (粗黑体)
- 用途: 农历、干支、利弊（32-38px）
- 问题: 过于通用，缺乏特色

---

## 💡 改进策略

### 方案A：思源宋体 + 思源黑体（优雅对比）

**展示字体**:
- 字体: Noto Serif CJK Bold (思源宋体粗体)
- 用途: 超大数字（450px）
- 特点: 优雅、有书法感

**正文字体**:
- 字体: Noto Sans CJK Regular (思源黑体常规)
- 用途: 农历、干支、利弊（36-40px）
- 特点: 清晰、易读

**美学方向**: 优雅、禅意、东方美学

---

### 方案B：文泉驿正黑 + 思源黑体（现代简约）

**展示字体**:
- 字体: WenQuanYi Zen Hei Sharp (文泉驿正黑锐利)
- 用途: 超大数字（420px）
- 特点: 现代、锐利、有力度

**正文字体**:
- 字体: Noto Sans CJK Light (思源黑体细体)
- 用途: 农历、干支、利弊（32-36px）
- 特点: 轻盈、透气

**美学方向**: 现代简约、轻盈透气

---

### 方案C：方正黑体 + 方正宋体（出版级品质）

**展示字体**:
- 字体: FZHei-B01 (方正黑体)
- 用途: 超大数字（450px）
- 特点: 出版级、有权威感

**正文字体**:
- 字体: FZSong-B02 (方正宋体)
- 用途: 农历、干支、利弊（36-40px）
- 特点: 精致、优雅

**美学方向**: 精致出版、权威感

---

### 方案D：动态字体（根据日期变化）

**每个日期使用不同风格**:
- 1, 4, 7: 禅意风格（思源宋体）
- 2, 5, 8: 现代风格（文泉驿正黑）
- 3, 6, 9: 出版风格（方正黑体）
- 0: 混合风格（粗细对比）

**美学方向**: 多样性、每天都有新意

---

## 🔧 实现方案

### 步骤1：检查可用字体

```python
from PIL import ImageFont
import os

fonts = [
    "/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Light.ttc",
    "/usr/share/fonts/truetype/wqy-zenhei/wqy-zenhei-sharp.ttc",
]

for font in fonts:
    if os.path.exists(font):
        print(f"✅ {font}")
    else:
        print(f"❌ {font}")
```

### 步骤2：更新脚本字体配置

```python
# 展示字体（根据方案选择）
DISPLAY_FONT = "/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc"
FONT_SIZE_DISPLAY = 450

# 正文字体
BODY_FONT = "/usr/share/fonts/opentype/noto/NotoSansCJK-Light.ttc"
FONT_SIZE_BODY = 38
```

### 步骤3：测试不同字体组合

生成多个版本，选择最佳。

---

## 📊 字体美学评分

### 评分标准

1. **独特性** (30分)
   - 是否避免通用字体
   - 是否有特色

2. **可读性** (25分)
   - 是否清晰易读
   - 层次是否分明

3. **美学一致性** (25分)
   - 是否符合整体美学方向
   - 配色是否协调

4. **视觉冲击力** (20分)
   - 是否有记忆点
   - 是否令人印象深刻

### 当前配置评分

- Noto Sans Black + Bold: 55/100
  - 独特性: 10/30（太通用）
  - 可读性: 20/25（清晰）
  - 一致性: 15/25（一般）
  - 冲击力: 10/20（缺乏）

### 方案A（思源宋体）评分: 75/100
- 独特性: 20/30（较好）
- 可读性: 18/25（清晰）
- 一致性: 22/25（禅意风格一致）
- 冲击力: 15/20（有特色）

---

## 🎯 推荐方案

**立即实施**: 方案A（思源宋体 + 思源黑体）

**理由**:
1. 适合诧寂风、东方美学
2. 字体优雅，有书法感
3. 符合小清新美学定位
4. 可读性好

**后续优化**: 方案D（动态字体）

**理由**:
1. 增加多样性
2. 每天都有新鲜感
3. 避免审美疲劳

---

## 📝 行动清单

- [ ] 检查系统可用字体
- [ ] 选择方案A字体
- [ ] 更新 poster_template_blocks.py
- [ ] 生成测试版本
- [ ] 对比效果
- [ ] 实施方案A
- [ ] 计划方案D

---

**更新时间**: 2026-03-30
**参考**: Frontend Design Skill (https://github.com/anthropics/skills/tree/main/skills/frontend-design)
