from kivymd.app import MDApp
from kivymd.theming import ThemeManager
from kivymd.uix.dialog import MDDialog
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.uix.list import TwoLineListItem
from kivymd.uix.button import MDIconButton
from kivymd import *

from PyDictionary import PyDictionary
import sys
import json
import requests


class Manager(ScreenManager):
    def change_screen(self, inst):
        Manager.current = f'{inst.ids.main.text}'

class Main(Screen):
    """main application goes here"""
    def close_dialog(self, obj):
        self.dialog.dismiss()

    def show_data(self):
        message = """
        Think of Probably Knot (PK) as a study
        guide of sorts. Helping the user guide
        himself.

        This little program was designed to help
        re-think ones sentences and therefore 
        find new solutions. By changing ones
        perception, things can become more clear
        where once they were misunderstood.

        PK re-shuffle a word from an input
        sentence to help rephrase ones 
        orignal sentence. To better
        understand problems and ideas by
        changing the angle of perception
        with more elegant solutions.
        """
        close = MDIconButton(icon="close-circle", on_release=self.close_dialog)
        #more = MDIconButton(icon="more")
        self.dialog = MDDialog(title="Probably Knot Helper", text=message,
                         size_hint=(0.8, 1), buttons=[close])
        self.dialog.open()


class Analyzer(Screen):
    def on_leave(self):
        # print(dir(self.ids.container))
        self.ids.container.clear_widgets()


    def analyze(self, main): # main is pointing to ---> Main().show_data()
        """Analyse data with PyDictionary"""

        sent = main.ids.sentence.text.lower()
        wrd = main.ids.word.text.lower()
        print(sent, wrd)

        # Definition Section #
        dictionary = PyDictionary()
        define_wrd = dictionary.meaning(wrd)

        if wrd != '' and sent != '':
            API_KEY = 'a701e74e453ee6695e450310340401f5'
            URL = f'http://words.bighugelabs.com/api/2/{API_KEY}/{wrd}/json'

            if wrd not in sent:
                print("i made it")
                error = MDDialog(title="Error", text=f"Word: '{wrd}' is not in\n\n'{sent}'")
                error.open()
            else:
                r = requests.get(URL) # get's url json file
                j = json.loads(r.text) # loads json into 'j' as a dict

                if type(j) == dict: # check is 'j' variable is coming in as a Dict holds the new sentences new = f"{result}\n"
                    final_set = set()
                    try:
                        for w in j['adjective']['syn']:
                            final_set.add(w)
                    except KeyError:
                        print(f'Adjective for "{wrd}" is not found.')
                    try:
                        for w in j['noun']['syn']:
                            final_set.add(w)
                    except KeyError:
                        print(f'Noun for "{wrd}" is not found.') 
                    try:
                        for w in j['verb']['syn']:
                            final_set.add(w)
                    except KeyError:
                        print(f'Verb for "{wrd}" is not found.')
                    item = TwoLineListItem(text=f"Original: {sent}", secondary_text=f"{wrd}")
                    self.ids.container.add_widget(item)
                    for word in final_set:
                        item = TwoLineListItem(text=f"{sent.replace(wrd, word)}", secondary_text=f"{word}")
                        self.ids.container.add_widget(item)


class ProbablyKnotApp(MDApp):
    def build(self):
        self.theme_cls = ThemeManager()
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Amber"
        self.theme_cls.primary_hue = "A700"

        return Manager()

if __name__ == "__main__":
    ProbablyKnotApp().run()
