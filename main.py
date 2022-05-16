from functools import partial
import webbrowser
from kivy.app import App
from kivy.config import Config
from kivy.lang import Builder
from kivy.storage.jsonstore import JsonStore
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.graphics import Rectangle, Color
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image

app_data_Json = JsonStore("app_data")
user_data_Json = JsonStore("user_data")

BROWSE_OBJECT_HEIGHT = 0.3
BROWSE_OBJECT_TITLE_COLOR = (0.027, 0.455, 0.612, 1)
BROWSE_OBJECT_BIO_COLOR = (0.035, 0.569, 0.765, 1)
BROWSE_OBJECT_BUTTONS_COLOR = (0.027, 0.455, 0.612, 1)
BROWSE_OBJECT_BOTTOM_LAYOUT_COLOR = (0.035, 0.569, 0.765, 1)

# Store data to be quickly accessed
temp_data = {
    "keywords": [],
    "browser_objects": [],
    "groups": {},
    "results": {}
}


class BrowseObject(BoxLayout):
    def __init__(self, title, bio, keywords, links = None, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "horizontal"
        self.size_hint=(1, None)
        self.height = app.root.ids.FormWindow.size[1] * BROWSE_OBJECT_HEIGHT

        self.widgets_with_canvas = []

        # Main Layout
        self.BoxLayout1 = BoxLayout(orientation="vertical", size_hint = (1, 1))
        self.add_widget(self.BoxLayout1)

        # Top Layout
        self.BoxLayout2 = BoxLayout(orientation="horizontal", size_hint = (1, 0.25))
        self.BoxLayout1.add_widget(self.BoxLayout2)

        # Logo
        self.Image1 = Image(source = 'DHS_logo.png', size_hint = (0.3, 1))
        self.BoxLayout2.add_widget(self.Image1)


        # Title
        self.Label1 = Label(text = title, font_name ="Roboto-Bold", font_size = "18sp", valign = "bottom", halign = "left", padding = (5, 5),size_hint = (0.7, 1))
        self.BoxLayout2.add_widget(self.Label1)
        with self.Label1.canvas.before:
            Color(*BROWSE_OBJECT_TITLE_COLOR)
            self.Label1.rect = Rectangle(pos = self.Label1.pos, size = self.Label1.size)
        self.widgets_with_canvas.append(self.Label1)

        # Bio
        self.Label2 = Label(text = bio, font_name ="Roboto-Bold", font_size = "13sp",  valign = "top", halign = "left", padding = (5, 5), size_hint = (1, 0.25))
        self.BoxLayout1.add_widget(self.Label2)
        with self.Label2.canvas.before:
            Color(*BROWSE_OBJECT_BIO_COLOR)
            self.Label2.rect = Rectangle(pos = self.Label2.pos,size = self.Label2.size)
        self.widgets_with_canvas.append(self.Label2)

        # Bottom layout
        self.BoxLayout3 = BoxLayout(orientation="horizontal", size_hint = (1, 0.5))
        self.BoxLayout1.add_widget(self.BoxLayout3)

        # Links layout
        self.StackLayout1 = StackLayout(size_hint = (0.5, 1))
        self.BoxLayout3.add_widget(self.StackLayout1)
        with self.StackLayout1.canvas.before:
            Color(*BROWSE_OBJECT_BOTTOM_LAYOUT_COLOR)
            self.StackLayout1.rect = Rectangle(pos = self.StackLayout1.pos,size = self.StackLayout1.size)
        self.widgets_with_canvas.append(self.StackLayout1)
        
        if links != None:
            for link in links:
                button_name = link + "Button"
                url = links[link]

                setattr(self, button_name, Button(text = link, background_color = BROWSE_OBJECT_BUTTONS_COLOR, size_hint = (1, 0.25)))
                button = getattr(self, button_name)

                self.StackLayout1.add_widget(button)

                open_link = partial(self.link_callback, url)
                button.bind(on_release = open_link)

        # Keywords layout
        self.StackLayout2 = StackLayout(size_hint = (0.5, 1))
        self.BoxLayout3.add_widget(self.StackLayout2)
        with self.StackLayout2.canvas.before:
            Color(*BROWSE_OBJECT_BOTTOM_LAYOUT_COLOR)
            self.StackLayout2.rect = Rectangle(pos = self.StackLayout2.pos,size = self.StackLayout2.size)
        self.widgets_with_canvas.append(self.StackLayout2)
    
        app.root.bind(size=self.update)

        for Element in self.widgets_with_canvas:
                Element.bind(pos=self.update)
                Element.bind(size=self.update)

    def update(self, *args):
        self.height = app.root.size[1] * BROWSE_OBJECT_HEIGHT
        for Element in self.widgets_with_canvas:
            Element.rect.pos = Element.pos
            Element.rect.size = Element.size
            Element.text_size = Element.size
    
    def link_callback(self, url, *args):
        pass
        webbrowser.open(url)


class BrowseWindow(Screen):
    pass

class FormWindow(Screen):
    pass

    # When the submit button is clicked on the form page, this function will be called
    def submit_button_click(self):
        if temp_data["keywords"] == [keyword.strip(" ") for keyword in self.ids.keywords_input.text.strip(" ,").split(",")]:
            return
        
        temp_data["keywords"] = [keyword.strip(" ") for keyword in self.ids.keywords_input.text.strip(" ,").split(",")]
        
        browser_layout = self.parent.ids.BrowseWindow.ids.browser_layout

        for widget in temp_data["browser_objects"]:
            browser_layout.remove_widget(widget)
        
        temp_data["browser_objects"] = []
        
        user_keywords = temp_data["keywords"]

        def create_result():
            results = {}

            for group in temp_data["groups"]:
                group_keywords = temp_data["groups"][group]["keywords"]

                number_of_keywords = 0
                matched_keywords = []
                
                for keyword in group_keywords:
                    if keyword in user_keywords:
                        matched_keywords.append(keyword)
                        number_of_keywords += 1
                
                if number_of_keywords != 0:
                    results[group] = {"number_of_keywords": number_of_keywords, "matched_keywords": matched_keywords}

            print(results)
            return results

        results = create_result()

        for group in results:
            print("CREATING GROUP", group)
            group_data = temp_data["groups"][group]
            Layout = BrowseObject(group, group_data["bio"], results[group]["matched_keywords"], group_data["links"])
            browser_layout.add_widget(Layout)
            temp_data["browser_objects"].append(Layout)

    def clean_button_click(self):
        self.ids.keywords_input.text = "type here"
        temp_data["keywords"].clear()

class MainWindow(Screen):
    def start_button_click(self):
        pass

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
        Config.set('graphics', 'width', '375')
        Config.set('graphics', 'height', '812')
        Config.write()

        global app
        app = App.get_running_app()


        if not user_data_Json.exists("keywords"):
            user_data_Json.put("user_data",  keywords = [""])

        temp_data["keywords"] = user_data_Json.get("user_data")["keywords"]
        temp_data["groups"] = app_data_Json.get("groups")

        return Builder.load_file("EztraCurricules.kv")

if __name__ == '__main__':
    # Loop that continuously runs until the application gui is closed
    EztraCurriculesApp().run()
