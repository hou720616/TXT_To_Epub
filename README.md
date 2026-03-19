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

## 快速启动

1. 双击 `run.bat`，或在终端执行：
   ```bash
   run.bat
   ```
2. 脚本会自动创建虚拟环境、安装依赖并启动图形界面。

## 使用说明

1. 手动方式启动应用程序：
   ```bash
   python -m venv venv
   .\venv\Scripts\python.exe -m pip install -r requirements.txt
   .\venv\Scripts\python.exe main.py
   ```
2. 在界面中：
   - 点击“浏览...”选择要转换的 TXT 文件。
   - （可选）设置输出的 EPUB 路径（默认与 TXT 同目录）。
   - （可选）填写书名和作者信息。
   - 点击“开始转换”按钮即可生成 EPUB 文件。

## 目录结构
- `main.py` - PyQt6 GUI 界面逻辑及入口文件
- `converter.py` - 核心转换逻辑文件（读取TXT、匹配章节、生成EPUB）
- `requirements.txt` - 项目依赖库列表
- `run.bat` - 一键创建环境并启动程序

## 打包 EXE

1. 安装打包工具：
   ```bash
   .\venv\Scripts\python.exe -m pip install pyinstaller
   ```
2. 构建单文件 GUI 程序：
   ```bash
   .\venv\Scripts\python.exe -m PyInstaller --noconfirm --clean --windowed --onefile --name TXT_To_Epub main.py
   ```
3. 生成文件位置：
   - `dist\TXT_To_Epub.exe`
