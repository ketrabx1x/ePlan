from kivymd.app import MDApp
from kivy.lang import Builder
from database import *
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.screen import MDScreen

class FirstPage(MDScreen):
    pass

class MainPage(MDScreen):
    pass

class MyApp(MDApp):
    def build(self):
        return Builder.load_file("main.kv")

if __name__=="__main__":
    MyApp().run()