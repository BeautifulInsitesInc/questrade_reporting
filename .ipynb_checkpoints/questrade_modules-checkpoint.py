#!/usr/bin/env python
# coding: utf-8

# https://pypi.org/project/questrade-api/

# In[75]:


import sys
import os
#from questrade_api import Questrade
from questrade_api.questrade import Questrade
import pandas as pd
#import datetime
from datetime import datetime, timedelta
from pytz import timezone


# In[79]:


# SET TOKEN PATH

def set_token_path():
    global TOKEN_PATH
    print('SET QUESTRADE ACCOUNT')
    print('1 - Corporate 1')
    print('2 - Corporate 2')
    print('3 - Personsal')
    account_name_number = input('Choose Account : (1-3)')
    if account_name_number == '1':
        account_name= 'corporate1'
    elif account_name_number == '2':
        account_name = 'corporate2'
    elif account_name_number == '3':
        account_name = 'personal'
    else:
        account_name = 'dumbass'
    if account_name:
        print('account_name : ',account_name)
    TOKEN_PATH = 'token-'+account_name+"-questrade.json"
    print(TOKEN_PATH)
    return(TOKEN_PATH)
    
set_token_path()
print('TOKEN_PATH = ',TOKEN_PATH)

    
    


# In[80]:


# INTIALLY SET ACCESS TOKEN

def set_access_token():
    token = input('Refresh Token: ')
    q = Questrade(refresh_token=token)
    print('token :',token)
    print(q)
    return()

set_access_token()


# In[81]:


# AFTER TOKEN HAS BEEN REGISTER USE THIS

def set_refresh_token():
    q = Questrade()
    print(q)
    return()
    
set_refresh_token()


# In[83]:


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
    
    
print(server_time())
print(time_name())
start_date(30)
print(start_date(30))


# In[14]:


# Set file foler path for exports
filefolder = 'D:\Dropbox\- INVESTINU\- QUESTRADE_API EXPORTS\ACCOUNT 1'
#filefolder = 'D:\Dropbox\- INVESTINU\- QUESTRADE_API EXPORTS\ACCOUNT 2'
print('using :', filefolder)


# In[84]:


# ACCOUNTS
def accounts():
    
    dict_accounts = q.accounts
    dict_accounts
    user_id = q.accounts['userId']
    print('user_id :',user_id)
    df_accounts = pd.DataFrame.from_dict(q.accounts['accounts']) #de-nest the accounts dict and make df
    display(df_accounts)
    filename = os.path.join(filefolder, '-accounts.xlsx')
    df_accounts.to_excel(filename, header=True, )
    return('success')

accounts()


# In[17]:


# GET ACCOUNT ID

id = input('Enter Account ID :')
#id = '28231880'
print('Using Account: ',id)


# In[18]:


# ACCOUNT POSITIONS
def account_positions():
    filename = os.path.join(filefolder, id+'-positions-'+time_name()+'.xlsx')
    dict_positions = q.account_positions(id)
    #print(dict_positions)
    position_list = dict_positions['positions']
    df_positions = pd.DataFrame.from_dict(position_list)
    display(df_positions)
    df_positions.to_excel(filename, header=True, )
    return('success')

account_positions()


# In[19]:


# ACCOUNT BALANCES - COMBINED

def account_balances():
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

account_balances()


# In[20]:


# ORDERS
def orders(start_time):
    filename = os.path.join(filefolder, id+'-orders-'+time_name()+'.xlsx')
    dict_orders = q.account_orders(id, startTime=start_time)
    df_orders = pd.DataFrame.from_dict(dict_orders['orders'])
    #display(df_orders)
    df_orders.to_excel(filename, header=True)
    return('success')

orders('2021-01-01T00:00:00-0')


# In[21]:


# INDIVIDUAL ORDER DETAIL
dict_order = q.account_order(id, 906251374)
dict_order['orders']
df_order = pd.DataFrame.from_dict(dict_order['orders'])
display(df_order)


# In[22]:


# EXECUTIONS
def executions(start_time):
    filename = os.path.join(filefolder, id+'-executions-'+time_name()+'.xlsx')
    #print(filepath)
    dict_executions = q.account_executions(id, startTime=start_time)
    #dict_executions
    df_executions = pd.DataFrame.from_dict(dict_executions['executions'])
    display(df_executions)
    df_executions.to_excel(filename, header=True, )
    return('success')

executions('2021-01-01T00:00:00-0')


# In[23]:


# ACCOUNT ACTIVITIES --- only 30 days
def activities():
    filename = os.path.join(filefolder, id+'-activities-'+time_name()+'.xlsx')
    dict_activities = q.account_activities(id, startTime=start_date(30))
    #print(dict_activities)
    df_activities = pd.DataFrame.from_dict(dict_activities['activities'])
    display(df_activities)
    df_activities.to_excel(filename, header=True, )
    return('success')

activities()


# In[17]:


# SYMBOL - uses symbole idonly

dict_symbol = q.symbol(34231109)
dict_symbol
df_symbol = pd.DataFrame.from_dict(dict_symbol['symbols'])
display(df_symbol)


# In[18]:


# SYMBOLs - can use symbols or id

dict_symbols = q.symbols(ids='34231109,34856813')
dict_symbols
df_symbols = pd.DataFrame.from_dict(dict_symbols['symbols'])
display(df_symbols)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




