import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp 
#from kivy.core.window import Window # for changing background color

#Define our different screens
class MainMenu(Screen):
    pass

class Administration(Screen):
    pass

class Filepicker(Screen):
    pass

    class MyLayout(Widget):
        def selected(self, filename):
            try:
                self.ids.my_image.source = filename[0]
            except:
                pass

class FloatTest(Screen):
    pass

class WindowManager(ScreenManager):
    pass

kv = Builder.load_file('kivy-imageviewer.kv')


class RiskMit(App):
    def build(self):
        #self.theme_cls.theme_style = "Dark"
        #self.theme_cls.primary_palette = 'BlueGray'
        return kv


if __name__ == '__main__':
    
    RiskMit().run()

