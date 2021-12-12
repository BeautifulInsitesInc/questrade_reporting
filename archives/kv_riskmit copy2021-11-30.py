# KIVY IMPORTS
import kivy
kivy.require('2.0.0')
from kivy.config import Config
#Config.set('graphics', 'width', '1200')
#Config.set('grafrom kivy.uix.screenmanager import Screenphics', 'height', '700')
Config.write()

from sys import maxsize
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen
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
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.card import MDCard
from kivy.metrics import dp

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
from rm_tables import *
import rm_tables



# ------------ SETUP DATABASE -------------
aws = "postgresql+psycopg2://riskmit:Cracker70@usefulanalytics-instance.cjepocpyhpgj.us-east-2.rds.amazonaws.com/riskmit"
engine = create_engine(aws, echo=False)
Session = sessionmaker(bind=engine) # create a configured "Session" class   
session = Session() # create a Session
metadata = MetaData()
Base = declarative_base()

# ROOT WIDGET
class RiskMit(Screen):
    pass

# =================  DEFINE SCREENS  =====================
# AUTHENTICATION SCREENS
class ScreenLogin(Screen):
    def __init__(self, **kw):
        super(ScreenLogin,self).__init__(**kw)
    
    def on_pre_enter(self, *args):
        pass
        #Window.size = (800,500)

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
                root.screen_manager.current = 'overview'
            else:
                print("Password is wrong")
                self.ids.welcome_label.text = "INCORRECT PASSWORD"
                self.ids.password.text = ""
                root.screen_manager.current = 'overview' #login no matter what
        except UnboundLocalError:
            print ("User name does not exist")
            self.ids.welcome_label.text = "USERNAME DOES NOT EXIST"
            self.ids.password.text = ""
            self.ids.login.text =""
            root.screen_manager.current = "overview" #login no matter what
        
    def register(self):
        print("register!")
        self.parent.current = "register_screen"
class ScreenRegistration(Screen):
    def __init__(self, **kw):
        super(ScreenRegistration,self).__init__(**kw)
    
    def on_pre_enter(self, *args):
        pass
        #Window.size = (500,500)   
# MAIN SCREENS
class ScreenMain(Screen):
    pass
class ScreenOverview(Screen):
    def __init__(self, **kw):
        super(ScreenOverview,self).__init__(**kw)
    
    def on_pre_enter(self, *args):
        #Window.maximize
        pass
        #Window.size = (1000,600)

    def open_superuser(self):
        print("Opening settings")
        self.parent.current = 'super_user'

    def log_out(self):
        s1 = self.manager.get_screen('screen_login')
        s1.ids.welcome_label.text = "LOGIN"
        self.parent.current = 'screen_login'
class PostionsScreen(Screen):
    pass
class OrdersScreen(Screen):
    pass
class BidsScreen(Screen):
    pass
class TradeScreen(Screen):
    pass
class JournalScreen(Screen):
    pass
class SettingsScreen(Screen):
    pass

# SUPER USER SCREENS
class SuperUserScreen(Screen):
    def back_button(self):
        self.parent.current='overview'

    def create_tables(self):
        print("I'm going to create the tables now")
        rm_tables.Base.metadata.create_all(engine)
        print('Tables Created')
class UserManagementScreen(Screen):

    def load_data(self):
        print('running load data')
        self.user_table = MDDataTable(size_hint = (1,1),
            column_data=[("UserName", dp(30)),
                ("Password", dp(30)),
                ("First Name",dp(30)),
            ],
            row_data=[("test","test","test"),
                ("test2", "test2", "test2"),
            ])
        self.ids.main_su.add_widget(self.user_table)
class AccountManagementScreen(Screen):
    pass

# SCREEN MANAGERS
class LoginScreenManager(ScreenManager):
    def __init__(self, **kwargs):
        super(LoginScreenManager, self).__init__(**kwargs)
class MainScreenManager(ScreenManager):
    def __init__(self, **kwargs):
        super(MainScreenManager, self).__init__(**kwargs)

class ContentNavigationDrawer(MDBoxLayout):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()


class Tab(MDFloatLayout, MDTabsBase):
    '''Class implementing content for a tab.'''
    #content_text = StringProperty("")
    pass

class SettingsDrawer(MDBoxLayout):
    pass

# ========== MAIN CLASS =========================
class RiskMit(MDApp):
    #theme_cls = ThemeManager()
    
    # SET TITLE AND ICON
    def __init__(self, **kwargs):
        self.title = "RiskMit"
        self.icon = "assets/fgwhite.png"
        
        super().__init__(**kwargs)
        
    # BUILD THE UI
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette ="Blue"
        self.theme_cls.accent_palette = "Green"
        # Create Screen Managers
        #sm1 = ScreenManager()
        #sm1.add_widget(Screen(name='login_screen'))
        #sm1.add_widget(Screen(name='register_screen'))
        #sm1.add_widget(Screen(name='super_user'))
        #sm2 = ScreenManager()
        #sm2.add_widget(Screen(name='overview'))
        #sm2.add_widget(Screen(name='positions'))
        #sm2.add_widget(Screen(name='orders'))
        
        
        return Builder.load_file('kv_riskmit.kv')


    def on_tab_switch(self, instance_tabs, instance_tab, instance_tab_label, tab_text):
        pass

    
# ========== PROCESSING ===========



# ======== RUN APP =======================    
if __name__ == '__main__':
    RiskMit().run()

# SETUP DATABASE


