#import questrade_api as qt
from questrade_api import *
from riskmit_live_review import *
from datetime import datetime, timedelta
import configparser
import urllib
from tkinter import *
from tkinter import messagebox # even though everything was imported messagebox still needs to be implicidly imported
from tkinter import ttk, filedialog, simpledialog
import sqlite3
import pandas as pd
from pytz import timezone
import os, sys
from IPython.display import display
from contextlib import contextmanager # for database manager
import pyodbc  # for database manager
#import sys  # for database manager

button_width = 19
button_padding = 2
button_color1 = 'black'
button_color2 = 'blue'
button_color3 = 'grey'
button_text_color1 = 'white'
label_width = 30

database ='riskmit.db'

print('Drivers :',pyodbc.drivers())

# =================== DATA BASE CONNECTION MANAGER ==============
@contextmanager
def open_db_connection(commit=False):
    connection = pyodbc.connect('Driver = {QB SQL Anywhere}; Database = rismit.db; Trusted_Connection = yes;')
    cursor = connection.cursor()
    try:
        yield cursor
    except pyodbc.DatabaseError as err:
        error, = err.args
        sys.stderr.write(error.message)
        cursor.execute("ROLLBACK")
        raise err
    else:
        if commit:
            cursor.execute("COMMIT")
        else:
            cursor.execute("ROLLBACK")
    finally:
        connection.close()

    #call it using: - connection will close when you leave with this block
    #with open_db_connection("...") as cursor:
    # Your code here

# ================== CLOSE OTHER WINDOWS IF CLOSED =======================
#def close_window():
#    global running
#    running = False # turn off while loop
#    print('close_window was run')
#    accounts_window.w1.destroy()
 #   root.destroy()
   
# =========================== GUI =============================
root = Tk()
#root.protocol("WM_DELETE_WINDOW", close_window)
root.title("InvestInU Reporting")
#root.geometry("500x600")
root.iconbitmap('favicon.ico')
#root.columnconfigure(0, weight=1)
#root.columnconfigure(1, weight=3)
#--------- CLOSE OTHER WINDOWS IF CLOSED -----------------

running = True;
print("tkinter window is running")
# This is an endless loop stopped only by setting 'running' to 'False'
#while running:
 #   if not running:
 #       print('window close has been triggered')
 #       break
    #cv.create_oval(i, i, i+1, i+1)
    #root.update() 





# ------ TEST PRINT VARIABLES ---------------------
def test_print():
    token_path = token_path_set(master_account_combo.get())
    print('token_path_set() was run: ',token_path)

test_button = Button(root, text='TEST VARIABLES', command=lambda: test_print(), width=button_width, bg='white', fg='black')
test_button.grid(row=10, column=0, sticky="W", pady=(button_padding,10))

#============== SERVER TIME ========================
def server_time():
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
start_date_label.grid(row=24, column=1, sticky="W",pady=(10,0))

# ================================================================================
# ============================== SELECT MASTER ACCOUNT ===========================
def master_account_set(account, *args):
    global q
    print("Starting master_account_set. account : ",account)
    q = allinone_token_set(account)
    master_account_label.config(text=account)
    print('Master account set, q = ',q)
    return q

options = ["corporate1", "corporate2", "personal"]

master_account_label = Label(root, text=options[0], relief = "flat", width=label_width, anchor=W)
master_account_label.grid(row=0, column=1, sticky="W")
master_account_combo = ttk.Combobox(root, value=options, width=20)
master_account_combo.current(0)
master_account_combo.grid(row=0, column=0, sticky="W")
master_account_combo.bind('<<ComboboxSelected>>', lambda x: master_account_set(master_account_combo.get()))

master_account_set(master_account_combo.get())

#=================================================================================
# ================================ ACCOUNTS ======================================
def accounts():
    dict_accounts = q.accounts
    ma_name = master_account_combo.get()
    user_id = q.accounts['userId']
    df = pd.DataFrame.from_dict(q.accounts['accounts']) #de-nest the accounts dict and make df
    print('running accounts : ',df)
    print('user_id = ',user_id)
    
    # Set database accountID to ma name in master_accounts table
    conn = sqlite3.connect(database)
    c = conn.cursor()
    c.execute("UPDATE master_accounts SET account_id=? WHERE account_name=?",(user_id, ma_name))
    conn.commit() # Commit changes
    c.close()
    conn.close() # close data base
    return (df, user_id)


accounts_button = Button(root, text="ACCOUNTS", command = accounts, width=button_width, bg=button_color2, fg=button_text_color1)
accounts_button.grid(row=29, column=0, sticky="W")
accounts_label = Label(root, text=' ', relief = "flat")
accounts_label.grid(row=29, column=1, sticky="W",pady=(button_padding,0))

#==================================================================================
# ===================== ACCOUNT BALANCES ==========================================
def balances(id):
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
    dict_positions = q.account_positions(id)
    position_list = dict_positions['positions']
    df_positions = pd.DataFrame.from_dict(position_list)
    df_positions.sort_values(by='symbol',inplace=True) # sort by symbol
    df_positions.rename({'openQuantity':'open_qty','closedQuantity':'closed_qty' }, axis=1, inplace=True) # clean up column names
    display(df_positions)
    return df_positions

postions_button = Button(root, text="POSITIONS", command = lambda : account_positions('28148589'), width=button_width, bg=button_color2, fg=button_text_color1)
postions_button.grid(row=35, column=0, sticky="W")
postions_label = Label(root, text=' ', relief = "flat")
postions_label.grid(row=35, column=1, sticky="W",pady=(button_padding,0))

# =========================================================================
# ============ DATABASE ===================================================
#==========================================================================
def create_database():
    print('Running create database')
    conn = sqlite3.connect('riskmit.db')
    c = conn.cursor() #Create a cursor instance

    # ----------------------------------------------------------------
    # ------------ CREATE USER TABLE ---------------------------------
    # ----------------------------------------------------------------
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        user_name text unique,
        first_name text,
        last_name text
        )
        ''')

    # ---------------------------------------------------------------
    # ------------- CREATE MASTER ACCOUNT TABLE  --------------------
    # ---------------------------------------------------------------
    c.execute('''CREATE TABLE IF NOT EXISTS master_accounts(
            id integer PRIMARY KEY,
            account_id integer,
            account_name text unique
            )''')

    # ---------------------------------------------------------------
    # ------------ LIVE POSITIONS TABLE  ----------------------------
    # ---------------------------------------------------------------
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
# =============== END DATABASE ========================================

account_window_button = Button(root, text="ACCOUNT WINDOW", command = lambda: accounts_window(database),width=button_width, bg='green', fg=button_text_color1)
account_window_button.grid(row=50, column=0, sticky="W", pady=(button_padding,0))

create_database()
add_ma_users()
accounts_window(database) # OPEN LIVE ACCOUNT WINDOW









print('This is the last line in the code')
root.mainloop()
# ================== END GUI ==================
