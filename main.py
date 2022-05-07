from kivy.app import App
from kivy.config import Config
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.widget import Widget

Config.set('graphics', 'resizable', '1')

class BrowseWindow(Screen):
    def start_button_click(self):
        print("clicked out")

class MainWindow(Screen):
    def start_button_click(self):
        print("clicked")

class WindowManager(ScreenManager):
    pass

kv = Builder.load_file("EztraCurricules.kv")

class EztraCurriculesApp(App):
    def build(self):
        return kv

if __name__ == '__main__':
    EztraCurriculesApp().run()
