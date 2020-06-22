from kivymd.app import MDApp
from kivymd.theming import ThemeManager
from kivymd.uix.dialog import MDDialog
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.uix.list import TwoLineListItem

from PyDictionary import PyDictionary
import sys
import json
import requests


class Manager(ScreenManager):
    """Manages Screens"""

class Main(Screen):
    """main application goes here"""
    def close_dialog(self, obj):
        self.dialog.dismiss()

    def show_data(self):
        message = """
        This little program was
        designed to help re-think
        your sentences and
        therefore find new
        solutions.
        
        By re-shuffling your words
        you can better understand
        your problems and come up
        with more elegant
        solutions.
        """
        close = MDIconButton(icon="close-circle", on_release=self.close_dialog)
        #more = MDIconButton(icon="more")
        self.dialog = MDDialog(title="Probably Knot", text=message,
                         size_hint=(0.5, 1), buttons=[close])
        self.dialog.open()


class Analyzer(Screen):
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
                    # try:
                    #     for num, w in enumerate(j['adjective']['syn'], 1):
                    #         item = OneLineListItem(text=f"{num}: {sent.replace(wrd, w)}\n")
                    #         self.ids.container.add_widget(item)
                    # except KeyError:
                    #     print(f'Adjective for "{wrd}" is not found.')
                    # try:
                    #     for num, w in enumerate(j['noun']['syn'], 1):
                    #         item = OneLineListItem(text=f"{num}: {sent.replace(wrd, w)}\n")
                    #         self.ids.container.add_widget(item)
                    # except KeyError:
                    #     print(f'Noun for "{wrd}" is not found.') 
                    # try:
                    #     for num, w in enumerate(j['verb']['syn'], 1):
                    #         item = OneLineListItem(text=f"{num}: {sent.replace(wrd, w)}\n")
                    #         self.ids.container.add_widget(item)
                    # except KeyError:
                    #     print(f'Verb for "{wrd}" is not found.')


class ProbablyKnotApp(MDApp):
    def build(self):
        self.theme_cls = ThemeManager()
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "DeepOrange"
        self.theme_cls.primary_hue = "A700"

        return Manager()

if __name__ == "__main__":
    ProbablyKnotApp().run()
