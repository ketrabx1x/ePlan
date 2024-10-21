import json
import os
from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRoundFlatButton

class FirstPage(MDScreen):
    dialog = None

    def check_and_proceed(self):
        if not self.ids.group_input.text or not self.ids.ang_input.text:
            if not self.dialog:
                self.dialog = MDDialog(
                    title='Alert',
                    text='Wpisz grupe i poziom angielskiego!',
                    buttons=[
                        MDRoundFlatButton(
                            text="OK",
                            on_release=self.close_dialog
                        ),
                    ],
                )
            self.dialog.open()
        else:
            self.save_data()
            self.manager.current = 'main'

    def close_dialog(self, instance):
        self.dialog.dismiss()
        self.dialog = None  # Reset the dialog instance

    def save_data(self):
        user_data = {
            "user_group": self.ids.group_input.text,
            "ang_level": self.ids.ang_input.text
        }
        with open("local_user_data.json", "w") as outfile:
            json.dump(user_data, outfile)

class MainPage(MDScreen):
    def on_enter(self, *args):
        with open("local_user_data.json", "r") as infile:
            user_data = json.load(infile)
            self.ids.group_app_bar.title = f"Grupa: {user_data['user_group']}, Ang: {user_data['ang_level']}"

    def go_to_first_page(self):
        self.manager.current = 'first'

class MyApp(MDApp):
    def build(self):
        return Builder.load_file("main.kv")
    
    def on_start(self):
        if os.path.exists("local_user_data.json"):
            with open("local_user_data.json", "r") as infile:
                user_data = json.load(infile)
                if "user_group" in user_data and "ang_level" in user_data:
                    self.root.current = 'main'

if __name__=="__main__":
    MyApp().run()