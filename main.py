import webbrowser
import time
import threading
from functools import partial
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

# Allows application to be resized
Config.set('graphics', 'resizable', '1')

# Sets width and height at which the app should launch at
Config.set('graphics', 'width', '375')
Config.set('graphics', 'height', '700')
Config.write()

# Constants
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

# BrowseObject constructor, BrowseObjects are the layouts found after submitting the form
class BrowseObject(BoxLayout):
    def __init__(self, title, bio, keywords, links = None, **kwargs):
        """Creates a BrowseObject

            Parameters: 
                title (str): The title of the group 
                bio (str): The bio of the group 
                keywords (list): Matched keywords to be displayed 
                links (dict): Dictionary of titles assigned to url links 

        
        """
        # Returns the __init__ method of class parent, BoxLayout, so we can call its methods
        super().__init__(**kwargs)

        self.orientation = "horizontal"
        self.size_hint=(1, None)
        self.height = app.root.ids.FormWindow.size[1] * BROWSE_OBJECT_HEIGHT

        self.widgets_with_canvas = []

        # Main Layout
        self.BoxLayout1 = BoxLayout(orientation="vertical", size_hint = (1, 1))
        self.add_widget(self.BoxLayout1)

        # Top Layout
        self.BoxLayout2 = BoxLayout(orientation="horizontal", padding = (3, 3), size_hint = (1, 0.25))
        self.BoxLayout1.add_widget(self.BoxLayout2)
        # Creating a rectangle on the layout so that we can have a colored background
        with self.BoxLayout2.canvas.before:
            Color(*BROWSE_OBJECT_TITLE_COLOR)
            self.BoxLayout2.rect = Rectangle(pos = self.BoxLayout2.pos, size = self.BoxLayout2.size)
        self.widgets_with_canvas.append(self.BoxLayout2)

        # Logo
        self.Image1 = Image(source = "Images/" + title + ".png", mipmap = True, size_hint = (0.3, 1))
        self.BoxLayout2.add_widget(self.Image1)

        initial_title_font_size = 18
        subtraction = len(title) // 15
        title_font_size = str(initial_title_font_size - subtraction) + "sp"

        # Title
        self.Label1 = Label(text = title, font_name ="Roboto-Bold", font_size = title_font_size, valign = "bottom", halign = "left", padding = (5, 5),size_hint = (0.7, 1))
        self.BoxLayout2.add_widget(self.Label1)

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
        
        # Creating link buttons
        if links != None:
            for link in links:
                button_name = link + "Button"
                url = links[link]

                setattr(self, button_name, Button(text = link, background_color = BROWSE_OBJECT_BUTTONS_COLOR, size_hint = (1, 0.25)))
                button = getattr(self, button_name)

                self.StackLayout1.add_widget(button)

                # When the button is pressed, it calls the partial function which passes its url to "link_callback" method
                open_link = partial(self.link_callback, url)
                button.bind(on_release = open_link)

        # Keywords layout
        self.Label3 = Label(text = "Matched keywords: \n" + ", ".join(keywords), font_name ="Roboto-Bold", font_size = "13sp",  valign = "top", halign = "left", padding = (5, 5), size_hint = (0.5, 1))
        self.BoxLayout3.add_widget(self.Label3)
        with self.Label3.canvas.before:
            Color(*BROWSE_OBJECT_BOTTOM_LAYOUT_COLOR)
            self.Label3.rect = Rectangle(pos = self.Label3.pos,size = self.Label3.size)
        self.widgets_with_canvas.append(self.Label3)
        
        # When app root size is changed, call "update" method
        app.root.bind(size=self.update)

        for Element in self.widgets_with_canvas:
            Element.bind(pos=self.update)
            Element.bind(size=self.update)

    # Update sizes
    def update(self, *args):
        self.height = app.root.size[1] * BROWSE_OBJECT_HEIGHT
        for Element in self.widgets_with_canvas:
            Element.rect.pos = Element.pos
            Element.rect.size = Element.size
            Element.text_size = Element.size
    
    # Opens url in browser with given link
    def link_callback(self, url, *args):
        webbrowser.open(url)


class BrowseWindow(Screen):
    pass

class FormWindow(Screen):

    # When the submit button is clicked on the form page, this function will be called
    def submit_button_click(self):
        temp_data["keywords"] = [keyword.strip(" ") for keyword in self.ids.keywords_input.text.lower().strip(" ,").split(",")]
        
        browser_layout = self.parent.ids.BrowseWindow.ids.browser_layout

        # Remove existing BrowserObjects on the brose page
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

        if results != {}:
            for group in results:
                print("CREATING GROUP", group)
                group_data = temp_data["groups"][group]
                Layout = BrowseObject(group, group_data["bio"], results[group]["matched_keywords"], group_data["links"])
                browser_layout.add_widget(Layout)
                temp_data["browser_objects"].append(Layout)

            app.root.transition.direction = "left"
            app.root.current = "Browse"
        else:
            # Changing the text of the buttons on a different thread so kivy can update the GUI on main thread
            threading.Thread(
                target = lambda: (
                    setattr(app.root.ids.FormWindow.ids.SubmitButton, "text", "No groups were matched!"), 
                    time.sleep(3),
                    setattr(app.root.ids.FormWindow.ids.SubmitButton, "text", "Submit form"))).start()


    def clean_button_click(self):
        self.ids.keywords_input.text = ""
        temp_data["keywords"].clear()
        threading.Thread(
                target = lambda: (
                    setattr(app.root.ids.FormWindow.ids.ClearButton, "text", "Form cleared!"), 
                    time.sleep(3),
                    setattr(app.root.ids.FormWindow.ids.ClearButton, "text", "Clear form"))).start()

class MainWindow(Screen):
    def start_button_click(self):
        pass

class WindowManager(ScreenManager):
    pass

class EztraCurriculesApp(App):
    def build(self):

        global app
        app = App.get_running_app()

        temp_data["groups"] = app_data_Json.get("groups")

        return Builder.load_file("EztraCurricules.kv")

# If the python file was called ..
if __name__ == '__main__':
    # Loop that continuously runs until the application gui is closed
    EztraCurriculesApp().run()
