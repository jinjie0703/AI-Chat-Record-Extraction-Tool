# AI-Chat-Record-Extraction-Tool

<p align="center">  <!-- 在这里可以放一些徽章，例如构建状态、许可证等 -->  <img src="https://img.shields.io/badge/build-passing-brightgreen" alt="Build Status">  <img src="https://img.shields.io/badge/license-MIT-blue" alt="License">  <img src="https://img.shields.io/badge/platform-Windows-informational" alt="Platform"></p>

<details><summary>English Version (Click to expand)</summary>

### Introduction

This is a utility tool for extracting and converting chat records from mainstream AI applications (like ChatGPT, Claude, etc.). It's designed to help users parse exported chat data and convert it into a universal Markdown (`.md`) format for easier analysis, archiving, or sharing.

I created this tool with the personal goal of converting my AI conversations into `.md` format to better organize knowledge and build knowledge graphs. Realizing it could be useful in other scenarios, I decided to make it open-source. Currently, the script only supports converting chat records from **Google AI Studio**. Support for other mainstream platforms will be added in the future, along with general user experience improvements. Contributions to enhance the project by submitting PRs are highly welcome.

### Features

* **Multi-Platform Support**: Capable of extracting records exported from various AI chat platforms and converting them into `.md` documents.
* **Multiple Output Formats**: Supports Markdown (`.md`) and JSON (`.json`).
* **Batch Processing**: Provides a script to process all chat record files within a folder at once.
* **Easy to Extend**: Features a modular design, making it convenient for users to add support for new platforms or output formats.

### Installation & Setup

1. **Clone the Repository**:
  
      git clone https://github.com/jinjie0703/AI-Chat-Record-Extraction-Tool.git
  
2. **Compile the Project**:
  
  * Open the solution file (`.sln`) with **Visual Studio 2022**.
  * Select the `Release` and `x64` configuration.
  * Click on "Build" -> "Build Solution" in the menu bar (Shortcut: `F7` or `Ctrl+Shift+B`).
3. **Find the Executable**:
  
  * After a successful build, you can find `AI-Chat-Record-Extraction-Tool.exe` in the `x64/Release/` directory of the project.

### Usage

The core of this tool is a command-line program. Place the `AI-Chat-Record-Extraction-Tool.exe`, the Python script, and the data file(s) exported from the official source into the same folder, and then run the executable.

**Parameter Description**:

* `--source, -s`: Specify the source platform of the chat record (e.g., `chatgpt`, `claude`).
* `--input, -i`: The path to a single input chat record file.
* `--output, -o`: The path to the directory where the converted file will be saved.
* `--format, -f`: The desired output format (`txt`, `md`, `json`).

* * *

### How to Contribute

Contributions of any kind are welcome! If you have a suggestion or find a bug, please feel free to submit a Pull Request or create an Issue.

1. Fork this repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

### License

This project is licensed under the [MIT](LICENSE.txt) License.

</details>

<details open><summary>中文版 (点击展开)</summary>

### 介绍

这是一款用于提取和转换主流AI聊天应用（如 ChatGPT, Claude 等）记录的实用工具。它旨在帮助用户解析导出的聊天数据，并将其转换为通用的Markdown (`.md`)格式，以便于后续的分析、存档或分享。本人制作这个小工具是想把与ai对话的聊天内容转换成.md格式方便知识汇总和制作知识图谱，考虑到有一定的应用场景所以开源出来；目前脚本只支持Google AI Studio的聊天内容转换，后续会补全主流平台的转换脚本并优化体验；欢迎完善项目，提交PR。

### 功能特性

* **多平台支持**: 能够提取从多种AI聊天平台导出的记录并转换成md文档。
* **多种输出格式**: Markdown (`.md`) 和 JSON (`.json`)。
* **批量处理**: 提供脚本，可以一次性转换文件夹内的所有聊天记录文件。
* **易于扩展**: 模块化设计，方便用户添加对新平台或新输出格式的支持。

### 安装与配置

1. **克隆仓库**:
  
      git cone https://github.com/jinjie0703/AI-Chat-Record-Extraction-Tool.git
  
2. **编译项目**:
  
  * 使用 **Visual Studio 2022** 打开解决方案文件 (`.sln`)。
  * 在配置中选择 `Release` 和 `x64`。
  * 点击菜单栏的“生成” -> “生成解决方案” (快捷键 `F7` 或 `Ctrl+Shift+B`)。
3. **找到可执行文件**:
  
  * 编译成功后，您可以在项目目录的 `x64/Release/` 文件夹下找到 `AI-Chat-Record-Extraction-Tool.exe`。

### 使用方法

本工具的核心是一个命令行程序，将`AI-Chat-Record-Extraction-Tool.exe`、`python`脚本、`官方数据库导出的数据文件`放在同一个文件夹里，运行exe程序。

**参数说明**:

* `--source, -s`: 指定聊天记录的来源平台 (例如 `chatgpt`, `claude`)。
* `--input, -i`: 单个输入聊天记录文件的路径。
* `--output, -o`: 用于存放转换后文件的目录路径。
* `--format, -f`: 您希望转换的目标格式 (`txt`, `md`, `json`)。

</details>

* * *

### 如何贡献

欢迎任何形式的贡献！如果您有好的建议或发现了Bug，请随时提交 Pull Request 或创建 Issue。

1. Fork 本仓库
2. 创建您的分支
3. 提交您的更改
4. 推送到分支
5. 打开一个 Pull Request

### 许可证

本项目采用 [MIT](LICENSE.txt) 许可证。