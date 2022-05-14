from typing import Text
from kivy.app import App
from kivy.uix.label import Label

class DemoApp(App):
    def build(self):
        return Label(text="Hello World")


if __name__ == "main":
    app = DemoApp()
    app.run()

