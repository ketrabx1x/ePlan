from kivymd.app import MDApp
from kivy.lang import Builder
from database import *
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRoundFlatButton

class FirstPage(MDScreen):
    dialog = None

    def check_and_proceed(self):
        if not self.ids.group_input.text:
            if not self.dialog:
                self.dialog = MDDialog(
                    title='Alert',
                    text='Please enter a group!',
                    buttons=[
                        MDRoundFlatButton(
                            text="OK",
                            on_release=self.close_dialog
                        ),
                    ],
                )
            self.dialog.open()
        else:
            self.manager.current = 'main'

    def close_dialog(self, instance):
        self.dialog.dismiss()
        self.dialog = None  # Reset the dialog instance

class MainPage(MDScreen):
    pass

class MyApp(MDApp):
    def build(self):
        return Builder.load_file("main.kv")

if __name__=="__main__":
    MyApp().run()