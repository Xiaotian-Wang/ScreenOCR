import keyboard
from capture import capture_screen
from ocr import recognize_text_and_draw_boxes
from display import display_image_and_text, show_info_dialog
import threading
import pystray
from pystray import MenuItem as item
from PIL import Image, ImageDraw
import logging
import sys

import os


def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filename='app.log',
                    filemode='w+')

def screenshot_ocr_and_display():
    screenshot = capture_screen()
    if screenshot is None:  # 检查是否取消了截图
        print("截图已取消。")
        return

    create_directory('screenshots/')

    screenshot_path = "screenshots/screenshot.png"
    screenshot.save(screenshot_path)

    processed_image, text_boxes = recognize_text_and_draw_boxes(screenshot_path)
    logging.info("ocr finished")
    display_image_and_text(processed_image, text_boxes)

def create_image(width, height, color1, color2):
    # 创建一个新的图像，并绘制一个简单的图标
    image = Image.new('RGB', (width, height), color1)
    dc = ImageDraw.Draw(image)
    dc.rectangle(
        [width // 2, 0, width, height // 2],
        fill=color2)
    dc.rectangle(
        [0, height // 2, width // 2, height],
        fill=color2)
    return image

def setup(icon):
    icon.visible = True

def create_tray_icon():
    # 图标图像
    icon_image = create_image(64, 64, 'black', 'red')

    # 托盘图标菜单项
    menu = (item('退出', on_exit),)

    # 创建并显示托盘图标
    global icon
    icon = pystray.Icon("test_icon", icon_image, "屏幕OCR", menu)


    icon.run(setup)


def on_exit(*event):

    icon.stop()  # 停止图标
    keyboard.unhook_all()  # 取消所有键盘钩子
    # sys.exit()  # 退出程序
    os._exit(0)

show_info_dialog()

# 设置截图热键
keyboard.add_hotkey('ctrl+shift+x', screenshot_ocr_and_display)

# 监听ESC键
keyboard.add_hotkey('esc', on_exit)

tray_icon_thread = threading.Thread(target=create_tray_icon)
tray_icon_thread.daemon = True
tray_icon_thread.start()

# create_tray_icon()
"""
dialog_thread = threading.Thread(target=show_info_dialog)
dialog_thread.daemon = True
dialog_thread.start()
"""


# 保持程序运行
keyboard.wait()