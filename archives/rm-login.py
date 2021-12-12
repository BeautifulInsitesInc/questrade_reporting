from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp 

class MainApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette ="Blue"
        self.theme_cls.accent_palette = "Green"
        return Builder.load_file('rm_login.kv')
    def logger(self):
        self.root.ids.welcome_label.text =f'{self.root.ids.user.text} Authorized!'
    def clearlogger(self):
        self.root.ids.welcome_label.text = "WELCOME"
        self.root.ids.user.text = ""
        self.root.ids.password.text = ""


#class RiskMit(App):
#    def build(self):
        #self.theme_cls.theme_style = "Dark"
        #self.theme_cls.primary_palette = 'BlueGray'
 #       return kv

if __name__ == '__main__':
    MainApp().run()

