from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang import Builder
# only need to import if doing work in .py
#from kivy.uix.slider import slider

Builder.load_file('kivy-check_boxes.kv')
#Define our different screens
class MyLayout(Widget):
    checks = []
    def checkbox_click(self, instance, value, topping):
        print(value, instance)
        if value == True:
            MyLayout.checks.append(topping)
            self.ids.output_label.text = str(MyLayout.checks)
        else:
            self.ids.output_label.text = "False"
class MySlider(App):
    def build(self):
        #self.theme_cls.theme_style = "Dark"
        #self.theme_cls.primary_palette = 'BlueGray'
        return MyLayout()

if __name__ == '__main__':
    
    MySlider().run()

