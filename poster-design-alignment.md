# 八字合盘海报 - 审美对齐记录

> 本文件记录每次海报生成的审美调整和结论，确保持续对齐弗尼的审美偏好。
>
> **最后更新**：2026-03-26
> **同步频率**：每两天一次到 GitHub
> **GitHub 仓库**：https://github.com/icemagejin/Worklifebalance.git

---

## 审美核心原则

### 整体风格
- ✅ 现代国画写意风格
- ✅ 国画机制简约风，留白克制
- ✅ 极简留白，iPhone全屏
- ✅ 小清新设计风格

### 配色方案
- 暖色光晕（代表火元素）
- 淡绿色墨线（代表木元素）
- 柔和色调，不刺眼

---

## 历史调整记录

### 2026-03-26 - 第1次生成及调整

#### 初始问题
1. ❌ 背景图尺寸错误（横屏被拉伸到竖屏）
2. ❌ 中文显示为方块（字体不支持中文）
3. ❌ 字体粗细对比不清晰

#### 解决方案

**问题1：背景图尺寸**
- 原因：使用默认 `2K` 尺寸生成横屏图片
- 解决：指定 `--size 1080x1920` 生成竖屏图片
- 命令：
  ```bash
  node /workspace/projects/extensions/coze-openclaw-plugin/skills/coze-image-gen/scripts/gen.mjs \
    --prompt "Modern Chinese ink painting style, minimalist composition with restrained negative space,
    one warm orange glow representing fire element, several light green ink strokes representing wood element,
    elegant and ethereal, no text, no characters, pure visual art, vertical portrait orientation, high quality" \
    --size 1080x1920
  ```

**问题2：中文方块**
- 原因：PIL 默认字体不支持中文
- 解决：安装 `fonts-noto-cjk` 中文字体包
- 命令：
  ```bash
  apt-get install -y fonts-noto-cjk
  fc-cache -fv
  ```

**问题3：字体粗细对比**
- 原因：所有文字使用相同字重
- 解决：创建字体组合对比
- 字体方案：
  - 超大数字：**Noto Sans CJK Bold**（粗体，字号480）
  - 祝福语/干支：**Noto Serif CJK Regular**（细体优雅，字号48）
  - 英文日期：**Noto Sans CJK Regular**（常规，字号36）

#### 最终配置

**海报尺寸**
- 宽度：1080px
- 高度：1920px
- 比例：9:16（iPhone 全屏）

**背景图要求**
- 使用 coze-image-gen 生成
- prompt 必须包含：
  - `Modern Chinese ink painting style`
  - `minimalist composition with restrained negative space`
  - `vertical portrait orientation`
  - `no text, no characters`
  - 具体元素描述（如：`warm orange glow`, `light green ink strokes`）
- 尺寸：`1080x1920`

**字体组合**
```python
# 大数字（粗体）
large_font = ImageFont.truetype("/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc", 480, index=0)

# 祝福语/干支（细体优雅）
serif_font = ImageFont.truetype("/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc", 48, index=0)

# 英文日期（常规）
regular_font = ImageFont.truetype("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc", 36, index=0)
```

**文字位置**
- 大数字：`(width // 2, 600)` 居中
- 英文日期：`(width // 2, 900)` 居中
- 干支：`(width // 2, 950)` 居中
- 祝福语第1行：`(width // 2, 1300)` 居中
- 祝福语第2行：`(width // 2, 1370)` 居中

**文字颜色**
- 主要文字（数字、祝福语）：`#1a1a1a`（深灰近黑）
- 次要文字（日期、干支）：`#666666`（中灰）

**背景遮罩**
- 透明度：80（`rgba(255, 255, 255, 80)`）
- 作用：让文字在背景图上更清晰

#### 脚本位置
`/workspace/projects/workspace-aesthetic/scripts/generate-poster.py`

---

## 审美检查清单

每次生成前检查：

- [ ] 背景图使用 `coze-image-gen` 生成
- [ ] 背景图尺寸：1080x1920（竖屏）
- [ ] prompt 包含 `vertical portrait orientation`
- [ ] prompt 包含 `no text, no characters`
- [ ] 字体组合：Sans Bold + Serif Regular
- [ ] 大数字字号：480
- [ ] 祝福语字号：48
- [ ] 日期字号：36
- [ ] 文字颜色正确（主文字 #1a1a1a，次要文字 #666666）
- [ ] 背景遮罩透明度：80
- [ ] 祝福语：6字对仗，体现今日干支意境
- [ ] 干支格式：`年月·日`（如：丙午·甲午）

---

## 优化方向（待讨论）

- [ ] 是否需要调整数字大小？
- [ ] 是否需要调整祝福语字间距？
- [ ] 背景图遮罩透明度是否合适？
- [ ] 是否需要更多的留白？
