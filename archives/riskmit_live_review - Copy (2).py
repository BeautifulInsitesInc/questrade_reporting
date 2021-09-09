# AUTH.PY IMPORTS ==========
from questrade_api import *
from tkinter import *
from tkinter import messagebox # even though everything was imported messagebox still needs to be implicidly imported
from tkinter import ttk, filedialog, simpledialog
import sqlite3
import pandas as pd
from pytz import timezone
import sys
from IPython.display import display
from pandastable import Table

label_width = 30
button_width = 15
button_height = 10
button_color1 = 'grey'
button_text_color1 = 'black'

#========================================================================================
#----------- REVIEW WINDOW --------------------------------------------------------------
#========================================================================================
def accounts_window(database):
    print('accounts_window started')
    w1 = Tk()
    w1.state('zoomed')
    #w1.geometry('1500x780')
    w1.title('ACCOUNTS')
    style=ttk.Style()
    style.theme_use('default')
    style.configure("Treeview",#Confirgure treeview colors
        background="#D3D3D3",
        foreground='black',
        rowheight=25,
        fieldbackground='#D3D3D3'
        )
    style.map('Treeview',# CHANGE SELECTED COLOR
        background=[('selected', '#347083')]
        )
    
# FRAME DIMENTIONS --------------
    w1.update()
    window_height = w1.winfo_height()
    window_width = w1.winfo_width()
    label_width = 30
    button_width = 15
    button_height = 1
    button_color1 = 'light grey'
    button_text_color1 = 'black'
    space=5
    tb_x, tb_y, tb_h, tb_w = space, space, window_height*.08, window_width-(space*2)
    ma_x, ma_y, ma_h, ma_w = tb_x, tb_y+tb_h, window_height*0.2, window_width*.2
    a_x, a_y, a_h, a_w = ma_x, ma_y+ma_h+space, window_height*0.25, ma_w
    p_x, p_y, p_h, p_w = ma_x, a_y+a_h+space, window_height*0.44, (window_width*.5)-(space*2)
    o_x, o_y, o_h, o_w = ma_x+p_w+space, p_y, p_h, p_w
    b_x, b_y, b_h, b_w = ma_x+ma_w+space, ma_y, window_height*0.3, window_width-(3*space)-ma_w
    e_x, e_y, e_h, e_w = b_x, ma_y+b_h, window_height*0.17, b_w
    act_x, act_y, act_h, act_w = e_x, e_y+e_h-space, e_h, e_w  

# TOOL BAR FRAME
    frame_tb = LabelFrame(w1, text ='CONTROL PANEL')
    frame_tb.place(x=tb_x, y=tb_y, height=tb_h, width=tb_w)
# MASTER ACCOUNT FRAME -----------------------------------------------------
    frame_ma = LabelFrame(w1, text="MASTER ACCOUNT")
    frame_ma.place(x=ma_x,y=ma_y, height=ma_h, width=ma_w) # set the height and width
    button_ma = Button(frame_tb, text="MASTER ACCOUNTS", command = lambda: ma_detail_window(),height=button_height, width=button_width, bg=button_color1, fg=button_text_color1)
    button_ma.grid(column=0,row=0)
    scroll_ma = Scrollbar(frame_ma) # add scroll bar
    scroll_ma.pack(side=RIGHT, fill=Y)
    tree_ma = ttk.Treeview(frame_ma, yscrollcommand=scroll_ma.set, selectmode="extended")
    tree_ma.pack()
    scroll_ma.config(command=tree_ma.yview)
# ACCOUNTS FRAME ------------------------------------------------------------
    frame_accounts = LabelFrame(w1, text="ACCOUNTS")
    frame_accounts.place(x=a_x, y=a_y, height=a_h, width=a_w) # set the height and width of Jake is a Bad Dog
    button_accounts = Button(frame_tb, text="ACCOUNTS", command = lambda: account_detail_window(), width=button_width, height=button_height, bg=button_color1, fg=button_text_color1)
    button_accounts.grid(column=1,row=0)
    scroll_accounts = Scrollbar(frame_accounts) # add scroll bar
    scroll_accounts.pack(side=RIGHT, fill=Y)
    tree_accounts = ttk.Treeview(frame_accounts, yscrollcommand=scroll_accounts.set, selectmode="extended")
    tree_accounts.pack()
    scroll_accounts.config(command=tree_accounts.yview)
# BALANCE FRAME ------------------------------------------------------------------
    frame_balance = LabelFrame(w1, text="BALANCES")
    frame_balance.place(x=b_x, y=b_y, height=b_h, width=b_w)
    tree_balances = ttk.Treeview(frame_balance, height=2, selectmode="extended")
    tree_balances.grid(row=0, column =0)
    tree_totals = ttk.Treeview(frame_balance, height=2,selectmode="extended")
    tree_totals.grid(row=1, column=0)
# POSITIONS FRAME
    frame_positions = LabelFrame(w1, text="POSITIONS")
    frame_positions.place(x=p_x, y=p_y, height=p_h, width=p_w)
    button_positions = Button(frame_tb, text="POSITIONS", command = lambda: position_detail_window(), width=button_width, height=button_height, bg=button_color1, fg=button_text_color1)
    button_positions.grid(column=2,row=0)
    scroll_postions_y = Scrollbar(frame_positions) # add scroll bar
    scroll_postions_y.pack(side=RIGHT, fill=Y)
    scroll_postions_x = Scrollbar(frame_positions, orient='horizontal')
    scroll_postions_x.pack(side=BOTTOM, fill=X)
    #print('p_h = ',p_h)
    tree_positions = ttk.Treeview(frame_positions, height=500, yscrollcommand=scroll_postions_y.set, selectmode="extended")
    tree_positions.pack(fill='x')
    scroll_postions_y.config(command=tree_positions.yview)
    scroll_postions_x.config(command=tree_positions.xview)
# ORDERS FRAME
    frame_orders = LabelFrame(w1, text="ORDERS")
    frame_orders.place(x=o_x, y=o_y, height=o_h, width=o_w)
    button_orders = Button(frame_tb, text="ORDERS", command = lambda: order_detail_window(), width=button_width, height=button_height,bg=button_color1, fg=button_text_color1)
    button_orders.grid(column=3,row=0)
    scroll_orders_y = Scrollbar(frame_orders) # add scroll bar
    scroll_orders_y.pack(side=RIGHT, fill=Y)
    scroll_orders_x = Scrollbar(frame_orders, orient='horizontal')
    scroll_orders_x.pack(side=BOTTOM, fill=X)
    tree_orders = ttk.Treeview(frame_orders, height= 500, yscrollcommand=scroll_orders_y.set, selectmode="extended")
    tree_orders.pack(fill='both')
    scroll_orders_y.config(command=tree_orders.yview)
    scroll_orders_x.config(command=tree_orders.xview)
# EXECUTIONS FRAME
    frame_exe = LabelFrame(w1, text="EXECUTIONS")
    frame_exe.place(x=e_x, y=e_y, height=e_h, width=e_w)
    exe_detail_button = Button(frame_tb, text="EXECUTIONS", command = lambda: order_detail_window(), width=button_width, height=button_height, bg=button_color1, fg=button_text_color1)
    exe_detail_button.grid(column=4,row=0)
    exe_scroll = Scrollbar(frame_exe) # add scroll bar
    exe_scroll.pack(side=RIGHT, fill=Y)
    exe_tree = ttk.Treeview(frame_exe, yscrollcommand=exe_scroll.set, selectmode="extended")
    exe_tree.pack()
    exe_scroll.config(command=exe_tree.yview)
# ACCTIVITIES FRAME
    frame_act = LabelFrame(w1, text="ACTIVITIES")
    frame_act.place(x=act_x, y=act_y, height=act_h, width=act_w)
    act_detail_button = Button(frame_tb, text="ACTIVITIES", command = lambda: position_detail_window(), width=button_width, height=button_height, bg=button_color1, fg=button_text_color1)
    act_detail_button.grid(column=5,row=0)
    act_scroll = Scrollbar(frame_act) # add scroll bar
    act_scroll.pack(side=RIGHT, fill=Y)
    act_tree = ttk.Treeview(frame_act, yscrollcommand=act_scroll.set, selectmode="extended")
    act_tree.pack()
    act_scroll.config(command=exe_tree.yview)
# CLOSE BUTTON
    close_button = Button(frame_tb, text='CLOSE', command=w1.destroy)
    close_button.grid(column=10,row=0)
    
    def resize_app(e):
        global window_height, window_width
        global ma_x, ma_y, ma_h, ma_w
        global a_x, a_y, a_h, a_w
        global p_x, p_y, p_h, p_w 
        global o_x, o_y, o_h, o_w 
        global b_x, b_y, b_h, b_w 
        global e_x, e_y, e_h, e_w 
        global act_x, act_y, act_h, act_w 

        w1.update()
        window_height = w1.winfo_height()
        window_width = w1.winfo_width()
        print('height : ',window_height)
        print('width :',window_width)
        space=5
        ma_x, ma_y, ma_h, ma_w = space, space, window_height*0.2, window_width*.2
        a_x, a_y, a_h, a_w = ma_x, ma_y+ma_h+space, window_height*0.25, ma_w
        p_x, p_y, p_h, p_w = ma_x, a_y+a_h+space, window_height*0.5, window_width*.5
        o_x, o_y, o_h, o_w = ma_x+p_w+space, p_y, window_height*0.5, window_width*.5
        b_x, b_y, b_h, b_w = ma_x+ma_w+space, ma_y, window_height*0.1, ((p_w*2)+(ma_x*2))-ma_w
        e_x, e_y, e_h, e_w = b_x, ma_y+b_h, window_height*0.15, b_w
        act_x, act_y, act_h, act_w = e_x, e_y+e_h+space, e_h, e_w  

    #w1.bind('<Configure>',resize_app)

    #============================================================================
    # ============= MASTER ACCOUNT FRAME ========================================
    # ====================================================================

    def draw_ma():
        tree_ma.delete(*tree_positions.get_children()) # clear any previous tree
        w1.update()
        print('running draw_ma')
        # OPEN DATABASE
        conn = sqlite3.connect('riskmit.db') 
        c = conn.cursor()
        c.execute("SELECT account_id, account_name FROM master_accounts")
        records = c.fetchall() # geta all rows in table
        headers = [i[0] for i in c.description] # gets all column names
        # COLUMN HEADINGS
        tree_ma['columns'] = headers
        tree_ma['show']= 'headings'
        for column in tree_ma['columns']:
            tree_ma.heading(column, text=column)
            if column =='account_name':
                tree_ma.column(column, width=100)
            elif column =='account_id':
                tree_ma.column(column, width=70)
            else:
                tree_ma.column(column, width=20)
        # PRINT ROWS
        for row in records:
            tree_ma.insert("", "end", values=row)
        # BINDING
        tree_ma.bind('<ButtonRelease-1>', master_account_change)
        conn.commit()
        c.close()
        conn.close()

    # GRAB THE MASTER ACCOUNT CHOOSEN AND UPDATE ACCOUNT LIST
    def master_account_change(e):
            global q
            global ma_name
            # CLEAR OTHER TREES
            tree_positions.delete(*tree_positions.get_children()) # clear any previous tree
            tree_accounts.delete(*tree_accounts.get_children()) # clear any previous tree  
            tree_orders.delete(*tree_orders.get_children()) # clear any previous tree
            w1.update() #refresh window
            # GET THE MA NAME CHOOSEN
            selected = tree_ma.focus() # Gab record number
            values = tree_ma.item(selected, 'values') # Grap tuple of row values
            ma_name = values[1] # Assign selected Account Number
            q = allinone_token_set(ma_name)# GET THE TOKEN SET FOR CHOOSEN MA
            print('Master Account set, q = ',q)
            draw_accounts(q) 

    def ma_detail_window():
            pass

# ===============================================================================
# ============== ACCOUNT LIST FRAME =============================================
# ==============================================================================
    def draw_accounts(q): # List accounts, get master account id
        global account_id
        accounts_data = accounts(q)
        account_df = accounts_data[0]
        account_id = accounts_data[1]
        frame_ma.configure(text = 'MASTER ACCOUNT :'+str(account_id))
        df_summary = account_df
        df_summary = df_summary.drop(['status','isPrimary','isBilling'], axis=1)
        # ------------------------ COLUMN HEADINGS ------------------------------------
        tree_accounts['columns'] = list(df_summary.columns)
        tree_accounts['show']= 'headings'
        for column in tree_accounts['columns']:
            tree_accounts.heading(column, text=column)
            tree_accounts.column(column, width=70)
        # --------------------------- PRINT ROWS -----------------------------------
        df_rows = df_summary.to_numpy().tolist() #turns dataframe into list of lists
        for row in df_rows:
            tree_accounts.insert("", "end", values=row)
        # --------------- BINDING ---------------------------------------------------
        tree_accounts.bind('<ButtonRelease-1>', account_clicked)
        # ----------  SET ACCOUNT ID IN DB MASTER ACCOUNT TABLE IF NOT SET YET -----------
        conn = sqlite3.connect(database)
        c = conn.cursor()
        c.execute("UPDATE master_accounts SET account_id=? WHERE account_name=?",(account_id, ma_name))
        conn.commit() # Commit changes
        c.close()
        conn.close() # close data base
        tree_ma.delete(*tree_ma.get_children()) # clear any previous tree
        w1.update()
        draw_ma()

    # ACCOUNT DETAIL WINDOW -------------------------------
    def account_detail_window(): 
            w2 = Toplevel(w1)
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
            df = accounts(q)
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

    # ACCOUNT HAS BEEN CLICKED - POPULATE THE FRAMES ===================
    def account_clicked(e):
            global account_number
            #------ GRAB ACCOUNT THAT WAS CLICKED -----------
            selected = tree_accounts.focus() # Gab record number
            values = tree_accounts.item(selected, 'values') # Grap tuple of row values
            account_number = values[1] # Assign selected Account Number
            # --------- CLEAR TREES -------------------------
            tree_positions.delete(*tree_positions.get_children()) # clear any previous tree
            tree_orders.delete(*tree_orders.get_children())
            tree_balances.delete(*tree_balances.get_children())
            tree_totals.delete(*tree_totals.get_children())
            exe_tree.delete(*exe_tree.get_children())
            act_tree.delete(*act_tree.get_children())
            w1.update() #refesh window
            # ----------- REPOPULATE THE OTHER TREES
            draw_positions(e) 
            draw_orders(e)
            draw_balances(e)

# =================================================================================
# ============== BALANCES FRAME ===================================================
# ==================================================================================
    def draw_balances(e):
        global account_number
        frame_balance.update()
        frame_width = frame_balance.winfo_width()
        df_balance_set = balances(q,account_number)
        df_balances = df_balance_set[0] # balances df
        df_totals = df_balance_set[1] # totals
        print('loaded df_totals in draw_balances :',df_totals)
    # BALANCE HEADINGS
        tree_balances['columns'] = list(df_balances.columns)
        tree_balances['show']= 'headings'
        for column in tree_balances['columns']:
            tree_balances.heading(column, text=column,anchor=W)
            tree_balances.column(column, width=int(frame_width/10))
    # BALANCE ROWS
        df_rows = df_balances.to_numpy().tolist() #turns dataframe into list of lists
        for row in df_rows:
            tree_balances.insert("", "end", values=row)
    # TOTALS HEADINGS
        tree_totals['columns'] = list(df_totals.columns)
        tree_totals['show']= 'headings'
        for column in tree_totals['columns']:
            #tree_totals.heading(column, text=column,anchor=W)
            tree_totals.column(column, width=int(frame_width/10))
    # TOTAL ROWS
        df_rows_totals = df_totals.to_numpy().tolist() #turns dataframe into list of lists
        for row in df_rows_totals:
            tree_totals.insert("", "end", values=row)

    # BINDING
        #tree_positions.bind('<ButtonRelease-1>', position_clicked)

# =================================================================================
# ============== POSITION FRAME ===================================================
# ==================================================================================
    def draw_positions(e):
        global account_number
        frame_positions.update()
        frame_width = frame_positions.winfo_width()
        df_positions = positions(q,account_number)
        df_positions_all = df_positions
        df_positions_all = df_positions_all.drop(['symbolId','closed_qty','pnl_day','pnl_closed','isRealTime','isUnderReorg'], axis=1)
    # COLUMN HEADINGS
        tree_positions['columns'] = list(df_positions_all.columns)
        tree_positions['show']= 'headings'
        for column in tree_positions['columns']:
            tree_positions.heading(column, text=column,anchor=W)
            tree_positions.column(column, width=int(frame_width/7))#, width=60
    # PRINT ROWS
        df_rows = df_positions_all.to_numpy().tolist() #turns dataframe into list of lists
        for row in df_rows:
            tree_positions.insert("", "end", values=row)
    # BINDING
        #tree_positions.bind('<ButtonRelease-1>', position_clicked)

    def position_detail_window():
            w3 = Toplevel(w1)
            w3.geometry('1400x600')
            w3.title('POSITIONS')
        # FRAMES
            frame_positions_all = LabelFrame(w3, text="CURRENT POSITIONS")
            frame_positions_all.place(x=5, y=5, height=500, width=1390) # set the height and width of Jake is a Bad Dog
            #frame_positions_all.pack(fill='both', expand=True)
            #data_scroll = Scrollbar(frame_positions_all) # add scroll bar
            #data_scroll.pack(side=RIGHT, fill=Y)
            '''
        # TREE
            data_tree = ttk.Treeview(frame_positions_all, height= 600)
            data_tree.pack()
            data_tree.delete(*data_tree.get_children()) # clear any previous tree
            data_scroll.config(command=data_tree.yview)
            '''
        # CLOSE BUTTON
            close_button = Button(w3, text='CLOSE', command=w3.destroy) 
            close_button.pack()
            #w3.update() #refresh window
            df_positions_all = positions(q,account_number)
            '''
        # COLUMN HEADINGSs
            data_tree['columns'] = list(df_positions_all.columns)
            data_tree['show']= 'headings'
            for column in data_tree['columns']:
                data_tree.heading(column, text=column)
                data_tree.column(column, width=70)
        # ROWS
            df_rows = df_positions_all.to_numpy().tolist() #turns dataframe into list of lists
            for row in df_rows:
                data_tree.insert("", "end", values=row)
            '''
        # PANDAS TABLE TEST

            pt = Table(frame_positions_all, dataframe=df_positions_all)
            #pt = Table(frame_positions_all, showtoolbar=True)

            pt.show()

            w3.mainloop()
# =================================================================================
# ============== ORDERS FRAME ===================================================
# ==================================================================================
    def create_orders_df(q,account_number):
        df_orders = orders(q,account_number)
        df_orders_filter1 = df_orders
        df_orders_filter1 = df_orders.drop(['id','symbolId','isAnonymous','icebergQuantity','minQuantity','source','primaryRoute','secondaryRoute','orderRoute','venueHoldingOrder','exchangeOrderId','isSignificantShareHolder','isInsider','isLimitOffsetInDollar','legs', 'strategyType','isCrossZero'], axis=1)
        df_orders_filter2 = df_orders_filter1
        df_orders_filter2 = df_orders_filter2.drop(['canceledQuantity','isAllOrNone', 'avgExecPrice', 'notes', 'userId', 'placementCommission'], axis=1)
        df_orders_filter3 = df_orders_filter2
        df_orders_filter3 = df_orders_filter2.drop(['openQuantity','filledQuantity','lastExecPrice','rejectionReason','comissionCharged','chainId', 'creationTime', 'updateTime', 'orderGroupId', 'timeInForce'], axis=1)
        df_orders_filter3 = df_orders_filter3[df_orders_filter3['state'].str.contains('Activated')]
        return(df_orders, df_orders_filter1, df_orders_filter2, df_orders_filter3)

    def draw_orders(e):
        global account_number
        frame_orders.update()
        frame_width = frame_orders.winfo_width()
        print('frame width = ',frame_width)
        df_orders = create_orders_df(q,account_number)[3]
    # COLUMN HEADINGS
        tree_orders['columns'] = list(df_orders.columns)
        tree_orders['show']= 'headings'
        for column in tree_orders['columns']:
            tree_orders.heading(column, text=column,anchor=W)
            tree_orders.column(column, width=int(frame_width/10))
    # PRINT ROWS
        df_rows = df_orders.to_numpy().tolist() #turns dataframe into list of lists
        for row in df_rows:
            tree_orders.insert("", "end", values=row)
    # BINDING
        #tree_positions.bind('<ButtonRelease-1>', position_clicked)

    def order_detail_window():
            global account_number
            w4 = Toplevel(w1)
            w4.geometry('1450x600')
            w4.title('ORDERS')
        # FRAMES
            frame_orders_all = LabelFrame(w4, text="OPEN ORDERS")
            frame_orders_all.place(x=5, y=5, height=500, width=1390) # set the height and width of data_scroll = Scrollbar(frame_positions_all) # add scroll bar
        # SCROLL
            scroll_orders_all_y = Scrollbar(frame_orders_all)
            scroll_orders_all_y.pack(side=RIGHT, fill=Y)
            # HORIZONTAL SCROOL
            scroll_orders_all_x = Scrollbar(frame_orders_all, orient='horizontal')
            scroll_orders_all_x.pack(side=BOTTOM, fill=X)
        # TREE
            '''
            tree_orders_all = ttk.Treeview(frame_orders_all,height=600,yscrollcommand=scroll_orders_all_y, selectmode='extended', xscrollcommand=scroll_orders_all_x)
            tree_orders_all.pack()
            tree_orders_all.delete(*tree_orders_all.get_children()) # clear any previous tree
            scroll_orders_all_y.config(command=tree_orders_all.yview)
            scroll_orders_all_x.config(command=tree_orders_all.xview)
            '''
        # CLOSE BUTTON
            close_button = Button(w4, text='CLOSE', command=w4.destroy) 
            close_button.pack()
            df_orders_all = create_orders_df(q,account_number)[2]
            '''
        # COLUMN HEADINGSs
            tree_orders_all['columns'] = list(df_orders.columns)
            tree_orders_all['show']= 'headings'
            for column in tree_orders_all['columns']:
                tree_orders_all.heading(column, text=column, anchor=W)
                tree_orders_all.column(column, width=70, anchor=W)
        # ROWS 
            df_rows = df_orders.to_numpy().tolist() #turns dataframe into list of lists
            for row in df_rows:
                tree_orders_all.insert("", "end", values=row)
            '''
        # PANDASTABLE
            pt = Table(frame_orders_all, dataframe=df_orders_all)
    draw_ma()
   
    w1.mainloop()

# ================== END GUI ======================

