# src/display.py
import tkinter as tk
from PIL import ImageTk, ImageDraw
from tkinter import Listbox, Entry, Button, messagebox

class InteractiveDisplay:
    def __init__(self, root, image, text_boxes):
        self.root = root
        self.original_image = image
        self.text_boxes = text_boxes
        self.tk_image = ImageTk.PhotoImage(image)

        # 图像显示
        self.label_image = tk.Label(root, image=self.tk_image)
        self.label_image.pack(side="left")

        # 文本列表显示
        self.listbox = Listbox(root, height=20)
        for idx, (text, x, y, w, h) in enumerate(text_boxes):
            self.listbox.insert(tk.END, f"{idx}: {text}")
        self.listbox.pack(side="left", fill=tk.Y)

        # 绑定列表框的选择事件
        self.listbox.bind("<<ListboxSelect>>", self.on_listbox_select)

        # 搜索框和按钮
        self.search_var = tk.StringVar()
        entry_search = Entry(root, textvariable=self.search_var)
        entry_search.pack(side="top", fill=tk.X)
        button_search = Button(root, text="搜索", command=self.search_text)
        button_search.pack(side="top")

    def on_listbox_select(self, event):
        selection = event.widget.curselection()
        if selection:
            idx = selection[0]
            _, x, y, w, h = self.text_boxes[idx]
            self.highlight_text_on_image(x, y, w, h)

    def highlight_text_on_image(self, x, y, w, h):
        # 创建一个新的图像副本以绘制高亮区域
        highlighted = self.original_image.copy()
        draw = ImageDraw.Draw(highlighted)
        draw.rectangle([x, y, x + w, y + h], outline="blue", width=2)

        # 更新Tkinter中的图像
        self.tk_image = ImageTk.PhotoImage(highlighted)
        self.label_image.config(image=self.tk_image)

    def search_text(self):
        search_keyword = self.search_var.get().lower()
        found_indices = []
        for idx, (text, _, _, _, _) in enumerate(self.text_boxes):
            if search_keyword in text.lower():
                found_indices.append(idx)

        if found_indices:
            for idx in found_indices:
                self.listbox.selection_set(idx)  # 高亮显示所有找到的项
                self.listbox.see(idx)  # 滚动到第一个找到的项
        else:
            messagebox.showinfo("搜索结果", "未找到包含关键词的文本。")


def display_image_and_text(image, text_boxes):
    root = tk.Tk()
    root.title("OCR Result")
    app = InteractiveDisplay(root, image, text_boxes)
    root.mainloop()


def show_info_dialog():
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口

    # 设置你想要显示的信息
    hotkey_info = "使用热键 Ctrl+Shift+X 截图，使用Esc退出"
    tesseract_info = f"使用前请确保Tesseract已安装在：C:\Program Files\Tesseract-OCR"

    # 弹出消息框
    messagebox.showinfo("程序已启动", f"{hotkey_info}\n{tesseract_info}")

    root.destroy()  # 关闭窗口
