from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.config import Config
from kivy.utils import get_color_from_hex
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.popup import Popup
from kivy.animation import Animation
from kivy.uix.button import Button
from kivy.uix.colorpicker import ColorPicker
from kivy.properties import ObjectProperty
from kivy.uix.textinput import TextInput

import json
import os
from time import strftime
import smtplib



class ScreenGenerator(ScreenManager):
    pass


class PessQuestions(Screen):
    pass


class Menu(Screen):
    def __init__(self, **kwargs):
        super().__init__()
        self.ids.menu_date.text = strftime('[size=24][b]%A[/b][/size], %B %Y')


class Trackers(Screen):
    storage = {}
    pess_storage = {'physical': None, 'emotional': None, 'spiritual': None, 'sexual': None}
    path = ''
    email = {'kevin': 'Klhyer@gmail.com',
        'davi': 'vidasilveira85@gmail.com'}

    def on_pre_enter(self):
        self.path = App.get_running_app().user_data_dir + '/'
        self.loadData()
        for tracker, num in self.storage.items():
            self.ids.track.add_widget(Tracker(text=tracker, number=num, data=self.storage))

    def on_pre_leave(self):
        print(len(self.storage))
        self.ids.track.clear_widgets()
        self.saveData()


    def delete_storage(self, tracker):
        tracking = tracker.ids.label.text
        print(tracking)
        self.ids.track.remove_widget(tracker)
        del self.storage[tracking]
        self.saveData()

    def reset(self): ##### <------- Problems, Not working ########
        for t in self.storage.keys():
            self.storage[t] = '0'
        self.saveData()
        self.ids.track.clear_widgets()
        self.on_pre_leave()
        self.on_pre_enter()

    def savePESS(self, PESS):
        self.pess_storage['physical'] = PESS.ids.phy_text.text
        self.pess_storage['emotional'] = PESS.ids.emo_text.text
        self.pess_storage['spiritual'] = PESS.ids.spi_text.text
        self.pess_storage['sexual'] = PESS.ids.sex_text.text
        print(self.pess_storage)

    def saveData(self, *args):
        with open(self.path + 'data.json', 'w') as data:
            json.dump(self.storage, data)

    def loadData(self, *args):
        try:
            with open(self.path + 'data.json', 'r') as data:
                self.storage = json.load(data)
                print(self.storage)
        except FileNotFoundError:
            pass

    def addWidget(self):
        box = BoxLayout(orientation= 'vertical', padding=40, spacing=15)
        pop = Popup(title='Tracker: Name', content=box, size_hint=(None,None), size=(300,300))

        text_input = TextInput(hint_text='Add Trackers', multiline=False, size_hint=(None, None), size=(self.width / 3, 70))
        okay = Button(text='Save', height=100, on_press=lambda *args :self.addit(text_input.text), on_release=pop.dismiss)

        box.add_widget(text_input)
        box.add_widget(okay)
        pop.open()

    def addit(self, text_input, *args):
        if text_input not in self.storage.keys():
            num = '0'
            self.ids.track.add_widget(Tracker(text=text_input, number=num, data=self.storage))
            self.storage[text_input] = '0'
            text_input = ''
            self.saveData()
        else:
            box = BoxLayout(orientation= 'vertical', padding=40, spacing=5)
            pop = Popup(title=f'Opps: "{text_input}" is already listed below', content=box, size_hint=(None,None), size=(300,180))
            try_again = Button(text='Try Again', on_release=pop.dismiss)
            box.add_widget(try_again)
            pop.open()


#### Add numebers and Subtract numbers from labels, Function ####
    def add_num(self, tracker):
        tracker.ids.count_add.text = str(int(tracker.ids.count_add.text) + 1)
        self.storage[tracker.ids.label.text] = str(int(tracker.ids.count_add.text))
        print(self.storage)
        self.saveData()

    def subtract_num(self, tracker):
        tracker.ids.count_add.text = str(int(tracker.ids.count_add.text) - 1)
        self.storage[tracker.ids.label.text] = str(int(tracker.ids.count_add.text))
        print(self.storage)
        self.saveData()

    def send(self):
        os.chdir(r'C:\Users\vida\Desktop\PESS')
        with open('bat', 'r') as bat:
            login = bat.read()
            me = self.email['davi']
            recipient = self.email['davi']
            day = strftime("%a, %b %d, %Y")
            tracker_message = 'PESS\n'
            subject_message = f"Subject: PESS {day}"

            for pess, txt in self.pess_storage.items():
                tracker_message += f"\t{pess.title()}: {txt}\n"

            for tracker, numbers in self.storage.items():
                tracker_message += f"\n{numbers} ---> {tracker}\n"
            message = f"{subject_message}\n\n{tracker_message}"

            #  setup email login/send msg
            smtp_obj = smtplib.SMTP('smtp.gmail.com', 587)
            smtp_obj.ehlo()
            smtp_obj.starttls()
            smtp_obj.login(me, login)
            smtp_obj.sendmail(me, recipient, message) #  send email
            smtp_obj.quit()
            #self.sent_confirmation()

    '''
    def sent_confirmation(self): # <----- not working "AssertionError: None is not callable"
        recipient = self.email['davi']
        box = BoxLayout(orientation= 'vertical', padding=40, spacing=5)
        pop = Popup(title=f'Congrats, {recipient} has recieved an email.', content=box, size_hint=(None,None), size=(300,300))
        exit_app = Button(text='Exit App', on_release=App.get_running_app().stop())
        box.add_widget(exit_app)
        pop.open()
        self.saveData()
    '''

class Tracker(BoxLayout):
    def __init__(self, text='', number='', data={}, **kwargs):
        super().__init__(**kwargs)
        self.ids.label.text = text
        self.ids.count_add.text = number


class Pess(App):
    def build(self):
        Config.set('graphics', 'width', '600')
        Config.set('graphics', 'height', '800')
        from kivy.core.window import Window
        Window.clearcolor = get_color_from_hex('#262829')

        return ScreenGenerator()


if __name__ == '__main__':
    Pess().run()
