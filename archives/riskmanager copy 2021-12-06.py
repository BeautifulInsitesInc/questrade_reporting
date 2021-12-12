# KIVY IMPORTS
import kivy
kivy.require('2.0.0')
from kivy.config import Config
#Config.set('graphics', 'width', '1200')
#Config.set('grafrom kivy.uix.screenmanager import Screenphics', 'height', '700')
#Config.write()

from sys import maxsize
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.factory import Factory
from kivy.core.window import Window
from kivy.metrics import dp

from kivymd.app import MDApp
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.icon_definitions import md_icons
from kivymd.theming import ThemeManager
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.card import MDCard

from kivymd.uix.button import MDRoundFlatButton


# DATABASE IMPORTS
from IPython.display import display
import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, MetaData, Table, select, delete
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.expression import null
from sqlalchemy import column
from sqlalchemy import create_engine
from sqlalchemy import select
from sqlalchemy import table
from sqlalchemy import text
from sqlalchemy import Integer

# ACCOUNT API IMPORTS
from rm_questrade_api import *
# CUSTOM FUCITION IMPORTS
from rm_tables import *
import rm_tables

# ------------ SETUP DATABASE -------------
aws = "postgresql+psycopg2://riskmit:Cracker70@usefulanalytics-instance.cjepocpyhpgj.us-east-2.rds.amazonaws.com/riskmit"
engine = create_engine(aws, echo=False)
#Session = sessionmaker(bind=engine) # create a configured "Session" class   
#Session = sessionmaker(engine)
#session = Session() # create a Session
metadata = MetaData()
Base = declarative_base()

# ROOT WIDGET
#class RiskMit(Screen):
#   pass

# =================  DEFINE SCREENS  =====================
# AUTHENTICATION SCREENS
class ScreenLogin(Screen):
    pass
class ScreenRegistration(Screen):
    def __init__(self, **kw):
        super(ScreenRegistration,self).__init__(**kw)
    
    def on_pre_enter(self, *args):
        pass
        #Window.size = (500,500)  
class ScreenMain(Screen):
    def __init__(self, **kw):
        super(ScreenMain,self).__init__(**kw)
class ScreenOverview(Screen):
    def __init__(self, **kw):
        super(ScreenOverview,self).__init__(**kw)
    
    def on_pre_enter(self, *args):
        #Window.maximize
        pass
        #Window.size = (1000,600)

    

    def log_out(self):
        s1 = self.manager.get_screen('screen_login')
        s1.ids.welcome_label.text = "LOGIN"
        self.parent.current = 'screen_login'

class ScreenManagerApp(ScreenManager):

    def open_superuser(self):
        print("Opening settings")
        self.parent.current = 'super_user'

    #def __init__(self, **kwargs):
     #   super(App.ScreenManager, self).__init__(**kwargs) 
class ScreenManagerMain(ScreenManager):
    def __init__(self, **kwargs):
        super(ScreenManagerMain, self).__init__(**kwargs)
        screen_manager_main = ObjectProperty()
        screenmanager_app = ObjectProperty()

    def open_superuser(self):
        print("Open Superuser!")

class Authentication(Widget):

    def login(username,password):
        print('Login!')
        username = username.text
        password = password.text
        #get password from db
        print ('Using:    Username : ', username,"   Password :",password)
        s = select(Users).where(Users.user_name == username)
        with engine.begin() as connection: #Open database and auto commit
            result = connection.execute(s)
            print("results : ",result)
        first_name = 'Does Note Exist'
        last_name = 'Does Note Exist'
        password_actual = 'Does Note Exist'
        username_actual = 'Does Note Exist'
        for object in result:
            try:
                print('object :',object)
                username_actual = object.user_name
                first_name = object.first_name
                last_name = object.last_name
                password_actual = object.password
            except:
                print('This is run because username is not found')
        print('actual values :', first_name, last_name, password_actual, username_actual)
        
        if username_actual == username and password_actual == password:
            print("you may pass")
            #app.ids.welcome_label.text = 'AUTHORIZED!'
            #app.screen_manager.current = 'overview'
        elif username_actual == username:
            print ('INCORECT PASSWORD')
        else:
            print("INCORRECT USERNAME")
            AppScreenManager.parent.current = "screen_main"
            #self.ids.welcome_label.text = "INCORRECT USERNAME"
            #self.ids.password.text = ""
        
    def register(self):
        print("register!")
        AppScreenManager.current = ScreenRegistration()


# MAIN SCREENS


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
class ScreenSuperuser(Screen):
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
class RiskManager(MDApp):
    #theme_cls = ThemeManager()
    
    # SET TITLE AND ICON
    def __init__(self, **kwargs):
        self.title = "RiskManager"
        self.icon = "assets/fgwhite.png"
        
        super().__init__(**kwargs)
        
    # BUILD THE UI
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette ="Blue"
        self.theme_cls.accent_palette = "Green"
               
        return Builder.load_file('riskmanager.kv')

    def on_tab_switch(self, instance_tabs, instance_tab, instance_tab_label, tab_text):
        pass

    def log_out(self):
        print("Log out Button Was pressed!")

# ========== PROCESSING ===========


# ======== RUN APP =======================    
if __name__ == '__main__':
    RiskManager().run()

# SETUP DATABASE


