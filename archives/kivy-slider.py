from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.lang import Builder
# only need to import if doing work in .py
#from kivy.uix.slider import slider

Builder.load_file('kivy-slider.kv')
#Define our different screens
class MyLayout(Widget):
    def slide_it(self, *args):
        print(args[1])
        self.slide_text.text = str(int(args[1]))
        
        
class MySlider(App):
    def build(self):
        #self.theme_cls.theme_style = "Dark"
        #self.theme_cls.primary_palette = 'BlueGray'
        return MyLayout()

if __name__ == '__main__':
    
    MySlider().run()

