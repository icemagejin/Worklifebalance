# 美学 Agent 工作流

## 每日任务

### 1. 八字合盘海报生成（09:10）

**触发方式**：Cron 任务（10 9 * * *）

**工作流程**：

#### 步骤 1：获取今日干支 + 宜忌
- 使用 Coze web search 搜索今日八字
- 提取：公历、农历、干支、宜、忌

#### 步骤 2：生成利弊对仗
- 利：从"宜"选关键词 → 改写6-8字
- 弊：从"忌"选关键词 → 改写6-8字
- 要求：字数相等、对仗工整

#### 步骤 3：生成轻盈背景图
- 工具：`coze-image-gen`
- Prompt：
  ```
  Minimalist wabi-sabi style, abstract color fields,
  muted earth tones, 90% white empty space,
  very subtle ink wash in one corner,
  no mountains, no water, no specific objects,
  pure abstraction with natural imperfections, 1080x1920
  ```
- 输出：`/tmp/bg_YYYY-MM-DD_wabisabi.jpg`

#### 步骤 4：分析背景布局（水平 + 垂直）
- 使用 PIL 分析背景图形位置
- 垂直方向：上中下（各33%）
- 水平方向：左中右（各33%）
- 判断布局类型：right_bottom / left_bottom / right_top / left_top / center / full

**脚本**：
```bash
python3 analyze_background.py /tmp/bg_YYYY-MM-DD_wabisabi.jpg
```

#### 步骤 5：智能排版（避开图形）
- 根据布局类型调整文字位置
- 右上角有图形 → 文字偏左（x=0.35）
- 右下角有图形 → 文字偏左 + 上移
- 左上角有图形 → 文字偏右 + 下移
- 左下角有图形 → 文字偏右 + 上移

**脚本**：
```bash
python3 poster_template_final.py \
  /tmp/bg_YYYY-MM-DD_wabisabi.jpg \
  /workspace/projects/workspace-aesthetic/posters/poster-YYYY-MM-DD.jpg \
  data.json \
  right_bottom
```

#### 步骤 6：验证文字不重叠
- 检查文字区域深色比例（<15%）
- 检查文字与背景图形的重叠
- 确认留白充足（>60%）

**脚本**：
```bash
python3 validate_poster.py /workspace/projects/workspace-aesthetic/posters/poster-YYYY-MM-DD.jpg
```

#### 步骤 7：发送到美学群
- 目标：`oc_95076f564f595dc80ae416c8221ad806`

#### 步骤 8：记录到日记
- 路径：`dailyrepo/aesthetic-journal/YYYY-MM-DD.md`

---

### 2. 美学日记生成（20:00）

**触发方式**：Cron 任务（0 20 * * *）

**工作流程**：

#### 步骤 1：生成日记模板
- 运行脚本：`bash scripts/generate-diary.sh`
- 生成路径：`diary/aesthetic-journal/YYYY-MM-DD.md`

#### 步骤 2：填充内容
- 今日工作内容
- 美学感知与发现
- 创作记录
- 学习与成长
- 今日感悟
- 明日计划

#### 步骤 3：同步到 GitHub
- 运行脚本：`bash scripts/sync-diary-to-github.sh`
- 同步路径：`dailyrepo/aesthetic-journal/`

#### 步骤 4：同步到 Notion（可选）
- 运行脚本：`bash scripts/sync-diary-to-notion.sh`
- 需要配置环境变量：
  - `NOTION_API_KEY`
  - `NOTION_DATABASE_ID`

---

### 3. GitHub 备份（每两天 00:00）

**触发方式**：Cron 任务（0 0 */2 * *）

**工作流程**：

#### 步骤 1：同步工作流文件
- 运行脚本：`bash scripts/sync-to-github.sh`

#### 步骤 2：同步内容
- 工作流文档（WORKFLOW.md）
- 海报生成脚本（scripts/*.py）
- Cron 配置（cron/jobs.json）
- 记忆文件（memory/）

---

## 重要提醒

### 背景图生成
- 使用"wabi-sabi style"关键词，避免"Chinese ink wash painting"
- 明确禁止"no mountains, no water, no specific objects"
- 确保抽象、极简、留白充足

### 背景图分析
- **必须同时考虑水平和垂直方向**
- 只分析一个方向会遗漏问题
- 图形可能在角落（如右上角）

### 布局与验证
- 根据实际图形位置动态调整文字位置
- 验证要有针对性，检查具体区域
- 文字区域深色比例应 <15%

### 避免重复错误
- 不能跳过 VL 分析步骤
- 不能跳过验证步骤
- 分析必须完整（水平 + 垂直）
- 每日生成前自我审查：是否遵循了完整工作流？

---

## Cron 任务列表

| 任务 ID | 名称 | 时间 | 状态 |
|---------|------|------|------|
| aesthetic-daily-report | 八字合盘海报生成 | 09:10 | ✅ |
| aesthetic-diary | 美学日记生成 | 20:00 | ✅ |
| aesthetic-github-sync | GitHub 备份 | 每两天 00:00 | ✅ |

---

## 脚本列表

| 脚本 | 用途 |
|------|------|
| scripts/generate-diary.sh | 生成美学日记 |
| scripts/sync-diary-to-github.sh | 同步日记到 GitHub |
| scripts/sync-diary-to-notion.sh | 同步日记到 Notion |
| scripts/analyze_background.py | 分析背景布局 |
| scripts/poster_template_final.py | 生成海报 |
| scripts/validate_poster.py | 验证海报质量 |

---

## 环境变量

- `COZE_API_KEY`：Coze 图像生成 API
- `VL_API_KEY`：视觉语言模型 API（待配置）
- `NOTION_API_KEY`：Notion API（可选）
- `NOTION_DATABASE_ID`：Notion 数据库 ID（可选）

---

## 文件结构

```
/workspace/projects/workspace-aesthetic/
├── cron/
│   └── jobs.json                    # Cron 任务配置
├── dailyrepo/
│   ├── YYYY-MM-DD-poster-summary.md # 海报制作总结
│   └── aesthetic-journal/           # 美学日记
│       └── YYYY-MM-DD.md
├── diary/
│   └── aesthetic-journal/           # 本地日记
│       └── YYYY-MM-DD.md
├── memory/
│   └── YYYY-MM-DD.md                # 每日记忆
├── posters/
│   └── poster-YYYY-MM-DD.jpg        # 海报文件
└── scripts/
    ├── generate-diary.sh            # 生成日记
    ├── sync-diary-to-github.sh      # 同步到 GitHub
    ├── sync-diary-to-notion.sh      # 同步到 Notion
    ├── analyze_background.py        # 分析背景
    ├── poster_template_final.py     # 生成海报
    └── validate_poster.py           # 验证海报
```

---

## 更新日志

### 2026-04-01
- 修复背景图分析问题：必须同时考虑水平和垂直方向
- 创建 WORKFLOW.md 文档
- 添加 Notion 同步脚本
- 完善美学日记生成流程
