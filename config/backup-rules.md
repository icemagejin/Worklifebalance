# 备份仓库配置

## 📁 work-life-balance 仓库

### 远程仓库地址
```
【待用户提供 - 请填写 GitHub 仓库地址】
```

### 用途
存放所有需要备份的文件，除了日报之外的所有内容。

## 📋 约法三章（重要）

### 1. 禁止同步到 `my-personal-site`
- ❌ 任何备份文件都不允许推送到 `my-personal-site` 仓库
- ❌ 任何配置文件、数据文件都不允许推送到 `my-personal-site`

### 2. 日报例外
- ✅ **唯一例外**：项目管理日报 → `my-personal-site/app/news`
- ✅ 文件名格式：`YYYY-MM-DD.md`（如 `2026-03-25.md`）
- ✅ 仅限 PM Agent 生成的日报

### 3. 所有备份到 `work-life-balance`
- ✅ 账号列表（如 x_accounts_list.json）
- ✅ 配置文件
- ✅ 数据文件
- ✅ 设计资源
- ✅ 任何需要备份的内容

## 🔄 备份流程

### Step 1: 添加文件
```bash
cd /workspace/work-life-balance
git add <文件名>
```

### Step 2: 提交
```bash
git commit -m "描述信息"
```

### Step 3: 推送
```bash
git push origin main
```

## 📝 注意事项

1. **推送前确认目标仓库**：确保是 `work-life-balance`，不是 `my-personal-site`
2. **日报特殊处理**：日报仍同步到 `my-personal-site/app/news`
3. **定期备份**：重要修改后立即备份到 `work-life-balance`

---

**配置时间**: 2026-03-26 23:02
**配置人**: PM Agent
**生效范围**: 所有 Agent
