from kivy.app import App
from kivy.uix.label import Label
from kivy.core.window import Window

import ctypes
from ctypes import wintypes


class MyApp(App):
    def build(self):
        Window.size = (800, 600)  # Set window size
        Window.borderless = False  # Ensure window has borders
        Window.resizable = False  # Disable window resizing
        self.title = "Fixed Size Kivy App"  # Set window title

        # Disable both the resize functionality and the maximize button (Windows specific)
        self.disable_resize_and_maximize()

        return Label(text="Fixed Size Window")

    def disable_resize_and_maximize(self):
        hwnd = ctypes.windll.user32.GetActiveWindow()
        if hwnd:
            GWL_STYLE = -16
            WS_MAXIMIZEBOX = 0x00010000
            WS_SIZEBOX = 0x00040000
            style = ctypes.windll.user32.GetWindowLongPtrW(hwnd, GWL_STYLE)
            style &= ~WS_MAXIMIZEBOX  # Disable maximize button
            style &= ~WS_SIZEBOX  # Disable resizing through borders
            ctypes.windll.user32.SetWindowLongPtrW(hwnd, GWL_STYLE, style)


if __name__ == "__main__":
    MyApp().run()
