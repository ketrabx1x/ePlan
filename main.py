import json
import os
from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFillRoundFlatButton, MDRectangleFlatButton, MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel
from datetime import datetime, timedelta

# Kalendarz do załadowania w MainPage
class CalendarWidget(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.current_date = datetime.today()
        self.header = MDBoxLayout(adaptive_height=True)
        self.prev_button = MDFillRoundFlatButton(text='<', on_press=self.prev_month)
        self.next_button = MDFillRoundFlatButton(text='>', on_press=self.next_month)
        self.month_label = MDLabel(text=self.current_date.strftime('%B %Y'), size_hint=(2, 1), halign='center')

        self.header.add_widget(self.prev_button)
        self.header.add_widget(self.month_label)
        self.header.add_widget(self.next_button)

        self.add_widget(self.header)
        self.calendar_grid = MDGridLayout(cols=7, spacing=5, size_hint=(1, None), height=300)
        self.add_widget(self.calendar_grid)
        self.populate_calendar(self.current_date)

    def populate_calendar(self, date):
        self.calendar_grid.clear_widgets()
        days_of_week = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        for day in days_of_week:
            self.calendar_grid.add_widget(MDLabel(text=day, halign='center'))

        first_day = date.replace(day=1)
        start_day = first_day.weekday()
        next_month = first_day.replace(day=28) + timedelta(days=4)
        last_day_of_month = next_month - timedelta(days=next_month.day)
        num_days = last_day_of_month.day

        for _ in range(start_day):
            self.calendar_grid.add_widget(MDLabel())

        for day in range(1, num_days + 1):
            self.calendar_grid.add_widget(MDFillRoundFlatButton(text=str(day), on_press=self.on_day_select))

        self.month_label.text = date.strftime('%B %Y')

    def on_day_select(self, instance):
        print(f"Wybrano dzień: {instance.text} {self.current_date.strftime('%B %Y')}")

    def prev_month(self, instance):
        first_day = self.current_date.replace(day=1)
        prev_month = first_day - timedelta(days=1)
        self.current_date = prev_month.replace(day=1)
        self.populate_calendar(self.current_date)

    def next_month(self, instance):
        next_month = self.current_date.replace(day=28) + timedelta(days=4)
        self.current_date = next_month.replace(day=1)
        self.populate_calendar(self.current_date)

class FirstPage(MDScreen):
    dialog = None

    def check_and_proceed(self):
        if not self.ids.group_input.text or not self.ids.ang_input.text:
            if not self.dialog:
                self.dialog = MDDialog(
                    title='Alert',
                    text='Wpisz grupe i poziom angielskiego!',
                    buttons=[
                        MDFillRoundFlatButton(
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
        self.dialog = None  # Reset dialogu

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

        # Dodanie kalendarza do MDBoxLayout o id calendar_box
        calendar_widget = CalendarWidget()
        self.ids.calendar_box.clear_widgets()  # Czyszczenie poprzednich widgetów (jeśli są)
        self.ids.calendar_box.add_widget(calendar_widget)

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