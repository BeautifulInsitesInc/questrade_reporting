from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.lang import Builder

Builder.load_file('kivy-test.kv')

class MyLayout(Widget):

    def press(self):
        name = self.ids.input_name.text
        something = self.ids.input_something.text
        self.ids.label_answer.text = f'Hello {name}, you are a {something}'
        print(f'Hi {name} you friging {something} ')
        self.ids.input_name.text = ''
        self.ids.input_something.text  = ''
  
class Main(App):
    def build(self):
        return MyLayout()

if __name__ == '__main__':
    Main().run()

