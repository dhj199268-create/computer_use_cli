# Computer Use CLI

一个基于 pyautogui 的计算机控制 CLI 工具，通过结构化接口为 AI Agent 提供计算机操作能力。

[English Documentation](README.md)

## 功能特性

- **鼠标控制**：移动、点击、拖拽、滚动等鼠标操作
- **键盘控制**：文本输入、按键、快捷键组合
- **屏幕操作**：截图、屏幕尺寸、像素颜色检测
- **图像识别**：在屏幕上定位图像，通过图像匹配进行点击
- **技能系统**：可复用的自动化技能框架
- **美观界面**：基于 Rich 的命令行界面

## 安装

```bash
# 从源码安装
pip install -e .
```

## 快速开始

```bash
# 查看帮助
computer-use --help

# 鼠标操作
computer-use mouse position                    # 获取当前鼠标位置
computer-use mouse move --x 100 --y 100      # 移动鼠标到指定坐标
computer-use mouse click                       # 在当前位置点击

# 键盘操作
computer-use keyboard write --text "你好"      # 输入文本
computer-use keyboard hotkey --keys cmd c     # 按下快捷键组合

# 屏幕操作
computer-use screen size                       # 获取屏幕分辨率
computer-use screen screenshot --output shot.png  # 截取屏幕
```

## 配置

从示例创建 `.env` 文件：

```bash
cp .env.example .env
```

主要配置选项：

- `PAUSE`：操作之间的延迟（默认：0.1 秒）
- `FAILSAFE`：启用故障安全功能（默认：true）
- `MINIMUM_DURATION`：最小移动持续时间
- `LOG_LEVEL`：日志级别（默认：INFO）

## 安全说明

- **故障安全**：将鼠标移动到左上角 (0, 0) 可中止操作
- 在自动化之前请务必仔细测试操作
- 故障安全功能默认启用

## 项目结构

```
computer_use_cli/
├── src/computer_use/
│   ├── core/           # 核心配置和异常
│   ├── tools/          # 鼠标、键盘和图像工具
│   ├── skills/         # 自动化技能框架
│   ├── cli/            # 命令行界面
│   └── utils/          # 工具函数
├── tests/              # 测试套件
├── examples/           # 使用示例
└── skills/             # 技能配置文件
```

## 为 Agent 设计

此工具旨在为 AI Agent 提供计算机操作能力。Agent 可以：

1. 直接使用 CLI 命令进行简单操作
2. 导入 Python 模块进行程序化控制
3. 使用 BaseSkill 抽象类构建自定义技能
4. 利用图像识别进行视觉自动化

## 许可证

MIT
