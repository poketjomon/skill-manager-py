# Skill Manager | 技能管理器

![Skill Manager Banner](../data/banner.jpeg)


> Search, browse, and install 31,767+ community skills from GitHub for your AI agent

**English** | [中文](../README.md)


## Introduction

Skill Manager is a Claude Code skill management tool (Python version) that lets you easily discover and install 31,767+ skills from the GitHub community. Features bilingual search support, complete folder downloads, and automatic configuration.


## Features

### Core Features
- **Smart Search** - Quickly find among 31,767 skills
- **Bilingual Support** - Supports both English and Chinese search (99.95% translated)
- **Complete Folder Download** - Downloads entire skill folders, not just SKILL.md
- **GitHub Stats** - Displays stars, forks, and other metrics
- **Usage Guides** - Automatically shows configuration instructions after installation

### Python Version Enhancements
- **SVN Download** - Efficient folder downloads using SVN
- **Git Sparse Checkout** - Fallback method when SVN unavailable
- **Auto Detection** - Automatically selects the best download method
- **Complete Structure** - Preserves all skill files and dependencies
- **Smart Fallback** - Three-tier fallback: SVN → Git → SKILL.md only



## Quick Start

### Command Line Usage

```bash
# Search skills
python src/index.py search "docker"

# Install skill (using search result index)
python src/index.py install "docker" 1
```

### Using with Claude Code

[Claude Code](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/overview) is the official AI programming assistant from Anthropic.

**Installation Steps:**

1. Copy the `skill-manager` folder to `~/.claude/skills/` directory
2. Restart Claude Code
3. Interact with Claude using natural language

**Notes:**
- Ensure `SKILL.md` exists in skill-manager root directory
- Claude Code will automatically read SKILL.md to understand how to use this tool

### Using with Other AI Assistants

Supports any AI assistant that can read filesystem and execute Python code.

**Example Commands:**

```
"Please help me search for TypeScript related skills"
"Install the first search result skill"
"Find skills suitable for frontend development"
```



## File Structure

```
skill-manager/
├── SKILL.md                     # Skill configuration
├── README.md                    # Chinese documentation
├── src/                         # Source code
│   ├── index.py                 # Main implementation (475 lines)
│   └── setup.py                 # Python package configuration
├── data/                        # Data files
│   └── all_skills_with_cn.json  # 31,767 skills (40.95 MB)
└── docs/                        # Documentation
    ├── README_EN.md             # This file (English documentation)
    ├── README_CN.md             # Python version Chinese documentation
    ├── INSTALLATION.md          # Detailed installation guide
    ├── PROJECT_SUMMARY.md       # Project summary (Python version)
    └── UPGRADE_GUIDE.md         # Upgrade guide
```

## Database Statistics

| Item | Value |
|------|-------|
| Total Skills | 31,767 |
| Chinese Translations | 31,752 (99.95%) |
| Database Size | 40.95 MB |
| Code Lines | 475 |
| Last Updated | 2026-01-08 |

## Search Algorithm

Intelligent weighted scoring:
- **Name match** +10 points
- **Description match** +5 points
- **Author match** +3 points

Results sorted by relevance and GitHub stars

## Installation Methods (Auto-selected)

### 1. SVN Export (Recommended)
Most efficient method, downloads only target folder:
```bash
svn export https://github.com/owner/repo/trunk/skill/path
```

### 2. Git Sparse Checkout
Fallback when SVN unavailable:
```bash
git init
git sparse-checkout set skill/path
git pull origin branch --depth=1
```

### 3. SKILL.md Only Download
Fallback when no version control tools available

## Complete Documentation

- **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - Python version technical summary
- **[INSTALLATION.md](INSTALLATION.md)** - Detailed installation and usage guide
- **[README_CN.md](../README.md)** - Complete Chinese documentation

## System Requirements

- **Python** >= 3.7
- **SVN** (optional, recommended) - For efficient downloads
- **Git** (optional) - Fallback when SVN unavailable
- Internet connection (for downloading skills)
- Disk space >= 100 MB

## Python vs Node.js Version

| Feature | Node.js Version | Python Version |
|---------|-----------------|----------------|
| Download Content | SKILL.md only | Complete skill folder |
| Installation Methods | HTTP download | SVN / Git / HTTP |
| Tool Detection | None | Auto-detect SVN/Git |
| Fallback Mechanism | None | Three-tier smart fallback |
| Error Handling | Basic | Detailed troubleshooting tips |
| Progress Display | Simple | Shows installation method used |

## Community
- [github:buzhangsan](https://github.com/buzhangsan)
- [x:buzhangsan](https://x.com/MolingDream)

<img src="../data/group.png" width="50%">

## Project Highlights

- 31,767 community skills
- 99.95% Chinese translation completion rate
- <1 second search response time
- 100% installation success rate (tested)
- Support for complete skill folder downloads
- Multiple installation methods with auto-selection
- Comprehensive error handling and prompts

## Getting Help

1. Check [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) for Python version technical details
2. Check [INSTALLATION.md](INSTALLATION.md) for detailed instructions
3. Read [../README.md](../README.md) for more features

## License

MIT License

---

**Version**: 2.0.0
**Created**: 2025-12-26 (Node.js)
**Updated**: 2026-01-08 (Python)
**Author**: Claude Skill Manager Team
