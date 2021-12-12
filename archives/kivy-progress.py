from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang import Builder
#from kivy.uix.slider import slider

Builder.load_file('kivy-progress.kv')
#Define our different screens
class MyLayout(Widget):
    def press_it(self):
        current = self.ids.my_progress_bar.value
        current = current + 1
        self.ids.my_progress_bar.value = current
        self.ids.progress_label.text = f'Distance {current}'

    def press_back(self):
        current = self.ids.my_progress_bar.value
        current = current -1
        self.ids.my_progress_bar.value = current
        self.ids.progress_label.text = f'Distance {current}'


    

class MySlider(App):
    def build(self):
        #self.theme_cls.theme_style = "Dark"
        #self.theme_cls.primary_palette = 'BlueGray'
        return MyLayout()

if __name__ == '__main__':
    
    MySlider().run()

