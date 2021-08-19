#from questrade_api.auth import Auth
import sys
import os
#from questrade_api import Questrade
#from questrade_api.questrade import Questrade
import pandas as pd
#import datetime
from datetime import datetime, timedelta
from pytz import timezone

# SET TOKEN PATH
#def set_token_path(masteraccount,exportfolder):
#    print('running set_token_path funtion')
 #   TOKEN_PATH = 'token-'+master_account+"-questrade.json"
 #   print(TOKEN_PATH)
 #   return()
    
# INTIALLY SET ACCESS TOKEN
#def set_inital_access_token():
 #   token = input('Refresh Token: ')
 #   q = Questrade(refresh_token=token)
 #   print('token :',token)
 #   print(q)
 #   return()

# AFTER TOKEN HAS BEEN REGISTER USE THIS
#def set_refresh_token():
 #   q = Questrade()
 #   print(q)
 #   return()

# TIME
def server_time():
    st=q.time
    server_time = st.get('time')
    return server_time

def time_name():
    timename = server_time().replace(':','-')
    return timename

def start_date(days_back):
    date_part = server_time()[:10]
    rest_of_it = server_time()[10:]
    date_format = "%Y-%m-%d"
    date_object = datetime.strptime(date_part, date_format)
    tdelta = timedelta(days=days_back)
    last_month_date_obj = date_object - tdelta
    last_month = last_month_date_obj.strftime(date_format)
    start_date = last_month + rest_of_it
    return(start_date)
    
# Set file foler path for exports
#filefolder = 'D:\Dropbox\- INVESTINU\- QUESTRADE_API EXPORTS\ACCOUNT 1'
#filefolder = 'D:\Dropbox\- INVESTINU\- QUESTRADE_API EXPORTS\ACCOUNT 2'
#print('using :', filefolder)

# ACCOUNTS
def accounts(*kwargs):
    dict_accounts = q.accounts
    user_id = q.accounts['userId']
    df_accounts = pd.DataFrame.from_dict(q.accounts['accounts']) #de-nest the accounts dict and make df
    filename = os.path.join(exportfolder, user_id+'-accounts.xlsx')
    #df_accounts.to_excel(filename, header=True, )
    return('success')

# GET ACCOUNT ID
#id = input('Enter Account ID :')
#id = '28231880'
#print('Using Account: ',id)


# ACCOUNT POSITIONS
def account_positions(*kwargs):
    #filename = os.path.join(filefolder, id+'-positions-'+time_name()+'.xlsx')
    dict_positions = q.account_positions(id)
    #print(dict_positions)
    position_list = dict_positions['positions']
    df_positions = pd.DataFrame.from_dict(position_list)
    display(df_positions)
    #df_positions.to_excel(filename, header=True, )
    return('success')

# ACCOUNT BALANCES - COMBINED
def account_balances(*kwargs):
    filename = os.path.join(filefolder, id+'-balances-'+time_name()+'.xlsx')
    dict_balances = q.account_balances(id)
    #combined_balances1 = dict_balances['perCurrencyBalances']
    #combined_balances2 = dict_balances['combinedBalances']
    #combined_balances3 = dict_balances['sodPerCurrencyBalances']
    #combined_balances4 = dict_balances['sodCombinedBalances']
    df_combined_balances1 = pd.DataFrame.from_dict(dict_balances['perCurrencyBalances'])  #Per balances: True CAD and USD native amounts
    df_combined_balances2 = pd.DataFrame.from_dict(dict_balances['combinedBalances'])  #combined : each row is TOTAL value in that currency - could be used for the 3rd row : combined in CAD
    df_combined_balances3 = pd.DataFrame.from_dict(dict_balances['sodPerCurrencyBalances'])# sod per Currency balances : The MOST ACCURATE to what is shown in account.
    df_combined_balances4= pd.DataFrame.from_dict(dict_balances['sodCombinedBalances'])# sod combined balances : Combined totals of sod per currency for use in 3rd row
    #display(df_combined_balances1)
    #display(df_combined_balances2)
    display(df_combined_balances3)
    display(df_combined_balances4)
    df_combined_balances3.to_excel(r'D:\Dropbox\- INVESTINU\- QUESTRADE_API EXPORTS\ACCOUNT 2\combined_currency_balances.xlsx', header=True, )
    df_combined_balances4.to_excel(r'D:\Dropbox\- INVESTINU\- QUESTRADE_API EXPORTS\ACCOUNT 2\combined_total_balances.xlsx', header=True, )
    df_combined_balances3.to_excel(filename, header=True)
    df_combined_balances4.to_excel(filename, header=True)
    return('success')


# ORDERS
def orders(start_time):
    #filename = os.path.join(filefolder, id+'-orders-'+time_name()+'.xlsx')
    dict_orders = q.account_orders(id, startTime=start_time)
    df_orders = pd.DataFrame.from_dict(dict_orders['orders'])
    #display(df_orders)
    #df_orders.to_excel(filename, header=True)
    return('success')

# INDIVIDUAL ORDER DETAIL
#dict_order = q.account_order(id, 906251374)
#dict_order['orders']
#df_order = pd.DataFrame.from_dict(dict_order['orders'])
#display(df_order)

# EXECUTIONS
def executions(start_time):
    #filename = os.path.join(filefolder, id+'-executions-'+time_name()+'.xlsx')
    #print(filepath)
    dict_executions = q.account_executions(id, startTime=start_time)
    #dict_executions
    df_executions = pd.DataFrame.from_dict(dict_executions['executions'])
    display(df_executions)
    df_executions.to_excel(filename, header=True, )
    return('success')

# ACCOUNT ACTIVITIES --- only 30 days
def activities(q):
    #filename = os.path.join(filefolder, id+'-activities-'+time_name()+'.xlsx')
    dict_activities = q.account_activities(id, startTime=start_date(30))
    df_activities = pd.DataFrame.from_dict(dict_activities['activities'])
    display(df_activities)
    df_activities.to_excel(filename, header=True, )
    return('success')


# SYMBOL - uses symbole idonly
#dict_symbol = q.symbol(34231109)
#dict_symbol
#df_symbol = pd.DataFrame.from_dict(dict_symbol['symbols'])
#display(df_symbol)


# SYMBOLs - can use symbols or id
#dict_symbols = q.symbols(ids='34231109,34856813')
#dict_symbols
#df_symbols = pd.DataFrame.from_dict(dict_symbols['symbols'])
#display(df_symbols)

