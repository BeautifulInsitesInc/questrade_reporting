from tkinter import *
from tkinter import ttk, filedialog, simpledialog
import sqlite3
import pandas as pd
from IPython.display import display
from openpyxl.workbook import Workbook
from openpyxl import load_workbook
# Imports for backup:
import os 
from datetime import datetime
import time
#ExcelApp = win32com.client.GetActiveObject("Excel.Application") #getting the active instance of Excell
# SQLALCHEMY
#import sqlalchemy as db
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, MetaData, Table, select
from sqlalchemy.orm import sessionmaker
#from pdb import set_trace; set_trace() # see what is happening hen it runs
from sqlalchemy.ext.declarative import declarative_base
from rm_tables import *

# ==== OPEN DATABASE CONNECTION ======
engine = create_engine('sqlite:///D:\\Dropbox\\code\\riskmit_questrade\\riskmit.db', echo=True)
Session = sessionmaker(bind=engine)
metadata = MetaData(engine)
Base = declarative_base()

#========================================================================================|
#============= DATABASE MANAGEMENT WINDOW ===============================================|
#========================================================================================|
def manage_database():
	session = Session()
	Base.metadata.create_all(engine)
	session.commit()
	backup_folder ='D:/Dropbox/Test folder/backups'
	datetime = time.strftime('%Y%m%d-%H%M%S')
	todays_backup_path = backup_folder
	filename = datetime+'rismit_backup.xlsx'
	full_file_path = backup_folder + '/' + filename

# ===== MAIN WINDOW ================
	root_d = Tk()
	#root_d.state('zoomed')
	root_d.geometry('1000x600')
	root_d.title('DATABASE MANAGMENT')

# FRAME DIMENTIONS
	root_d.update()
	window_height = root_d.winfo_height()
	window_width = root_d.winfo_width()
	label_width = 30
	button_width = 15
	button_height = 1
	button_color1 = 'light grey'
	button_text_color1 = 'black'
	space=5
	tb_x, tb_y, tb_h, tb_w = space, space, window_height*.08, window_width-(space*2)# toolbar
	users_x, users_y, users_h, users_w = space, space*2+tb_h, window_height-space*3-tb_h, (window_width-space*4)/3
	ma_x, ma_y, ma_h, ma_w = users_x+users_w+space, users_y, users_h, users_w
	accounts_x, accounts_y, accounts_h, accounts_w = ma_x+ma_w+space,ma_y,ma_h,ma_w

# TOOL BAR FRAME
	frame_tb = LabelFrame(root_d, text ='CONTROL PANEL')
	frame_tb.place(x=tb_x, y=tb_y, height=tb_h, width=tb_w)
# USERS FRAME
	frame_users = LabelFrame(root_d, text ='USERS')
	frame_users.place(x=users_x, y=users_y, height=int(users_h*.50), width=users_w)
	frame_user_buttons = LabelFrame(root_d, text = 'USER CONTROLS')
	frame_user_buttons.place(x=users_x, y=users_y+int(users_h*.50), height=int(users_h*.50), width=users_w)
	tree_users = ttk.Treeview(frame_users)
	tree_users.pack(fill='x')
# MASTER ACCOUNT FRAME
	frame_ma = LabelFrame(root_d, text ='MASTER ACCOUNT')
	frame_ma.place(x=ma_x, y=ma_y, height=ma_h*.50, width=ma_w)
	frame_ma_buttons = LabelFrame(root_d, text = 'MA CONTROLS')
	frame_ma_buttons.place(x=ma_x, y=ma_y+int(ma_h*.50), height=int(ma_h*.50), width=ma_w)
	tree_ma = ttk.Treeview(frame_ma)
	tree_ma.pack(fill='x')
# ACCOUNTS FRAME
	frame_accounts = LabelFrame(root_d, text ='ACCOUNTS')
	frame_accounts.place(x=accounts_x, y=accounts_y, height=accounts_h, width=accounts_w)


	# ============================================================================
	# ======  BACKUP TO EXCELL ===================================================
	#=============================================================================
	def backup_database(database):
		
	# CREATE DF FROM TABLES 
		with engine.begin() as conn:
			df_ma = pd.read_sql_query("SELECT * FROM master_accounts",conn)
			df_users = pd.read_sql_query("SELECT * FROM users",conn)
			display(df_ma)
			display(df_users)
			try:
				os.mkdir(todays_backup_path)
			except:
				print('Directory already exists :',todays_backup_path)

	# WRITE TO EXCEL
		with engine.begin() as conn:
			wb= Workbook()
			wb.save(full_file_path)
			with pd.ExcelWriter(full_file_path, mode='a') as writer:
				df_ma.to_excel(writer, sheet_name='master_accounts', index=False)
				df_users.to_excel(writer, sheet_name='users', index=False)

	# ============================================================================
	# ======  RESTORE FROM  EXCELL ===================================================
	#=============================================================================
	def restore_database(database):	
		with engine.begin() as conn:
			excel_file_full_path = filedialog.askopenfilename(initialdir=backup_folder, title="Select Excel Workbook", filetypes=(("xlsx Fiel", ".xlsx"),("All Files","*.*")))
			print('Restore file : ',excel_file_full_path)
			df_master_accounts = pd.read_excel(excel_file_full_path,sheet_name = 'master_accounts')
			df_users = pd.read_excel(excel_file_full_path,sheet_name = 'users')
			df_master_accounts.to_sql(name='master_accounts',con=conn,if_exists='replace',index=False)
			df_users.to_sql(name='users',con=conn,if_exists='replace',index=False)
		query_names()
		#query_ma()

	# ============================================================================
	# ======  POPULATE DATABASE ===================================================
	#=============================================================================
	def populate_database(database):
		pass

	# TOOL BAR BUTTONS
	button_backup = Button(frame_tb, text='BACKUP', command = lambda: backup_database(database), width=button_width, height=button_height, bg=button_color1, fg=button_text_color1)
	button_backup.grid(column=0, row=0)
	button_restore = Button(frame_tb, text='RESTORE', command = lambda: restore_database(database), width=button_width, height=button_height, bg=button_color1, fg=button_text_color1)
	button_restore.grid(column=5, row=0)
	button_create = Button(frame_tb, text='CREATE', command = lambda: Base.metadata.create_all(engine), width=button_width, height=button_height, bg=button_color1, fg=button_text_color1)
	button_create.grid(column=10, row=0)
	button_populate = Button(frame_tb, text='POPULATE', command = lambda: populate_database(database), width=button_width, height=button_height, bg=button_color1, fg=button_text_color1)
	button_populate.grid(column=15, row=0)
	button_delete = Button(frame_tb, text='DELETE2', command = lambda: Base.metadata.drop_all(engine), width=button_width, height=button_height, bg=button_color1, fg=button_text_color1)
	button_delete.grid(column=20, row=0)

	# ======================================================
	# ========== USERS EDIT ================================
	# ======================================================
	def submit_name():
		with engine.begin() as conn:
			c.execute("INSERT INTO users VALUES (:user_name, :first_name, :last_name)",
				{'user_name' : entry_user_name.get(),'first_name': entry_first_name.get(),'last_name' : entry_last_name.get()})
		clear_name()
		query_names()

	def clear_name():
		entry_user_name.delete(0,END)
		entry_first_name.delete(0,END)
		entry_last_name.delete(0,END)

	def query_names():
		census = Table('users', metadata, autoload=True, autoload_with=engine)
		records = session.execute(select([census])).fetchall()
		headers = census.columns.keys()
		# CLEAR TREE
		tree_users.delete(*tree_users.get_children())
		tree_users.update()
		# PRINT COLUMN HEADINGS
		tree_users['columns'] = headers
		tree_users['show']= 'headings'
		for column in tree_users['columns']:
			tree_users.heading(column, text=column, anchor=W)
			tree_users.column(column, width=80)
		# PRINT ROWS
		for row in records:
			row = list(row) # convert tup to list
			tree_users.insert("", "end", values=row)
		tree_users.bind('<ButtonRelease-1>', user_record_clicked)

	def delete_name():
		key_to_delete = get_user_selected('e')[3]
		print("about to delete user id :", key_to_delete) 
		with engine.begin() as conn:
			c.execute("DELETE from users WHERE oid= "+ key_to_delete)
		query_names()

	def update_user():
		user_id = get_user_selected('e')[3]
		print('user_id :',user_id)
		with engine.begin() as conn:
			c.execute("""UPDATE users SET
				user_name = :user_name,
				first_name = :first_name,
				last_name = :last_name

				WHERE oid = :oid""",
				{
				'user_name': user_name.get(),
				'first_name': first_name.get(),
				'last_name': last_name.get(),
				'oid': user_id
				})
		clear_name()
		query_names()

	def get_user_selected(*args):
		selected = tree_users.focus() # Gab record number
		values = tree_users.item(selected, 'values') # Grap tuple of row values
		print('User record clicked :',values)
		return values

	def user_record_clicked(*args):
		selected_user = get_user_selected('e')
		print('Selected User :', selected_user)
		clear_name()
		entry_user_name.insert(0,selected_user[0])
		entry_first_name.insert(0,selected_user[1])
		entry_last_name.insert(0,selected_user[2])
		return selected_user

	def import_users():	
		excel_file_full_path = filedialog.askopenfilename(initialdir=backup_folder, title="Select Excel Workbook", filetypes=(("xlsx Fiel", ".xlsx"),("All Files","*.*")))
		print('Restore file : ',excel_file_full_path)
		df_users = pd.read_excel(excel_file_full_path,sheet_name = 'users')
		#with engine.begin() as conn:
		#	df_users.to_sql(users, conn, if_exists='append', index=False)
		for row in df_users:
			print(row)


		query_names()
	
	# User Input boxes
	label_user_name = Label(frame_user_buttons, text='User Name')
	label_user_name.grid(row = 0, column = 0)
	entry_user_name = Entry(frame_user_buttons, width=30)
	entry_user_name.grid(row=0, column=1, padx=0)
	label_first_name = Label(frame_user_buttons, text='First Name')
	label_first_name.grid(row = 1, column = 0)
	entry_first_name = Entry(frame_user_buttons, width=30)
	entry_first_name.grid(row=1, column=1, padx=0)
	label_last_name = Label(frame_user_buttons, text='Last Name')
	label_last_name.grid(row = 2, column = 0)
	entry_last_name = Entry(frame_user_buttons, width=30)
	entry_last_name.grid(row=2, column=1, padx=0)
	button_user_submit = Button(frame_user_buttons, text = "Add User", command=submit_name)
	button_user_submit.grid(row = 3, column=0, columnspan=2, pady=0, padx=0, ipadx=100)
	button_clear_user = Button(frame_user_buttons, text = "Clear", command=clear_name)
	button_clear_user.grid(row = 4, column=0, columnspan=2, pady=0, padx=0, ipadx=110)
	button_user_query = Button(frame_user_buttons, text = "Query Database", command=query_names)
	button_user_query.grid(row =5, column=0, columnspan=2, pady=0, padx=0, ipadx=100)
	button_user_delete = Button(frame_user_buttons, text = "Delete User", command=delete_name)
	button_user_delete.grid(row =6, column=0, columnspan=2, pady=0, padx=0,ipadx=100)
	button_update_user = Button(frame_user_buttons, text = "Update User", command=update_user)
	button_update_user.grid(row =7, column=0, columnspan=2, pady=0, padx=0, ipadx=100)
	button_import_users = Button(frame_user_buttons, text = "Import Users", command=import_users)
	button_import_users.grid(row =8, column=0, columnspan=2, pady=0, padx=0, ipadx=100)

	# ======================================================
	# ========== MASTER ACCOUNT EDIT ================================
	# ======================================================
	def submit_ma():
		with engine.begin() as conn:
			c.execute("INSERT INTO master_accounts VALUES (:account_id, :account_name)",
				{'account_id' : 666,'account_name': entry_ma_name.get()})
		clear_ma()
		query_ma()
	def clear_ma():
		#entry_user_name.delete(0,END)
		entry_ma_name.delete(0,END)
		#entry_ownerId.delete(0,END)

	def query_ma():
		census = Table('master_accounts', metadata, autoload=True, autoload_with=engine)
		records = session.execute(select([census])).fetchall()
		headers = census.columns.keys()
		# CLEAR TREE
		tree_ma.delete(*tree_users.get_children())
		tree_ma.update()
		# PRINT COLUMN HEADINGS
		tree_ma['columns'] = headers
		tree_ma['show']= 'headings'
		for column in tree_ma['columns']:
			tree_ma.heading(column, text=column, anchor=W)
			tree_ma.column(column, width=80)
		# PRINT ROWS
		for row in records:
			row = list(row) # convert tup to list
			tree_mainsert("", "end", values=row)
		tree_ma.bind('<ButtonRelease-1>', user_record_clicked)

	def delete_ma():
		key_to_delete = get_ma_selected('e')[2]
		print("about to delete ma id :", key_to_delete) 
		with engine.begin() as conn:
			c.execute("DELETE from master_accounts WHERE oid= "+ key_to_delete)
		query_ma()
	def update_ma():
		ma_id = get_ma_selected('e')[2]
		print('ma_id :',ma_id)
		with engine.begin() as conn:
			conn.execute("""UPDATE master_accounts SET
				account_id = :account_id,
				account_name = :account_name,

				WHERE oid = :oid""",
				{
				'account_id': account_detail_windowunt_id,
				'account_name': entry_ma_name.get(),
				'oid': ma_id
				})
		clear_ma()
		query_ma()
	def get_ma_selected(*args):
		selected = tree_ma.focus() # Gab record number
		values = tree_ma.item(selected, 'values') # Grap tuple of row values
		print('MA record clicked :',values)
		return values

	def ma_record_clicked(*args):
		selected_ma = get_ma_selected('e')
		print('Selected MA :', selected_ma)
		clear_name()
		entry_ma_name.insert(0,selected_ma[1])
		return selected_ma

	def import_ma():	
		excel_file_full_path = filedialog.askopenfilename(initialdir=backup_folder, title="Select Excel Workbook", filetypes=(("xlsx Fiel", ".xlsx"),("All Files","*.*")))
		print('Restore file : ',excel_file_full_path)
		df_ma = pd.read_excel(excel_file_full_path,sheet_name = 'master_account')
		with engine.begin() as conn:
			df_ma.to_sql(master_account, conn, if_exists='append', index=False)
		query_names()
	

	# MA Input boxes
	label_ma_name = Label(frame_ma_buttons, text='MA Name')
	label_ma_name.grid(row = 0, column = 0)
	entry_ma_name = Entry(frame_ma_buttons, width=30)
	entry_ma_name.grid(row=0, column=1, padx=0)
	label_ma_number = Label(frame_ma_buttons, text='MA Number')
	label_ma_number.grid(row = 1, column = 0)
	button_ma_submit = Button(frame_ma_buttons, text = "Add MA", command=submit_ma)
	button_ma_submit.grid(row = 3, column=0, columnspan=1, pady=0, padx=0, ipadx=0)
	button_clear_ma = Button(frame_ma_buttons, text = "Clear", command=clear_ma)
	button_clear_ma.grid(row = 4, column=0, columnspan=1, pady=0, padx=0, ipadx=0)
	button_ma_query = Button(frame_ma_buttons, text = "Query Database", command=query_ma)
	button_ma_query.grid(row =5, column=0, columnspan=1, pady=0, padx=0, ipadx=0)
	button_ma_delete = Button(frame_ma_buttons, text = "Delete MA", command=delete_ma)
	button_ma_delete.grid(row =6, column=0, columnspan=1, pady=0, padx=0,ipadx=0)
	button_update_ma = Button(frame_ma_buttons, text = "Update MA", command=update_ma)
	button_update_ma.grid(row =7, column=0, columnspan=1, pady=0, padx=0, ipadx=0)
	button_import_ma = Button(frame_ma_buttons, text = "Import Users", command=import_ma)
	button_import_ma.grid(row =8, column=0, columnspan=1, pady=0, padx=0, ipadx=0)


	
	frame_users.update()
	frame_ma.update()
	#query_names()
	#query_ma()

	session.close()


	root_d.mainloop()

	# === CLOSE DATABASE ====
	