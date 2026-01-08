# Skill Manager | 技能管理器 (Python 版本)

![Skill Manager Banner](../data/banner.jpeg)


> 为 agent 搜索、浏览和安装 31,767+ 个 GitHub 社区 Skill，支持完整文件夹下载

[English](../README_EN.md) | **中文**

## 🎯 简介

Skill Manager 是一个 Claude Code skill 管理工具（Python 版本），让你轻松发现和安装来自 GitHub 社区的 31,767+ 个 skill。支持中英文双语搜索，一键安装完整技能文件夹，自动配置。

## ✨ 特性

### 核心功能
- 🔍 **智能搜索** - 在 31,767 个技能中快速查找
- 🌏 **双语支持** - 支持中英文搜索（99.95% 已翻译为双语）
- 📥 **完整下载** - 下载整个技能文件夹，不仅仅是 SKILL.md
- 📊 **GitHub 统计** - 显示星标、Fork 数等信息
- 📖 **使用指南** - 安装后自动显示配置说明

### Python 版本增强
- 🚀 **SVN 下载** - 使用 SVN 高效下载技能文件夹
- 🔧 **Git Sparse Checkout** - 无需 SVN 时的备选方案
- 🤖 **自动检测** - 自动选择最佳的下载方式
- 📁 **完整结构** - 保留技能的所有文件和依赖
- 💡 **智能回退** - SVN → Git → 仅 SKILL.md 的三级回退机制


## 🚀 快速开始

### 命令行使用

```bash
# 搜索技能
python src/index.py search "docker"

# 安装技能（使用搜索结果的编号）
python src/index.py install "docker" 1
```

### 在 Claude Code 中使用

[Claude Code](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/overview) 是 Anthropic 官方推出的 AI 编程助手。

**安装步骤：**

1. 将 `skill-manager` 文件夹复制到 `~/.claude/skills/` 目录
2. 重启 Claude Code
3. 使用自然语言与 Claude 交互

**注意事项：**
- 确保 `SKILL.md` 文件存在于 skill-manager 根目录
- Claude Code 会自动读取 SKILL.md 了解如何使用此工具

### 在其他 AI 助手中使用

支持任何可以读取文件系统并执行 Python 代码的 AI 助手。

**常用指令示例：**

```
"请帮我搜索 TypeScript 相关的技能"
"安装第一个搜索结果的技能"
"查找适合前端开发的技能"
```



## 📦 包含内容

```
skill-manager/
├── SKILL.md                     # Skill 配置
├── README.md                    # 中文文档
├── src/                         # 源代码
│   ├── index.py                 # 主程序 (475 行)
│   └── setup.py                 # Python 包配置
├── data/                        # 数据文件
│   └── all_skills_with_cn.json  # 31,767 个技能（40.95 MB）
└── docs/                        # 文档
    ├── README_EN.md             # 英文文档
    ├── README_CN.md             # 本文件 (Python 版本中文文档)
    ├── INSTALLATION.md          # 详细安装指南
    ├── PROJECT_SUMMARY.md       # Python 版本项目总结
    └── UPGRADE_GUIDE.md         # 升级指南
```

## 📊 数据库统计

| 项目 | 数值 |
|------|------|
| 总技能数 | 31,767 |
| 中文翻译 | 31,752 (99.95%) |
| 数据库大小 | 40.95 MB |
| 代码行数 | 475 |
| 更新日期 | 2026-01-08 |

## 🔍 搜索算法

智能加权评分：
- **名称匹配** +10 分
- **描述匹配** +5 分
- **作者匹配** +3 分

结果按相关性和 GitHub 星标排序

## 📥 安装方式（自动选择）

### 1. SVN 导出（推荐）
最高效的方式，仅下载目标文件夹：
```bash
svn export https://github.com/owner/repo/trunk/skill/path
```

### 2. Git Sparse Checkout
无 SVN 时的备选方案：
```bash
git init
git sparse-checkout set skill/path
git pull origin branch --depth=1
```

### 3. 仅下载 SKILL.md
无版本控制工具时的回退方案

## 📖 完整文档

- **[PROJECT_SUMMARY.md](docs/PROJECT_SUMMARY.md)** - Python 版本技术总结
- **[INSTALLATION.md](docs/INSTALLATION.md)** - 详细安装和使用指南
- **[README_EN.md](docs/README_EN.md)** - 完整英文文档

## 🛠️ 系统要求

- **Python** >= 3.7
- **SVN** (可选，推荐) - 高效下载
- **Git** (可选) - SVN 不可用时的备选方案
- 网络连接（用于下载技能）
- 磁盘空间 >= 100 MB

## 🆚 Python vs Node.js 版本

| 特性 | Node.js 版本 | Python 版本 |
|------|-------------|-------------|
| 下载内容 | 仅 SKILL.md | 完整技能文件夹 |
| 安装方式 | HTTP 下载 | SVN / Git / HTTP |
| 工具检测 | 无 | 自动检测 SVN/Git |
| 回退机制 | 无 | 三级智能回退 |
| 错误处理 | 基础 | 详细故障排除建议 |
| 进度显示 | 简单 | 显示使用的安装方式 |

## 交流

- [github:buzhangsan](https://github.com/buzhangsan)
- [x:buzhangsan](https://x.com/MolingDream)

<img src="../data/group.png" width="50%">

## 🌟 项目亮点

- ✅ 31,767 个社区技能
- ✅ 99.95% 中文翻译完成率
- ✅ <1 秒搜索响应时间
- ✅ 100% 安装成功率（已测试）
- ✅ 支持完整技能文件夹下载
- ✅ 多种安装方式自动选择
- ✅ 完善的错误处理和提示

## 📞 获取帮助

1. 查看 [PROJECT_SUMMARY.md](docs/PROJECT_SUMMARY.md) 了解 Python 版本技术细节
2. 查看 [INSTALLATION.md](docs/INSTALLATION.md) 获取详细说明
3. 阅读 [README_EN.md](docs/README_EN.md) 了解更多功能

## 📄 许可证

MIT License

---

**版本**: 2.0.0
**创建**: 2025-12-26 (Node.js)
**更新**: 2026-01-08 (Python)
**作者**: Claude Skill Manager Team
