import tkinter as tk
from PIL import ImageGrab
import pyautogui

class CaptureScreen:
    def __init__(self, root):
        self.root = root
        self.cancelled = False
        self.start_x = None
        self.start_y = None
        self.end_x = None
        self.end_y = None
        self.rect = None
        self.canvas = tk.Canvas(root, cursor="cross")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # 设置窗口属性
        self.root.attributes("-fullscreen", True)
        self.root.attributes("-topmost", True)
        self.root.attributes("-alpha", 0.3)  # 设置透明度
        self.root.bind("<Button-1>", self.on_mouse_down)
        self.root.bind("<B1-Motion>", self.on_mouse_drag)
        self.root.bind("<ButtonRelease-1>", self.on_mouse_up)
        self.root.bind("<Button-3>", self.on_right_click)

    def on_mouse_down(self, event):
        self.start_x = self.root.winfo_pointerx()
        self.start_y = self.root.winfo_pointery()
        self.rect = self.canvas.create_rectangle(0, 0, 1, 1, outline="red")

    def on_mouse_drag(self, event):
        curX, curY = self.root.winfo_pointerx(), self.root.winfo_pointery()
        self.canvas.coords(self.rect, self.start_x, self.start_y, curX, curY)

    def on_mouse_up(self, event):
        if not self.cancelled:
            self.end_x, self.end_y = pyautogui.position()
            self.take_screenshot()

    def on_right_click(self, event):
        self.cancelled = True
        self.root.destroy()
        return "break"

    def take_screenshot(self):
        x1, y1 = min(self.start_x, self.end_x), min(self.start_y, self.end_y)
        x2, y2 = max(self.start_x, self.end_x), max(self.start_y, self.end_y)
        self.screenshot = ImageGrab.grab(bbox=(x1, y1, x2, y2))
        self.root.destroy()

    def get_screenshot(self):
        self.root.mainloop()
        return None if self.cancelled else self.screenshot

def capture_screen():
    root = tk.Tk()
    capture_screen = CaptureScreen(root)
    return capture_screen.get_screenshot()
