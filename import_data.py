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
from PIL import ImageTk, Image # install pillow for images
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
export_folder ='D:\Dropbox\Test folder'
excel_file_full_path = 'D:\Dropbox\Test folder\riskmit_questrade.xlsx'
excel_filename = 'riskmit_questrade.xlsx'
access_token ='nil'
TOKEN_PATH = 'D:\Dropbox\- INVESTINU\- QUESTRADE_API EXPORTS\questrade.json'


# Moms token YaHqygHc1gSIvn3bcA1FT2Zp_sWgvSMr0

# =========================== GUI =============================
root = Tk()
root.title("InvestInU Reporting")
root.geometry("500x600")
root.iconbitmap('favicon.ico')

root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=3)

# =============== PRINT VARIABLES FOR TESTING ===========
def print_vars():
    print('----------------------------')
    print('master_account : ',master_account)
    print('export_folder :',export_folder)
    print('excel_filename :',excel_filename)
    print('excel_file_full_path :',excel_file_full_path)
    print('access_token :',access_token)
    print('-----------------------------')
    print('TOKEN_PATH = ', TOKEN_PATH)
    return()

print_vars_button = Button(root, text='PRINT VARIABLES', command=print_vars)
print_vars_button.grid(row=15, column=1, sticky="W", pady=(30,0))

# ================= SET TOKEN_PATH ===================
def token_path_set():
	global export_folder
	global master_account
	token_path = export_folder+'/'+master_account+'-questrade.json'
	print('Token Path Set : ',token_path)
	return(token_path)

TOKEN_PATH=token_path_set()

# =============== SELECT MASTER ACCOUNT =======================s
def master_account_set(*args):
    global master_account
    global TOKEN_PATH
    master_account = master_account_combo.get()
    master_account_label.config(text=master_account)
    TOKEN_PATH = token_path_set()
    print_vars()
    return()

options = ["corporate1", "corporate2", "personal"]

master_account_label = Label(root, text=options[0], relief = "flat")
master_account_label.grid(row=0, column=1, sticky="W")

master_account_combo = ttk.Combobox(root, value=options)
master_account_combo.current(0)
master_account_combo.grid(row=0, column=0, sticky="W")
master_account_combo.bind('<<ComboboxSelected>>', master_account_set)

# ======== EXPORT FOLDER SET ====================
def export_folder_set():
	global export_folder
	global TOKEN_PATH
	export_folder = filedialog.askdirectory(initialdir='/Dropbox')
	exportfolder_label.config(text = export_folder)
	TOKEN_PATH = export_folder+'/'+master_account+'-questrade.json'

exportfolder_button = Button(root, text="EXPORT FOLDER", command=export_folder_set)
exportfolder_button.grid(row=2, column=0, sticky="W", pady=(10,0))
exportfolder_label = Label(root, text=export_folder, relief = 'flat')
exportfolder_label.grid(row=2, column=1, sticky="W")#can pad with pady or padx

#============== SELECT EXCEL FILE ================
def excel_filename_set():
	global excel_file_full_path
	excel_file_full_path = filedialog.askopenfilename(initialdir='/Dropbox', title="Select Excel Workbook", filetypes=(("xlsx Fiel", ".xlsx"),("All Files","*.*")))
	print(excel_filename)
	excel_filename_label.config(text = excel_file_full_path)

excel_filename_button = Button(root, text="ACTIVE WORKBOOK", command=excel_filename_set)
excel_filename_button.grid(row=3, column=0, sticky="W", pady=(20,0))
excel_filename_label = Label(root, text=excel_file_full_path, relief = 'flat')
excel_filename_label.grid(row=3, column=1, sticky="W",pady=(20,0))#can pad with pady or padx

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
    return()

	# showinfo, showwarning, showerror, askquestion, askokcancel,askyesno

create_excel_button = Button(root, text="CREATE NEW WB", command=create_excel_wb)
create_excel_button.grid(row=4, column=0, sticky="W")
create_excel_label = Label(root, text=excel_filename, relief = 'flat')
create_excel_label.grid(row=4, column=1, sticky="W",pady=(20,0))#can pad with pady or padx

# ================ ACCESS TOKEN SET ==================================================
def access_token_set():
	global access_token
	access_token = simpledialog.askstring(title="ACCESS TOKEN", prompt='New Token : ')
    #access_token = access_token_input.get()
	print('access_token = ',access_token)
	access_token_label.config(text = "CURRENT TOKEN : "+str(access_token))


access_token_button = Button(root, text='ACCESS TOKEN', command=access_token_set)
access_token_button.grid(row=7, column=0, sticky="W")

access_token_label = Label(root, text='Enter Access Token', relief = "flat")
access_token_label.grid(row=7, column=1, sticky="W", pady=(20,0))

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
	return()

token_registration = Button(root, text="TOKEN REGISTRATION", command = token_registration_set)
token_registration.grid(row=20, column=0, sticky="W")

# ========== AFTET TOKEN IS REGISTERED USE THIS ======
def refresh_token_set():
	global q
	q = Questrade()
	print('Refresh token retrieved : ',q)
	return()

token_refresh = Button(root, text="TOKEN REFRESH", command = refresh_token_set)
token_refresh.grid(row=20, column=1, sticky="W")

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

server_time_button = Button(root, text="SERVER TIME", command = server_time)
server_time_button.grid(row=22, column=0, sticky="W")
server_time_label = Label(root, text=' ', relief = "flat")
server_time_label.grid(row=22, column=1, sticky="W",pady=(10,0))

time_name_button = Button(root, text="TIME NAME", command = time_name)
time_name_button.grid(row=23, column=0, sticky="W")
time_name_label = Label(root, text=' ', relief = "flat")
time_name_label.grid(row=23, column=1, sticky="W",pady=(10,0))

start_date_button = Button(root, text="START DATE", command = lambda: start_date(30))
start_date_button.grid(row=24, column=0, sticky="W")
start_date_label = Label(root, text=' ', relief = "flat")
start_date_label.grid(row=24, column=1, sticky="W",pady=(10,0))


# ============= ACCOUNTS ===========================
def accounts():
    global q
    global user_id
    global export_folder
    dict_accounts = q.accounts
    user_id = q.accounts['userId']
    df_accounts = pd.DataFrame.from_dict(q.accounts['accounts']) #de-nest the accounts dict and make df
    filename = os.path.join(export_folder, str(user_id)+'-accounts.xlsx')
    df_accounts.to_excel(filename, header=True, )
    #df_accounts.to_excel(excel_file_full_path, sheet_name="accounts", index=False)
    display(df_accounts)
    return(df_accounts)

accounts_button = Button(root, text="ACCOUNTS", command = lambda: accounts())
accounts_button.grid(row=30, column=0, sticky="W", pady=(10,0))

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
    return()

aio_token_button = Button(root, text="ALL-IN-ONE REGISTER", command = allinone_token_set)
aio_token_button.grid(row=21, column=0, sticky="W", pady=20)

aio_token_label = Label(root, text='NOT REGISTERED', relief = "flat")
aio_token_label.grid(row=21, column=1, sticky="W")

# ================  POSITIONS =============
def account_positions():
	global q
	dict_positions = q.account_positions(id)
	position_list = dict_positions['positions']
	df_positions = pd.DataFrame.from_dict(position_list)
	display(df_positions)
	#df_positions.to_excel(filename, header=True, )
	return('success')

# ===================== ACCOUNT BALANCES - COMBINED
def account_balances():
	global q
	filename = os.path.join(filefolder, id+'-balances-'+time_name()+'.xlsx')
	dict_balances = q.account_balances(id)
	df_combined_balances3 = pd.DataFrame.from_dict(dict_balances['sodPerCurrencyBalances'])# sod per Currency balances : The MOST ACCURATE to what is shown in account.
	df_combined_balances4= pd.DataFrame.from_dict(dict_balances['sodCombinedBalances'])# sod combined balances : Combined totals of sod per currency for use in 3rd row
	display(df_combined_balances3)
	display(df_combined_balances4)
	df_combined_balances3.to_excel(filename, header=True)
	df_combined_balances4.to_excel(filename, header=True)
	return('success')

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
