from kivy.app import App
from kivy.config import Config
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.widget import Widget

Config.set('graphics', 'resizable', '1')

class MainFloatLayout(FloatLayout):
    pass

class EztraCurriculesApp(App):
    def build(self):
        return MainFloatLayout()

EztraCurriculesApp().run()