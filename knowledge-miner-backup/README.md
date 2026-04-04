# Knowledge Miner 完整备份

## 备份时间
2026-04-04 11:42

## 备份内容

### 1. anxiety-sessions/ - 对话记录
原始对话记录，包含完整挖掘过程。

### 2. memory/ - 记忆文件
每日工作记录和角色定义。

### 3. data_original/ - 思想金句+核心逻辑
按日期分类的结构化数据。

### 4. full-conversation-data.json - 完整数据
JSON 格式的所有对话数据，便于程序读取。

## 数据统计

| 角色 | 数量 |
|---|---|
| 小K | 13 条 |
| 莫妮卡 | 2 条 |
| **总计** | **15 条** |

## 主题分布

| 主题 | 数量 |
|---|---|
| 工具主权 | 5 条 |
| 创作自由 | 2 条 |
| 能量转化 | 2 条 |
| 创作主权 | 1 条 |
| 生理体验 | 1 条 |
| 能力传承 | 1 条 |
| 补位思维 | 1 条 |
| 帮助他人 | 1 条 |
| 双重壁垒 | 1 条 |
| 生态思维 | 1 条 |

## 相关链接

- **Knowledge Miner 工作区**: `/workspace/projects/knowledge-miner`
- **GitHub data_original**: https://github.com/icemagejin/openclaw_daily/tree/main/data_original
- **Notion 思想母库**: https://www.notion.so/33535d2a6ddb8069a74deb83b895bbaa

## 恢复方法

如果需要恢复数据：

```bash
# 克隆备份仓库
git clone git@github.com:icemagejin/Worklifebalance.git

# 复制数据到 knowledge-miner
cp -r Worklifebalance/knowledge-miner-backup/anxiety-sessions /workspace/projects/knowledge-miner/knowledge-base/
cp -r Worklifebalance/knowledge-miner-backup/memory /workspace/projects/knowledge-miner/
```

---

_此备份由 Knowledge Miner 自动创建，确保对话数据安全。_