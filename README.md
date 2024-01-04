# 截图和OCR项目

## 项目概述

这个项目是一个用于截取屏幕区域并识别其中文字的工具。它允许用户通过热键触发屏幕截图，然后使用OCR技术来识别截图中的文字。

## 功能特点

- **快速截图**：用户可以通过简单的热键操作快速截取屏幕上的任意区域。
- **文字识别**：集成OCR技术，能够识别截图中的文字内容。
- **交互界面**：提供一个简单直观的用户界面，展示截图和识别结果。
- **搜索功能**：在识别的结果中搜索特定的关键词。
- **多语言支持**：支持多种语言的文字识别，包括中文。

## 使用指南

预先安装Tesseract-OCR到默认目录C:\Program Files\Tesseract-OCR\ [下载/安装说明](https://tesseract-ocr.github.io/tessdoc/Installation.html)


在windows操作系统下，clone项目后，进入path/to/project/screen_ocr/dist/ScreenOCR/

运行ScreenOCR.exe运行程序


## 安装指南

说明生成windows可执行程序。这可能包括如何下载源代码、安装必要的依赖等。

```bash
git clone https://this-repository-url
cd path/to/project/screen_ocr
# 安装依赖
pip install -r requirements.txt
```
### 修改Tesseract安装路径

```src/ocr.py
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
## 将后面默认路径修改为实际安装路径
```
### 生成windows可执行项目

```bash
pyinstaller --icon=src/icon.ico --name="ScreenOCR" --window src/main.py
```
