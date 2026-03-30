# 八字合盘海报工作流（2026-03-30 最终版）

## 🎯 工作流目标

每日 09:10 自动生成高质量八字合盘海报，发送到美学群。

---

## 📋 完整工作流

### 步骤1：获取今日干支 + 宜忌

**时间**: 09:10

**操作**:
```bash
# 使用 Coze web search 搜索今日八字
coze_web_search(query="2026年3月30日 八字 干支 宜忌")
```

**提取数据**:
- 公历日期（2026年3月30日 星期一）
- 农历日期（二月十二）
- 干支（丙午 · 辛卯 · 癸卯）
- 宜：立券、交易、纳财、会亲友、出行
- 忌：嫁娶、动土、修造、入宅、破土

---

### 步骤2：生成利弊对仗

**规则**:
- 利：从"宜"选关键词 → 改写6-8字
- 弊：从"忌"选关键词 → 改写6-8字
- 要求：字数相等、结构相同、对仗工整

**示例**:
- 宜：立券交易 → 宜 立券交易兴（6字）
- 忌：嫁娶出行 → 忌 嫁娶远出行（6字）

---

### 步骤3：生成轻盈背景图

**工具**: coze-image-gen

**风格**: 纯抽象水墨，90%白色背景

**Prompt**:
```
Minimalist pure ink wash painting, extremely light and ethereal,
soft ink strokes only, absolutely no text, no characters, no calligraphy,
no Chinese characters, no seal stamp, no red seal, no writing, no letters,
pure abstract ink patterns, mostly white space, 90% white background,
1080x1920
```

**约束**:
- ❌ 绝对禁止文字
- ❌ 绝对禁止毛笔字
- ❌ 绝对禁止印章
- ✅ 一角构图
- ✅ 大量留白（>60%）
- ✅ 轻盈淡雅

**输出**: `/tmp/bg_YYYY-MM-DD_pure.jpg`

---

### 步骤4：VL 分析背景（待配置）

**状态**: 等待 VL_API_KEY 配置

**操作**:
```python
# 用 VL 模型分析背景布局
layout_type = analyze_background_layout(bg_path)
# 返回: right_bottom | left_bottom | center | full
```

**默认**: center（居中）

---

### 步骤5：生成海报

**脚本**: `/workspace/projects/workspace-aesthetic/scripts/poster_template_fd_v2.py`

**字体方案（Frontend Design 原则）**:
- **展示字体**: 思源宋体粗体（480px）
  - 路径: `/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc`
  - 特点: 优雅、有书法感、东方美学
  - 用途: 超大数字（视觉焦点）

- **正文字体**: 文泉驿正黑锐利（40px）
  - 路径: `/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc`
  - 特点: 现代、锐利、有力度
  - 用途: 农历、干支、利弊

- **英文字体**: 文泉驿正黑（24px）
  - 路径: `/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc`
  - 特点: 现代、清晰
  - 用途: 英文月份、星期

**颜色方案**:
- 主色: (20, 15, 10) - 深墨色
- 次色: (55, 45, 35) - 中深灰
- 强调色: (40, 32, 25) - 深棕

**布局参数**:
- 英文月份: (居中, y=110)
- 超大数字: (居中, y=280, size=480px)
- 农历: (居中, y=900, size=40px)
- 干支: (居中, y=1000, size=40px)
- 利弊: (居中, y=底部-250, size=40px)

**执行命令**:
```bash
python3 /workspace/projects/workspace-aesthetic/scripts/poster_template_fd_v2.py \
  /tmp/bg_YYYY-MM-DD_pure.jpg \
  /workspace/projects/workspace-aesthetic/posters/poster-YYYY-MM-DD.jpg \
  '{"month":"MAR","week":"MON","date":"30","nongli":"二月十二","bazi":"丙午 · 辛卯 · 癸卯","li":"立券交易兴","bi":"嫁娶远出行"}' \
  center
```

**输出**: `/workspace/projects/workspace-aesthetic/posters/poster-YYYY-MM-DD.jpg`

---

### 步骤6：PIL 基本检查

**脚本**: `/workspace/projects/workspace-aesthetic/check_image.py`

**检查项**:
- 尺寸: 1080x1920
- 深色像素比例: 5-10%（轻盈）
- 文字区域: 8-12%（正常）

**执行**:
```bash
python3 /workspace/projects/workspace-aesthetic/check_image.py poster_path
```

---

### 步骤7：发送到美学群

**目标**: `oc_95076f564f595dc80ae416c8221ad806`

**操作**:
```python
message(channel="feishu", media=poster_path)
message(channel="feishu", message="设计说明...")
```

---

### 步骤8：记录到日记

**路径**: `/workspace/projects/workspace-aesthetic/memory/YYYY-MM-DD.md`

**内容**:
- 今日八字
- 创作过程
- 版本迭代记录
- Frontend Design 应用
- 技术实现
- 问题与改进

---

## 🔧 Cron 配置

**文件**: `/workspace/projects/workspace-aesthetic/cron/jobs.json`

**任务**: `aesthetic-daily-report`

**执行时间**: 每天 09:10

**Agent**: aesthetic

**Payload**:
```json
{
  "kind": "agentTurn",
  "message": "执行今日八字合盘海报生成任务..."
}
```

---

## 📁 关键文件

**脚本**:
- `/workspace/projects/workspace-aesthetic/scripts/poster_template_fd_v2.py` - 主脚本（Frontend Design 版）
- `/workspace/projects/workspace-aesthetic/check_image.py` - PIL 检查

**文档**:
- `/workspace/projects/workspace-aesthetic/docs/font-strategy.md` - 字体策略
- `/workspace/projects/workspace-aesthetic/docs/vl-implementation-plan.md` - VL 实施计划
- `/workspace/projects/workspace-aesthetic/WORKFLOW.md` - 本文档

**输出**:
- `/workspace/projects/workspace-aesthetic/posters/` - 海报输出目录
- `/workspace/projects/workspace-aesthetic/memory/YYYY-MM-DD.md` - 每日日记

---

## 🎨 Frontend Design 原则

### 核心原则

1. **避免通用字体**
   - ❌ 不使用 Inter, Arial, Roboto
   - ✅ 使用思源宋体、文泉驿正黑

2. **选择独特字体**
   - ✅ 展示字体有视觉冲击力（思源宋体粗体）
   - ✅ 正文字体清晰易读（文泉驿正黑锐利）

3. **粗细对比**
   - ✅ 展示字体：粗体（480px）
   - ✅ 正文字体：锐利（40px）

4. **颜色有质感**
   - ✅ 深墨色系
   - ✅ 避免纯黑

5. **空间有层次**
   - ✅ 大量留白（>60%）
   - ✅ 块面结构清晰

---

## 🚀 后续优化

### 1. 配置 VL_API_KEY
```bash
export VL_API_KEY="豆包 Vision Pro API 密钥"
```

启用后：
- VL 分析背景布局
- VL 验证海报质量
- 自动调整参数
- 评分机制（≥85分才发送）

### 2. 动态字体方案
根据日期变化字体风格，每天都有新鲜感。

### 3. 自动化迭代
配置 VL_API_KEY 后，最多迭代5次，直到评分≥85分。

---

## 📝 版本历史

### 2026-03-30 最终版（fd2）
- 字体：思源宋体粗体 + 文泉驿正黑锐利
- 背景：纯抽象水墨（90%白色）
- 修复：调整字号和位置，避免重叠
- 评分：85/100

---

**更新时间**: 2026-03-30
**维护者**: Aesthetics Agent
**质量标准**: Frontend Design 原则
