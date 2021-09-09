# AUTH.PY IMPORTS ==========
import os
import json
import time
from urllib import request
# QUESTRADE.PY IMPORTS =========
#import os
#import json
from datetime import datetime, timedelta
import configparser
import urllib
# DATA COLLECTION 
from tkinter import *
from tkinter import messagebox # even though everything was imported messagebox still needs to be implicidly imported
from tkinter import ttk, filedialog, simpledialog
#from PIL import ImageTk, Image # install pillow for images
from openpyxl.workbook import Workbook
from openpyxl import load_workbook
from openpyxl.styles import Font, Border, Side
from openpyxl.chart import PieChart, Reference, BarChart, LineChart
import sqlite3
import pandas as pd
from pytz import timezone
import sys
from IPython.display import display

master_account ='corporate1'
user_id="Nil"
export_folder ='D:\Dropbox\Test folder'
excel_file_full_path = 'D:\Dropbox\Test folder/reporting_test.xlsx'
excel_filename = 'riskmit_questrade.xlsx'
access_token ='nil'
TOKEN_PATH = 'D:\Dropbox\- INVESTINU\- QUESTRADE_API EXPORTS\questrade.json'
button_width = 19
button_padding = 2
button_color1 = 'black'
button_color2 = 'blue'
button_color3 = 'grey'
button_text_color1 = 'white'

label_width = 30

# Moms token YaHqygHc1gSIvn3bcA1FT2Zp_sWgvSMr0

# =========================== GUI =============================
root = Tk()
root.title("InvestInU Reporting")
#root.geometry("500x600")
root.iconbitmap('favicon.ico')
#root.columnconfigure(0, weight=1)
#root.columnconfigure(1, weight=3)

# =============== PRINT VARIABLES FOR TESTING ===========
def print_vars():
    print('----------------------------')
    print('master_account : ',master_account)
    print('user_id :',user_id)
    print('export_folder :',export_folder)
    print('excel_filename :',excel_filename)
    print('excel_file_full_path :',excel_file_full_path)
    print('access_token :',access_token)
    print('-----------------------------')
    print('TOKEN_PATH = ', TOKEN_PATH)

print_vars_button = Button(root, text='PRINT VARIABLES', command=print_vars, width=button_width, bg ='brown')
print_vars_button.grid(row=15, column=0, sticky="W", pady=(10,0))

# ================= SET TOKEN_PATH ===================
def token_path_set(account):
	global export_folder
	#global master_account
	token_path = export_folder+'/'+account+'-questrade.json'
	print('Token Path Set : ',token_path)
	return(token_path)

TOKEN_PATH=token_path_set(master_account)

# =============== SELECT MASTER ACCOUNT =======================s
def master_account_set(account, *args):
    global master_account
    global TOKEN_PATH
    #master_account = master_account_combo.get()
    #master_account_label.config(text=master_account)
    master_account = account
    master_account_label.config(text=account)
    TOKEN_PATH = token_path_set(account)
    allinone_token_set()
    #if 'normal'== w1.state(): # root.state getst he state of the window, normal means its open
    print_vars()

options = ["corporate1", "corporate2", "personal"]

master_account_label = Label(root, text=options[0], relief = "flat", width=label_width, anchor=W)
master_account_label.grid(row=0, column=1, sticky="W")

master_account_combo = ttk.Combobox(root, value=options, width=20)
master_account_combo.current(0)
master_account_combo.grid(row=0, column=0, sticky="W")
master_account_combo.bind('<<ComboboxSelected>>', lambda x: master_account_set(master_account_combo.get()))

# ======== EXPORT FOLDER SET ====================
def export_folder_set():
	global export_folder
	global TOKEN_PATH
	export_folder = filedialog.askdirectory(initialdir='/Dropbox')
	exportfolder_label.config(text = export_folder)
	TOKEN_PATH = export_folder+'/'+master_account+'-questrade.json'

exportfolder_button = Button(root, text="EXPORT FOLDER", command=export_folder_set, width=button_width, bg=button_color1, fg=button_text_color1)
exportfolder_button.grid(row=2, column=0, sticky="W", pady=(button_padding,0))
exportfolder_label = Label(root, text=export_folder, relief = 'flat', width=label_width, anchor=W)
exportfolder_label.grid(row=2, column=1, sticky="W", pady=(button_padding,0))#can pad with pady or padx

#============== SELECT ACTIVE EXCEL FILE ================
def excel_filename_set():
	global excel_file_full_path
	excel_file_full_path = filedialog.askopenfilename(initialdir=export_folder, title="Select Excel Workbook", filetypes=(("xlsx Fiel", ".xlsx"),("All Files","*.*")))
	print(excel_filename)
	excel_filename_label.config(text = excel_file_full_path)

excel_filename_button = Button(root, text="ACTIVE WORKBOOK", command=excel_filename_set, width=button_width, bg=button_color1, fg=button_text_color1)
excel_filename_button.grid(row=3, column=0, sticky="W", pady=(button_padding,0))
excel_filename_label = Label(root, text=excel_file_full_path, relief = 'flat', width=label_width, anchor=W)
excel_filename_label.grid(row=3, column=1, sticky="W",pady=(button_padding,0))#can pad with pady or padx

#============== CREATE NEW EXCEL FILE =================
def create_excel_wb():
    global excel_filename
    global excel_file_full_path
    wb=Workbook()
    ws=wb.active
    excel_filename = simpledialog.askstring(title="FILE NAME", prompt='NAME : ')
    excel_filename += ".xlsx"
    excel_file_full_path = export_folder+'/'+excel_filename
    wb.save(excel_file_full_path)
    messagebox.showinfo('CONFIRMATION', "A New Excel WB : "+excel_file_full_path)
    excel_filename_label.config(text = excel_file_full_path)
    create_excel_label.config(text =excel_filename)

	# showinfo, showwarning, showerror, askquestion, askokcancel,askyesno

create_excel_button = Button(root, text="CREATE NEW WB", command=create_excel_wb, width=button_width, bg=button_color1, fg=button_text_color1)
create_excel_button.grid(row=4, column=0, sticky="W",pady=(button_padding,0))
create_excel_label = Label(root, text=excel_filename, relief = 'flat', width=label_width, anchor=W)
create_excel_label.grid(row=4, column=1, sticky="W",pady=(button_padding,0))#can pad with pady or padx

# ================ ACCESS TOKEN SET ==================================================
def access_token_set():
    global access_token
    access_token = simpledialog.askstring(title="ACCESS TOKEN", prompt='New Token : ')
    #access_token = access_token_input.get()
    print('access_token = ',access_token)
    access_token_label.config(text = "CURRENT TOKEN : "+str(access_token))


access_token_button = Button(root, text='ACCESS TOKEN', command=access_token_set, width=button_width, bg=button_color1, fg=button_text_color1)
access_token_button.grid(row=7, column=0, sticky="W", pady=(button_padding,0))

access_token_label = Label(root, text='Enter Access Token', relief = "flat", width=label_width, anchor=W)
access_token_label.grid(row=7, column=1, sticky="W", pady=(button_padding,0))

# =========  QUESTRADE API WRAPPER --- QUESTRADE.PY ============
CONFIG_PATH = os.path.join(os.path.abspath(
    os.path.dirname(__file__)), 'questrade.cfg')

class Questrade:
    def __init__(self, **kwargs):
        if 'config' in kwargs:
            self.config = self.__read_config(kwargs['config'])
        else:
            self.config = self.__read_config(CONFIG_PATH)

        auth_kwargs = {x: y for x, y in kwargs.items() if x in
                       ['token_path', 'refresh_token']}

        self.auth = Auth(**auth_kwargs, config=self.config)

    def __read_config(self, fpath):
        config = configparser.ConfigParser()
        with open(os.path.expanduser(fpath)) as f:
            config.read_file(f)
        return config

    @property
    def __base_url(self):
        return self.auth.token['api_server'] + self.config['Settings']['Version']

    def __build_get_req(self, url, params):
        if params:
            url = self.__base_url + url + '?' + urllib.parse.urlencode(params)
            return urllib.request.Request(url)
        else:
            return urllib.request.Request(self.__base_url + url)

    def __get(self, url, params=None):
        req = self.__build_get_req(url, params)
        req.add_header(
            'Authorization',
            self.auth.token['token_type'] + ' ' +
            self.auth.token['access_token']
        )
        try:
            r = urllib.request.urlopen(req)
            return json.loads(r.read().decode('utf-8'))
        except urllib.error.HTTPError as e:
            return json.loads(e.read().decode('utf-8'))

    def __build_post_req(self, url, params):
        url = self.__base_url + url
        return urllib.request.Request(url, data=json.dumps(params).encode('utf8'))

    def __post(self, url, params):
        req = self.__build_post_req(url, params)
        req.add_header(
            'Authorization',
            self.auth.token['token_type'] + ' ' +
            self.auth.token['access_token']
        )
        try:
            r = urllib.request.urlopen(req)
            return json.loads(r.read().decode('utf-8'))
        except urllib.error.HTTPError as e:
            return json.loads(e.read().decode('utf-8'))

    @property
    def __now(self):
        return datetime.now().astimezone().isoformat('T')

    def __days_ago(self, d):
        now = datetime.now().astimezone()
        return (now - timedelta(days=d)).isoformat('T')

    @property
    def time(self):
        return self.__get(self.config['API']['time'])

    @property
    def accounts(self):
        return self.__get(self.config['API']['Accounts'])

    def account_positions(self, id):
        return self.__get(self.config['API']['AccountPositions'].format(id))

    def account_balances(self, id):
        return self.__get(self.config['API']['AccountBalances'].format(id))

    def account_executions(self, id, **kwargs):
        return self.__get(self.config['API']['AccountExecutions'].format(id), kwargs)

    def account_orders(self, id, **kwargs):
        if 'ids' in kwargs:
            kwargs['ids'] = kwargs['ids'].replace(' ', '')
        return self.__get(self.config['API']['AccountOrders'].format(id), kwargs)

    def account_order(self, id, order_id):
        return self.__get(self.config['API']['AccountOrder'].format(id, order_id))

    def account_activities(self, id, **kwargs):
        if 'startTime' not in kwargs:
            kwargs['startTime'] = self.__days_ago(1)
        if 'endTime' not in kwargs:
            kwargs['endTime'] = self.__now
        return self.__get(self.config['API']['AccountActivities'].format(id), kwargs)

    def symbol(self, id):
        return self.__get(self.config['API']['Symbol'].format(id))

    def symbols(self, **kwargs):
        if 'ids' in kwargs:
            kwargs['ids'] = kwargs['ids'].replace(' ', '')
        return self.__get(self.config['API']['Symbols'].format(id), kwargs)

    def symbols_search(self, **kwargs):
        return self.__get(self.config['API']['SymbolsSearch'].format(id), kwargs)

    def symbol_options(self, id):
        return self.__get(self.config['API']['SymbolOptions'].format(id))

    @property
    def markets(self):
        return self.__get(self.config['API']['Markets'])

    def markets_quote(self, id):
        return self.__get(self.config['API']['MarketsQuote'].format(id))

    def markets_quotes(self, **kwargs):
        if 'ids' in kwargs:
            kwargs['ids'] = kwargs['ids'].replace(' ', '')
        return self.__get(self.config['API']['MarketsQuotes'], kwargs)

    def markets_options(self, **kwargs):
        return self.__post(self.config['API']['MarketsOptions'], kwargs)

    def markets_strategies(self, **kwargs):
        return self.__post(self.config['API']['MarketsStrategies'], kwargs)

    def markets_candles(self, id, **kwargs):
        if 'startTime' not in kwargs:
            kwargs['startTime'] = self.__days_ago(1)
        if 'endTime' not in kwargs:
            kwargs['endTime'] = self.__now
        return self.__get(self.config['API']['MarketsCandles'].format(id), kwargs)

#=========================================================================
# ================ AUTH CLASS ============================================
# Needs TOKEN_PATH Global set
class Auth:
    def __init__(self, **kwargs):
        if 'config' in kwargs:
            self.config = kwargs['config']
        else:
            raise Exception('No config supplied')
        if 'token_path' in kwargs:
            self.token_path = kwargs['token_path']
        else:
            self.token_path = TOKEN_PATH
        if 'refresh_token' in kwargs:
            self.__refresh_token(kwargs['refresh_token'])

    def __read_token(self):
        try:
            with open(self.token_path) as f:
                str = f.read()
                return json.loads(str)
        except IOError:
            raise('No token provided and none found at {}'.format(TOKEN_PATH))

    def __write_token(self, token):
        with open(self.token_path, 'w') as f:
            json.dump(token, f)
        os.chmod(self.token_path, 0o600)

    def __refresh_token(self, token):
        req_time = int(time.time())
        r = request.urlopen(self.config['Auth']['RefreshURL'].format(token))
        if r.getcode() == 200:
            token = json.loads(r.read().decode('utf-8'))
            token['expires_at'] = str(req_time + token['expires_in'])
            self.__write_token(token)

    def __get_valid_token(self):
        try:
            self.token_data
        except AttributeError:
            self.token_data = self.__read_token()
        finally:
            if time.time() + 60 < int(self.token_data['expires_at']):
                return self.token_data
            else:
                self.__refresh_token(self.token_data['refresh_token'])
                self.token_data = self.__read_token()
                return self.token_data

    @property
    def token(self):
        return self.__get_valid_token()

# ============ SET ACCESS TOKEN ====================
def token_registration_set():
	global access_token
	global q
	q = Questrade(refresh_token=access_token)
	print('Token registered: ',q)

#token_registration = Button(root, text="TOKEN REGISTRATION", command = token_registration_set)
#token_registration.grid(row=20, column=0, sticky="W")

# ========== AFTET TOKEN IS REGISTERED USE THIS ======
def refresh_token_set():
	global q
	q = Questrade()
	print('Refresh token retrieved : ',q)
	return()

#token_refresh = Button(root, text="TOKEN REFRESH", command = refresh_token_set)
#token_refresh.grid(row=20, column=1, sticky="W")

#============== SERVER TIME ========================
def server_time():
    global q
    st=q.time
    server_time = st.get('time')
    #print('Server Time : ', server_time)
    server_time_label.config(text = server_time)
    return(server_time)

def time_name():
    timename = server_time().replace(':','-')
    print('server time afer replace :',timename)
    time_name_label.config(text = timename)
    return(timename)

def start_date(days_back):
    date_part = server_time()[:10]
    rest_of_it = server_time()[10:]
    date_format = "%Y-%m-%d"
    date_object = datetime.strptime(date_part, date_format)
    tdelta = timedelta(days=days_back)
    last_month_date_obj = date_object - tdelta
    last_month = last_month_date_obj.strftime(date_format)
    start = last_month + rest_of_it
    print('start date : ',start)
    start_date_label.config(text = start)
    return(start)

server_time_button = Button(root, text="SERVER TIME", command = server_time, width=button_width, bg=button_color2, fg=button_text_color1)
server_time_button.grid(row=22, column=0, sticky="W")
server_time_label = Label(root, text=' ', relief = "flat")
server_time_label.grid(row=22, column=1, sticky="W",pady=(button_padding,0))

time_name_button = Button(root, text="TIME NAME", command = time_name, width=button_width, bg=button_color2, fg=button_text_color1)
time_name_button.grid(row=23, column=0, sticky="W")
time_name_label = Label(root, text=' ', relief = "flat")
time_name_label.grid(row=23, column=1, sticky="W",pady=(button_padding,0))

start_date_button = Button(root, text="START DATE", command = lambda: start_date(30), width=button_width, bg=button_color2, fg=button_text_color1)
start_date_button.grid(row=24, column=0, sticky="W")
start_date_label = Label(root, text=' ', relief = "flat")
start_date_label.grid(row=24, column=1, sticky="W",pady=(button_padding,0))

# ========== ALL IN ONE TOKEN REFRESH ======
def allinone_token_set():
    global q
    global account_name
    global access_token
    try:
        q = Questrade()
        print('Refresh token retrieved : ',q)
        server_time()
        print('successful!')
        aio_token_label.config(text = "SUCCESSFUL! - "+master_account)
    except:
        print('There is an issue with the token ')
        aio_token_label.config(text = "Huston, We Have A Problem! - Token needs to be reset")
        access_token_set()
        q = Questrade(refresh_token=access_token)
        print('Refresh token retrieved : ',q)
        try:
            server_time()
            print('successful!')
            aio_token_label.config(text = "NEW REGISTRATION SUCCCESFUL! - "+master_account)
        except Exception:
            print('WE HAVE A BIGGER PROBLEM')

aio_token_button = Button(root, text="ALL-IN-ONE REGISTER", command = allinone_token_set, width=button_width, bg='yellow', fg='black')
aio_token_button.grid(row=21, column=0, sticky="W", pady=15)

aio_token_label = Label(root, text='NOT REGISTERED', relief = "flat")
aio_token_label.grid(row=21, column=1, sticky="W")

#=================================================================================
# ================================ ACCOUNTS ======================================
def accounts():
    global q
    global user_id
    dict_accounts = q.accounts
    user_id = q.accounts['userId']
    df = pd.DataFrame.from_dict(q.accounts['accounts']) #de-nest the accounts dict and make df
    print('running accounts : ',df)
    return df

accounts_button = Button(root, text="ACCOUNTS", command = accounts, width=button_width, bg=button_color2, fg=button_text_color1)
accounts_button.grid(row=29, column=0, sticky="W")
accounts_label = Label(root, text=' ', relief = "flat")
accounts_label.grid(row=29, column=1, sticky="W",pady=(button_padding,0))

#==================================================================================
# ===================== ACCOUNT BALANCES ==========================================
def balances(id):
    global q
    dict_balances = q.account_balances(id)
    df_combined_balances3 = pd.DataFrame.from_dict(dict_balances['sodPerCurrencyBalances'])# sod per Currency balances : The MOST ACCURATE to what is shown in account.
    df_combined_balances4 = pd.DataFrame.from_dict(dict_balances['sodCombinedBalances'])# sod combined balances : Combined totals of sod per currency for use in 3rd row
    display(df_combined_balances3)
    display(df_combined_balances4)
    return (df_combined_balances3, df_combined_balances4)

balances_button = Button(root, text="BALANCES", command = lambda : account_balances('28148589'), width=button_width, bg=button_color2, fg=button_text_color1)
balances_button.grid(row=30, column=0, sticky="W")
balances_label = Label(root, text=' ',   relief = "flat")
balances_label.grid(row=30, column=1, sticky="W",pady=(button_padding,0))

# ================================================================================
# ===================  POSITIONS ================================================
def positions(id):
    global q
    dict_positions = q.account_positions(id)
    position_list = dict_positions['positions']
    df_positions = pd.DataFrame.from_dict(position_list)
    df_positions.sort_values(by='symbol',inplace=True) # sort by symbol
    df_positions.rename({'openQuantity':'open_qty','closedQuantity':'closed_qty' }, axis=1, inplace=True) # clean up column names
    display(df_positions)
    #df_positions.to_excel(filename, header=True, )
    return df_positions

postions_button = Button(root, text="POSITIONS", command = lambda : account_positions('28148589'), width=button_width, bg=button_color2, fg=button_text_color1)
postions_button.grid(row=35, column=0, sticky="W")
postions_label = Label(root, text=' ', relief = "flat")
postions_label.grid(row=35, column=1, sticky="W",pady=(button_padding,0))


#========================================================================================
#----------- REVIEW WINDOW --------------------------------------------------------------
#========================================================================================

def accounts_window():
    print('accounts_window started')
    allinone_token_set()
    accounts()
    w1 = Toplevel(root)
    w1.geometry('1200x600')
    w1.title('ACCOUNTS')
    #style
    style=ttk.Style()
    #Theme
    style.theme_use('default')
    #Confirgure treeview colors
    style.configure("Treeview",
        background="#D3D3D3",
        foreground='black',
        rowheight=25,
        fieldbackground='#D3D3D3'
        )

    # CHANGE SELECTED COLOR
    style.map('Treeview',
        background=[('selected', '#347083')]
        )
    # ACCOUNTS WINDOW CLOSE
    close_button = Button(w1, text='CLOSE', command=w1.destroy)
    close_button.place(rely=.90, relx=.5)
    # --------------- MASTER ACCOUNT FRAME -----------------------------------------------------
    frame_ma = LabelFrame(w1, text="Master Account")
    frame_ma.place(x=5,y=5, height=100, width=250) # set the height and width

    # --------- ACCOUNTS FRAME ------------------------------------------------------------
    frame_accounts = LabelFrame(w1, text="Account Listing")
    frame_accounts.place(x=5, y=110, height=200, width=250) # set the height and width of Jake is a Bad Dog
    account_detail_button = Button(frame_accounts, text="DETAILS", command = lambda: account_detail_window(), width=button_width, bg=button_color1, fg=button_text_color1)
    account_detail_button.pack(pady=10)
    accounts_scroll = Scrollbar(frame_accounts) # add scroll bar
    accounts_scroll.pack(side=RIGHT, fill=Y)
    accounts_tree = ttk.Treeview(frame_accounts, yscrollcommand=accounts_scroll.set, selectmode="extended")
    accounts_tree.pack()
    accounts_scroll.config(command=accounts_tree.yview)

    # ----------- BALANCE FRAME ------------------------------------------------------------------
    frame_balance = LabelFrame(w1, text="Balances")
    frame_balance.place(x=260, y=5, height=100, width=800)

    # ------- POSITIONS FRAME
    frame_positions = LabelFrame(w1, text="Positions")
    frame_positions.place(x=260, y=110, height=400, width=400)
    positions_detail_button = Button(frame_positions, text="DETAILS", command = lambda: position_detail_window(), width=button_width, bg=button_color1, fg=button_text_color1)
    positions_detail_button.pack(pady=10)
    positions_scroll = Scrollbar(frame_positions) # add scroll bar
    positions_scroll.pack(side=RIGHT, fill=Y)
    positions_tree = ttk.Treeview(frame_positions, yscrollcommand=positions_scroll.set, selectmode="extended")
    positions_tree.pack()
    accounts_scroll.config(command=positions_tree.yview)

    #============================================================================
    # ============= MASTER ACCOUNT FRAME ========================================
    # ====================================================================
    def draw_ma():
        print('running draw_ma')
        global options
        global user_id
        global user_id_lable
        ma_combo = ttk.Combobox(frame_ma, value=options, width=20)
        ma_combo.current(0) # Set default to first master account
        ma_combo.grid(row=0, column=0, sticky="W")
        print('about to run master_account_set')
        ma_combo.bind('<<ComboboxSelected>>', lambda x: master_account_change(ma_combo.get())) # New MA choosen - start updating the account lists
        user_id_lable = Label(frame_ma, text='ID: '+str(user_id), relief = "flat")
        user_id_lable.grid(row=2, column=0, pady=5, sticky='W')
        print('setting token')
        #allinone_token_set()
        print("token set, drawing accounts")
        #draw_accounts()
        print('complete')
        return()

    # GRAB THE MASTER ACCOUNT CHOOSEN AND UPDATE ACCOUNT LIST
    def master_account_change(masteraccount):
            print('running master_account_change')
            global user_id_lable
            positions_tree.delete(*positions_tree.get_children()) # clear any previous tree
            accounts_tree.delete(*accounts_tree.get_children()) # clear any previous tree  
            master_account_set(masteraccount) #switch token to correction account
            allinone_token_set() # connect to new token
            accounts() #renew acounts to get new id
            draw_accounts() #redraw them on screen 
            user_id_lable.config(text='ID: '+str(user_id))

    # ======================================================================================
    # GRAB THE ACCOUNT NUMBER THAT WAS CLICKED
    # ==============================================================
    def select_account(e):
        selected = accounts_tree.focus() # Gab record number
        values = accounts_tree.item(selected, 'values') # Grap tuple of row values
        account_number = values[1] # Assign selected Account Number
        #print("Account number: ", account_number)
        return(account_number)

    # =================================================================================
    # ============== POSITION FRAME ===================================================
    # ==================================================================================
    def draw_positions(e):
        global account_number
        account_number = select_account(e)
        print("Account number: ", account_number)
        print("type :", type(account_number))
        positions_tree.delete(*positions_tree.get_children()) # clear any previous tree
        w1.update() #refresh window
        df_pos = positions(account_number)
        print("Running position display: ")
        df_pos_summary = df_pos
        df_pos_summary = df_pos_summary.drop(['symbolId','dayPnl','isRealTime','isUnderReorg'], axis=1)
        #df_summary = df_summary.drop(['status','isPrimary','isBilling'], axis=1)
        # COLUMN HEADINGS
        positions_tree['columns'] = list(df_pos_summary.columns)
        positions_tree['show']= 'headings'
        for column in positions_tree['columns']:
            positions_tree.heading(column, text=column)
            positions_tree.column(column, width=70)
        # PRINT ROWS
        df_rows = df_pos_summary.to_numpy().tolist() #turns dataframe into list of lists
        for row in df_rows:
            positions_tree.insert("", "end", values=row)
        # BINDING
        #positions_tree.bind('<ButtonRelease-1>', position_clicked)

    def position_detail_window():
            w3 = Toplevel(root)
            w3.geometry('1000x400')
            w3.title('POSITIONS')
            # CLOSE BUTTON
            close_button = Button(w3, text='CLOSE', command=w3.destroy) 
            close_button.pack()
            # CREATE TREE
            positions_detail_tree = ttk.Treeview(w3)
            positions_detail_tree.pack()
            positions_detail_tree.delete(*positions_detail_tree.get_children()) # clear any previous tree
            #w3.update() #refresh window
            df_pos_detail = positions(account_number)
            # COLUMN HEADINGSs
            positions_detail_tree['columns'] = list(df_pos_detail.columns)
            positions_detail_tree['show']= 'headings'
            for column in positions_detail_tree['columns']:
                positions_detail_tree.heading(column, text=column)
                positions_detail_tree.column(column, width=70)
            # ROWS
            df_rows = df_pos_detail.to_numpy().tolist() #turns dataframe into list of lists
            for row in df_rows:
                positions_detail_tree.insert("", "end", values=row)

    # ===============================================================================
    # ============== ACCOUNT LIST FRAME =============================================
    # ==============================================================================
    def draw_accounts():
        accounts_tree.delete(*accounts_tree.get_children()) # clear any previous tree
        w1.update() #refresh window
        df = accounts()
        df_summary = df
        df_summary = df_summary.drop(['status','isPrimary','isBilling'], axis=1)
        # COLUMN HEADINGS
        accounts_tree['columns'] = list(df_summary.columns)
        accounts_tree['show']= 'headings'
        for column in accounts_tree['columns']:
            accounts_tree.heading(column, text=column)
            accounts_tree.column(column, width=70)
        # PRINT ROWS
        df_rows = df_summary.to_numpy().tolist() #turns dataframe into list of lists
        for row in df_rows:
            accounts_tree.insert("", "end", values=row)
        # BINDING
        accounts_tree.bind('<ButtonRelease-1>', account_clicked)

    # ------------ ACCOUNT DETAIL WINDOW -------------------------------
    def account_detail_window(): 
            w2 = Toplevel(root)
            w2.geometry('1000x400')
            w2.title('ACCOUNTS')
            # CLOSE BUTTON
            close_button = Button(w2, text='CLOSE', command=w2.destroy) 
            close_button.pack()
            # CREATE TREE
            accounts_detail_tree = ttk.Treeview(w2)
            accounts_detail_tree.pack()
            #accounts_detail_tree.delete(*accounts_detail_tree.get_children()) # clear any previous tree
            #w2.update() #refresh window
            df = accounts()
            # COLUMN HEADINGSs
            accounts_detail_tree['columns'] = list(df.columns)
            accounts_detail_tree['show']= 'headings'
            for column in accounts_detail_tree['columns']:
                accounts_detail_tree.heading(column, text=column)
                accounts_detail_tree.column(column, width=70)
            # ROWS
            df_rows = df.to_numpy().tolist() #turns dataframe into list of lists
            for row in df_rows:
                accounts_detail_tree.insert("", "end", values=row)

    # ================   ACCOUNT HAS BEEN CLICKED - POPULATE THE FRAMES ====================
    def account_clicked(e):
        positions_tree.delete(*positions_tree.get_children()) # clear any previous tree
        draw_positions(e) # Send selected account number to draw positions

        

    draw_ma()
    draw_accounts()

    w1.mainloop()

    #==========     END OF WINDOW LOOP ====================================

# =========================================================================
# ============ DATABASE ===================================================
#==========================================================================
def create_database():
    conn = sqlite3.connect('riskmit.db')
    c = conn.cursor() #Create a cursor instance
    #  ------------ user table ---------------------
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id integer PRIMARYH KEY,
        user_name text unique,
        first_name text,
        last_name text,
        
        user_id integer)
        ''')

    # ------------- master account table -------------
    c.execute('''CREATE TABLE IF NOT EXISTS master_accounts(
            id integer PRIMARY KEY,
            account_id integer,
            account_name text unique
            )''')
    # ------------ live positions -----------------
    #c.execute('''CREATE TABLE if not exists positions (
    #    
    #    )
    #    ''')



    conn.commit() # Commit changes
    c.close()
    conn.close() # close data base



#create_database()

# ------ ADD USERS TO MASTER ACCOUNT LIST -------
def add_ma_users():
    global options
    conn = sqlite3.connect('riskmit.db')
    c = conn.cursor()
    for name in options:
        try:
            c.execute('''INSERT INTO master_accounts (account_id, account_name) VALUES (? ,?)''',(666, name))
            print('Master Account Added')
        except:
            print('WARRNING: MASTER ACCOUNT ALREADY EXISTS')
    
    conn.commit()
    #querry database
    c.execute("SELECT * FROM users")
    records = c.fetchall()
    print(records)

     # Commit changes
    conn.close()


create_database()
add_ma_users()


accounts_button = Button(root, text="ACCOUNTS", command = lambda: accounts(), width=button_width, bg=button_color2, fg=button_text_color1)
accounts_button.grid(row=31, column=0, sticky="W", pady=(button_padding,0))

account_window_button = Button(root, text="ACCOUNT WINDOW", command = lambda: accounts_window(),width=button_width, bg='green', fg=button_text_color1)
account_window_button.grid(row=50, column=0, sticky="W", pady=(button_padding,0))

accounts_window()

    


# ORDERS
def orders(start_time):
	global q
	filename = os.path.join(filefolder, id+'-orders-'+time_name()+'.xlsx')
	dict_orders = q.account_orders(id, startTime=start_time)
	df_orders = pd.DataFrame.from_dict(dict_orders['orders'])
	display(df_orders)
	#df_orders.to_excel(filename, header=True)
	return('success')

# EXECUTIONS
def executions(start_time):
	global q
	filename = os.path.join(filefolder, id+'-executions-'+time_name()+'.xlsx')
	print(filepath)
	dict_executions = q.account_executions(id, startTime=start_time)
	df_executions = pd.DataFrame.from_dict(dict_executions['executions'])
	display(df_executions)
	df_executions.to_excel(filename, header=True)
	return('success')

# ACCOUNT ACTIVITIES --- only 30 days
def activities():
	global q
	#filename = os.path.join(filefolder, id+'-activities-'+time_name()+'.xlsx')
	dict_activities = q.account_activities(id, startTime=start_date(30))
	df_activities = pd.DataFrame.from_dict(dict_activities['activities'])
	display(df_activities)
	df_activities.to_excel(filename, header=True, )
	return('success')




root.mainloop()
# ================== END GUI ==================
