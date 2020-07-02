from kivymd.app import MDApp
from kivymd.theming import ThemeManager
from kivymd.uix.dialog import MDDialog
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.uix.list import TwoLineListItem
from kivymd.uix.button import MDIconButton, MDFlatButton
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.chip import MDChip
from kivy.clock import Clock
from kivy.modules import keybinding
from kivy.core.window import Window

from PyDictionary import PyDictionary
import sys
import json
import requests
from functools import partial

LIST = []

MESSAGE = """
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

class Manager(ScreenManager):
    pass

class Main(Screen):
    def on_pre_enter(self):
        Window.bind(on_key_down=self.call)

    """main application goes here"""
    # def on_touch_down(self, touch):
    #     print("touched screen")
    #     return super().on_touch_down(touch)

    def navigation_draw(self):
        print("navigation")

    def close_dialog(self, obj):
        self.dialog.dismiss()

    def open_dialog(self):
        close = MDIconButton(icon="close-circle", on_release=self.close_dialog)
        #more = MDIconButton(icon="more")
        self.dialog = MDDialog(title="Probably Knot Helper",
                               text=MESSAGE,
                               size_hint=(0.8, 1), buttons=[close],)
        self.dialog.open()

    def call(self, *args):
        theme_cls = ThemeManager()
        self.ids.stack.clear_widgets()
        sent = self.ids.sentence.text.lower()
        for idx, word in enumerate(sent.split()):
            print(idx, word)
            c = MDChip(label=word,
                       callback=self.do_something,
                       #icon='home-analytics',
                       selected_chip_color=theme_cls.accent_color,
                       )
            self.ids.stack.add_widget(c)

    def do_something(self, inst, word, *args):
        self.ids.analyze_btn.disabled = False

        LIST.append(word)
        return LIST


class Analyzer(Screen):
    def on_touch_move(self, touch):
        # print(touch)
        with self.canvas:
            print(dir(touch.ud))

    def on_leave(self):
        # print(dir(self.ids.container))
        self.ids.container.clear_widgets()

    def define(self):
        definition = ''
        wrd = LIST[-1].lower()
        # Definition Section #
        dictionary = PyDictionary()
        define_wrd = dictionary.meaning(wrd)
        for key, value in define_wrd.items():
            for words in value:
                definition += f"{words}, "
        theme_cls = ThemeManager()
        self.dialog_one = MDDialog(
                                title=f"Definition: {wrd}",
                                text=definition,
                                buttons=[
                                    MDFlatButton(
                                        text="CLOSE", text_color=theme_cls.primary_color),])
        self.dialog_one.open()

    def analyze(self, main): # main is pointing to ---> Main().show_data()
        """Analyse data with PyDictionary"""

        sent = main.ids.sentence.text.lower()
        if LIST == []:
            self.empty()
        else:
            wrd = LIST[-1].lower()

            if wrd != '' and sent != '':
                API_KEY = 'a701e74e453ee6695e450310340401f5'
                URL = f'http://words.bighugelabs.com/api/2/{API_KEY}/{wrd}/json'

                if wrd not in sent:
                    error = MDDialog(title="Error", text=f"Word: '{wrd}' is not in\n\n'{sent}'")
                    error.open()
                else:
                    r = requests.get(URL) # get's url json file
                    try:
                        j = json.loads(r.text) # loads json into 'j' as a dict
                        print(len(j['noun']['syn']), j)
                    except:
                        j = {''}
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
            else:
                self.empty()

    def empty(self, *args):
        print("I made it -- empty dialog")
        theme_cls = ThemeManager()
        self.dialog_one = MDDialog(
                                text="First screen dialog",
                                buttons=[
                                    MDFlatButton(
                                        text="CANCEL", text_color=theme_cls.primary_color),
                                    MDFlatButton(
                                        text="DISCARD", text_color=theme_cls.primary_color)])
        self.dialog_one.open()


class ProbablyKnotApp(MDApp):
    def build(self):
        self.theme_cls = ThemeManager()
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.primary_hue = "900"

        self.theme_cls.accent_palette = 'Blue'
        self.theme_cls.accent_hue = "900"

        return Manager()

    def change_screen(self, screen):
        self.root.current = screen


if __name__ == "__main__":
    ProbablyKnotApp().run()
