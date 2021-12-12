# KIVY IMPORTS
from sys import maxsize
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivymd.app import MDApp
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.icon_definitions import md_icons
from kivy.factory import Factory
from kivy.core.window import Window
from kivymd.theming import ThemeManager
# DATABASE IMPORTS
from IPython.display import display
import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, MetaData, Table, select, delete
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.expression import null
# ACCOUNT API IMPORTS
from rm_questrade_api import *
# CUSTOM FUCITION IMPORTS
#from rm_tables import *
import rm_tables

# ------------ SETUP DATABASE -------------
aws = "postgresql+psycopg2://riskmit:Cracker70@usefulanalytics-instance.cjepocpyhpgj.us-east-2.rds.amazonaws.com/riskmit"
engine = create_engine(aws, echo=False)
Session = sessionmaker(bind=engine) # create a configured "Session" class
session = Session() # create a Session
metadata = MetaData()
Base = declarative_base()

# =========  DEFINE SCREENS  ===================
class LoginScreen(Screen):
    def __init__(self, **kw):
        super(LoginScreen,self).__init__(**kw)
    
    def on_pre_enter(self, *args):
        pass
        #Window.size = (400,500)

    def login(self):
        print('Login!')
        password_entered = self.ids.password.text
        username = self.ids.login.text
        #get password from db
        s = select(Users).where(Users.user_name == username)
        result = session.execute(s)
        for object in result.scalars():
            first_name = object.first_name
            last_name = object.last_name
            password = object.password
            user_name = object.user_name

        print("login :",username," Password : ", password_entered)
        try:
            if password_entered == password:
                print("you may pass")
                self.ids.welcome_label.text = 'AUTHORIZED!'
                self.parent.current = 'main_screen'
            else:
                print("Password is wrong")
                self.ids.welcome_label.text = "INCORRECT PASSWORD"
                self.ids.password.text = ""
                self.parent.current = 'main_screen' #login no matter what
        except UnboundLocalError:
            print ("User name does not exist")
            self.ids.welcome_label.text = "USERNAME DOES NOT EXIST"
            self.ids.password.text = ""
            self.ids.login.text =""
            self.parent.current = 'main_screen' #login no matter what
        
    def register(self):
        print("register!")
        self.parent.current = "register_screen"
class RegisterScreen(Screen):
    def __init__(self, **kw):
        super(RegisterScreen,self).__init__(**kw)
    
    def on_pre_enter(self, *args):
        pass
        #Window.size = (500,500)   
class MainScreen(Screen):
    def __init__(self, **kw):
        super(MainScreen,self).__init__(**kw)
    
    def on_pre_enter(self, *args):
        #Window.maximize
        pass
        #Window.size = (1000,600)

    def open_superuser(self):
        print("Opening settings")
        self.parent.current = 'super_user'

    def log_out(self):
        s1 = self.manager.get_screen('login_screen')
        s1.ids.welcome_label.text = "LOGIN"
        self.parent.current = 'login_screen'

class SuperUserScreen(Screen):
    def back_button(self):
        self.parent.current='main_screen'

    def create_tables(self):
        print("I'm going to create the tables now")
        rm_tables.Base.metadata.create_all(engine)
        print('Tables Created')
        
class Screen_Manager(ScreenManager):
    pass
class Tab(MDFloatLayout, MDTabsBase):
    '''Class implementing content for a tab.'''
    #content_text = StringProperty("")
    pass
class SettingsDrawer(MDBoxLayout):
    pass

    

# ========== MAIN CLASS =========================
class RiskMit(MDApp):
    
    # SET TITLE AND ICON
    def __init__(self, **kwargs):
        self.title = "RiskMit"
        super().__init__(**kwargs)
        self.icon = "fgwhite.png"

    # BUILD THE UI
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette ="Blue"
        self.theme_cls.accent_palette = "Green"
        #Window.size = (500,600)
        return Builder.load_file('kv_riskmit.kv')

    def on_tab_switch(self, instance_tabs, instance_tab, instance_tab_label, tab_text):
        pass

    
# ========== PROCESSING ===========



# ======== RUN APP =======================    
if __name__ == '__main__':
    RiskMit().run()

# SETUP DATABASE


