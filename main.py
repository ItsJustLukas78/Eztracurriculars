# Designed by Lukas Somwong
from kivy.app import App
from kivy.config import Config
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import sqlite3
# from kivy.uix.floatlayout import FloatLayout
# from kivy.uix.boxlayout import BoxLayout
# from kivy.uix.button import Button
# from kivy.uix.widget import Widget

# Store data such as keywords to be quickly accessed
user_data = {
    "keywords": []
}

class BrowseWindow(Screen):
    def start_button_click(self):
        print("clicked out")

    def submit_button_click(self):
        user_data["keywords"] = [keyword.strip(" ") for keyword in self.ids.keywords_input.text.strip(" ,").split(",")]
        print(user_data)
    
    def clean_button_click(self):
        self.ids.keywords_input.text = "type here"
        user_data["keywords"].clear()

class FormWindow(Screen):
    def start_button_click(self):
        print("clicked out")

    def submit_button_click(self):
        user_data["keywords"] = [keyword.strip(" ") for keyword in self.ids.keywords_input.text.strip(" ,").split(",")]
        print(user_data)
    
    def clean_button_click(self):
        self.ids.keywords_input.text = "type here"
        user_data["keywords"].clear()

class MainWindow(Screen):
    def start_button_click(self):
        print("clicked")

class WindowManager(ScreenManager):
    pass

class EztraCurriculesApp(App):
    def build(self):

        # Data storage for persistant data between sessions
        '''
        store_connection = sqlite3.connect("app_data.db")
        store_cursor = store_connection.cursor()
        store_cursor.executescript()
        store_connection.commit()
        store_connection.close()
        '''

        # Allows application to be resized
        Config.set('graphics', 'resizable', '1')

        return Builder.load_file("EztraCurricules.kv")

if __name__ == '__main__':
    # Loop that continuously runs until the application gui is closed
    EztraCurriculesApp().run()
