from kivy.app import App
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.popup import Popup
from kivy.clock import mainthread
import ctypes
import threading
import updater
import injector
import os


class MyApp(App):
    def build(self):
        Window.size = (400, 300)
        Window.borderless = False
        Window.resizable = False
        self.title = "YimMenu Launchpad"

        self.disable_resize_and_maximize()  # Call for window style

        main_layout = BoxLayout(orientation="vertical")

        # Title layout
        title_lbl = Label(
            text="YimMenu Launchpad",
            font_size="28sp",
            bold=True,
            size_hint=(None, None),
            size=(400, 50),
            valign="top",
            halign="center",
        )

        # Buttons layout
        buttons_layout = RelativeLayout()
        button1 = Button(
            text="Update",
            size_hint=(None, None),
            size=(150, 50),
            pos_hint={"center_x": 0.5},
            y=Window.height / 2 - 150,  # Vertical align
        )
        button2 = Button(
            text="Inject",
            size_hint=(None, None),
            size=(150, 50),
            pos_hint={"center_x": 0.5},
            y=Window.height / 2 - 225,  # Vertical align
        )

        button1.bind(on_press=self.start_check_for_updates)
        button2.bind(on_press=self.start_injection)

        # Add into layouts
        main_layout.add_widget(title_lbl)
        buttons_layout.add_widget(button1)
        buttons_layout.add_widget(button2)
        main_layout.add_widget(buttons_layout)

        return main_layout

    def disable_resize_and_maximize(self):
        """
        This function is only to make the window not maximizable and resizable.
        """
        hwnd = ctypes.windll.user32.GetActiveWindow()
        if hwnd:
            GWL_STYLE = -16
            WS_MAXIMIZEBOX = 0x00010000
            WS_SIZEBOX = 0x00040000
            style = ctypes.windll.user32.GetWindowLongPtrW(hwnd, GWL_STYLE)
            style &= ~WS_MAXIMIZEBOX  # Disable maximize button
            style &= ~WS_SIZEBOX  # Disable resizing through borders
            ctypes.windll.user32.SetWindowLongPtrW(hwnd, GWL_STYLE, style)

    def start_check_for_updates(self, instance):
        """
        Start the update check in a new thread.
        """
        threading.Thread(target=self.check_for_updates).start()

    def check_for_updates(self):
        """
        Check for updates and show a popup if everything is up-to-date.
        """
        if not updater.download_if_needed():
            self.show_popup("Everything up-to-date")
        else:
            self.show_popup("Updated!")

    def start_injection(self, instance):
        """
        Start the injection in a new thread.
        """
        threading.Thread(target=self.injection).start()

    def injection(self):
        pid = injector.find_process_id(injector.PROCESS_NAME)
        if pid == None:
            self.show_popup("Couldn't find the process!")
            return

        exotic_folder = updater.check_dirs()[0]
        dll_file = os.path.join(exotic_folder, "YimMenu.dll")
        try:
            injector.inject_dll(pid, dll_file)
        except:
            self.show_popup("Error injecting!")

    @mainthread
    def show_popup(self, message):
        """
        Display a popup with the given message.
        """
        popup_layout = BoxLayout(orientation="vertical", padding=5)
        popup_label = Label(text=message, size_hint=(1, 0.8))
        close_button = Button(text="Close", size_hint=(1, 0.5))
        popup_layout.add_widget(popup_label)
        popup_layout.add_widget(close_button)

        popup = Popup(
            title="Update Status",
            content=popup_layout,
            size_hint=(0.5, 0.5),
            auto_dismiss=False,
        )
        close_button.bind(on_press=popup.dismiss)
        popup.open()


if __name__ == "__main__":
    MyApp().run()
