# Designed by Lukas Somwong
from kivy.app import App
from kivy.config import Config
from kivy.lang import Builder
from kivy.storage.jsonstore import JsonStore
from kivy.uix.screenmanager import ScreenManager, Screen
import sqlite3
# from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Rectangle, Color
from kivy.uix.boxlayout import BoxLayout
# from kivy.uix.button import Button
from kivy.uix.label import Label
# from kivy.uix.widget import Widget

app_data_Json = JsonStore("app_data")
user_data_Json = JsonStore("user_data")

# Store data such as keywords to be quickly accessed
temp_data = {
    "keywords": [],
    "browser_objects": []
}

class BrowseObject(BoxLayout):
    def __init__(self, title, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.size_hint=(1, None)
        self.height = app.root.ids.FormWindow.size[1] * 0.2

        self.Label1 = Label(text = title)
        self.add_widget(self.Label1)
        
        with self.Label1.canvas.before:
            Color(0.2, 0.1, 0.2, 1)
            self.Label1.rect = Rectangle(pos = self.Label1.pos, size = self.Label1.size)
        
        app.root.bind(size=self.update)
        self.Label1.bind(pos=self.update)
        self.Label1.bind(size=self.update)

    def update(self, *args):
        self.height = app.root.size[1] * 0.3
        self.Label1.rect.pos = self.Label1.pos
        self.Label1.rect.size = self.Label1.size



class BrowseWindow(Screen):
    def start_button_click(self):
        print("clicked out")

    def submit_button_click(self):
        temp_data["keywords"] = [keyword.strip(" ") for keyword in self.ids.keywords_input.text.strip(" ,").split(",")]
        print(temp_data)
    
    def clean_button_click(self):
        self.ids.keywords_input.text = "type here"
        temp_data["keywords"].clear()

class FormWindow(Screen):
    def start_button_click(self):
        print("clicked out")

    # When the submit button is clicked on the form page, this function will be called
    def submit_button_click(self):
        if temp_data["keywords"] == [keyword.strip(" ") for keyword in self.ids.keywords_input.text.strip(" ,").split(",")]:
            return
        
        temp_data["keywords"] = [keyword.strip(" ") for keyword in self.ids.keywords_input.text.strip(" ,").split(",")]
        print(temp_data)
        
        browser_layout = self.parent.ids.BrowseWindow.ids.browser_layout

        for widget in temp_data["browser_objects"]:
            browser_layout.remove_widget(widget)
            temp_data["browser_objects"].remove(widget)
        
        for x in range(5):

            Layout = BrowseObject("Foo Bar")
            browser_layout.add_widget(Layout)
            temp_data["browser_objects"].append(Layout)
        
        for x in temp_data["browser_objects"]:
            print(x)

    
    def clean_button_click(self):
        self.ids.keywords_input.text = "type here"
        temp_data["keywords"].clear()

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

        global app
        app = App.get_running_app()

        return Builder.load_file("EztraCurricules.kv")

if __name__ == '__main__':
    # Loop that continuously runs until the application gui is closed
    EztraCurriculesApp().run()
