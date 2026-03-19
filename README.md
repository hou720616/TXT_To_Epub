# TXT 到 EPUB 转换工具

这是一个使用 Python 和 PyQt6 编写的轻量级 TXT 转 EPUB 桌面应用程序。该工具支持自动检测章节（如“第一章”、“Chapter 1”等）并将其生成带有目录（TOC）的 EPUB 文件。

## 功能特性
- **简约界面**：基于 PyQt6 的现代化用户界面。
- **自动分章**：自动识别文本中的章节标题，在生成的 EPUB 文件中划分章节并生成书籍目录。
- **自动编码检测**：自动尝试 `utf-8`、`gb18030`、`gbk`、`big5` 等多种编码读取文本文件，防止中文乱码。
- **异步转换**：转换过程在后台线程进行，界面不卡顿。

## 运行环境
- Python 3.10+
- PyQt6
- EbookLib

## 下载打包程序
- 已发布可直接下载的 Windows 打包版本（含 EXE）：https://github.com/hou720616/TXT_To_Epub/releases

## 目录结构
- `main.py` - PyQt6 GUI 界面逻辑及入口文件
- `converter.py` - 核心转换逻辑文件（读取TXT、匹配章节、生成EPUB）
- `requirements.txt` - 项目依赖库列表
- `run.bat` - 一键创建环境并启动程序
