from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang import Builder
# only need to import if doing work in .py
#from kivy.uix.slider import slider

Builder.load_file('kivy-spinner.kv')
#Define our different screens
class MyLayout(Widget):
    def spinner_clicked(self, value):
        self.ids.click_label.text = value



class MySlider(App):
    def build(self):
        #self.theme_cls.theme_style = "Dark"
        #self.theme_cls.primary_palette = 'BlueGray'
        return MyLayout()

if __name__ == '__main__':
    
    MySlider().run()

