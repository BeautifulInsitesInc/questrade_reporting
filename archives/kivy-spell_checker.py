from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.core.spelling import Spelling

Builder.load_file('kivy-spell_checker.kv')
#Define our different screens
class MyLayout(Widget):
    def press(self):
        # Create instance of Spelling
        s = Spelling()
        
        # see what languages are available
        print("Languages: ", s.list_languages())
        s.select_language('en_US')
        #grab word from textbox
        word = self.ids.word_input.text

        option = s.suggest(word)
        
        #update our label
        self.ids.word_label.text = str(option)
        print("Option: ",option)
        
class SpellChecker(App):
    def build(self):
        #self.theme_cls.theme_style = "Dark"
        #self.theme_cls.primary_palette = 'BlueGray'
        return MyLayout()

if __name__ == '__main__':
    
    SpellChecker().run()

