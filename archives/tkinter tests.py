import questrade_modules
from questrade_modules import *
from tkinter import *
from tkinter import messagebox # even though everything was imported messagebox still needs to be implicidly imported
from tkinter import ttk, filedialog
from PIL import ImageTk, Image # install pillow for images
from openpyxl.workbook import Workbook
from openpyxl import load_workbook
from openpyxl.styles import Font, Border, Side
from openpyxl.chart import PieChart, Reference, BarChart, LineChart

excel_filename = 'riskmit_questrade.xlsx'
excel_file_full_path = 'D:\Dropbox\- INVESTINU\- QUESTRADE_API EXPORTS\riskmit_questrade.xlsx'

# =========================== GUI =============================
root = Tk()
root.title("InvestInU Reporting")
root.geometry("500x600")
root.iconbitmap('favicon.ico')

root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=3)

# =============== SELECT MASTER ACCOUNT =======================s
def master_account_set():
	global master_account
	master_account = master_account_combo.get()
	master_account_label.config(text=master_account)
	print("Account Selected:",master_account)

if not ('master_account' in globals()):
	master_account ='corporate1'

options = ["corporate1", "corporate2", "personal"]

master_account_combo = ttk.Combobox(root, value=options)
master_account_combo.current(0)
master_account_combo.grid(row=0, column=1, sticky="W")

change_account_button = Button(root, text="CHANGE ACCOUNT", command=master_account_set)
change_account_button.grid(row=0, column=0, sticky="W")

master_account_label = Label(root, text='Choose Account', relief = "flat")
master_account_label.grid(row=1, column=1, sticky="W")

# ======== EXPORT FOLDER SET ====================
def export_folder_set():
	export_folder = filedialog.askdirectory(initialdir='/Dropbox')
	print('export_folder = ',export_folder)
	exportfolder_label.config(text = export_folder)

if not ('export_folder' in globals()):
	export_folder ='D:\Dropbox\- INVESTINU\- QUESTRADE_API EXPORTS'

exportfolder_button = Button(root, text="EXPORT FOLDER", command=export_folder_set)
exportfolder_button.grid(row=2, column=0, sticky="W", pady=20)
exportfolder_label = Label(root, text=export_folder, relief = 'flat')
exportfolder_label.grid(row=2, column=1, sticky="W")#can pad with pady or padx

#============== SELECT EXCEL FILE ================
def excel_filename_set():
	excel_filename = filedialog.askopenfilename(initialdir='/Dropbox', title="Select Excel Workbook", filetypes=(("xlsx Fiel", ".xlsx"),("All Files","*.*")))
	print(excel_filename)
	excel_filename_label.config(text = excel_filename)

excel_filename_button = Button(root, text="EXCEL WORKBOOK", command=excel_filename_set)
excel_filename_button.grid(row=3, column=0, sticky="W", pady=20)
excel_filename_label = Label(root, text=export_folder, relief = 'flat')
excel_filename_label.grid(row=3, column=1, sticky="W")#can pad with pady or padx

#============== CREATE NEW EXCEL FILE =================
def create_excel_wb():
	wb=Workbook()
	ws=wb.active
	excel_filename=create_excel_input.get()
	excel_filename += ".xlsx"
	print("excel_filname = ",excel_filename)
	#print('excel full path : ',excel_file_full_path)
	excel_file_full_path = export_folder+excel_filename
	print('after path creation: ',excel_file_full_path)
	wb.save(excel_file_full_path)
	#wb.save(excel_filename)
	messagebox.showinfo('CONFIRMATION', "A New Excel WB : "+excel_file_full_path)
	# showinfo, showwarning, showerror, askquestion, askokcancel,askyesno


create_excel_input = Entry(root, width = 50)
create_excel_input.grid(row=4, column=1, sticky="W")

create_excel_button = Button(root, text="CREATE NEW WB", command=create_excel_wb)
create_excel_button.grid(row=4, column=0, sticky="W")
create_excel_label = Label(root, text=excel_filename, relief = 'flat')
create_excel_label.grid(row=5, column=1, sticky="W",pady=(0,20))#can pad with pady or padx

# ================ ACCESS TOKEN SET ==================================================
def access_token_set():
	access_token = access_token_input.get()
	print('access_token = ',access_token)
	access_token_label.config(text = "CURRENT TOKEN : "+access_token)
	return

if not ('access_token' in globals()):
	access_token ='nil'
	print('access_token assigned nill :',access_token)
else:
	print('access token exists : ', access_token)

access_token_input = Entry(root, width = 50)
access_token_input.grid(row=7, column=1, sticky="W")

access_token_button = Button(root, text='ACCESS TOKEN', command=access_token_set)
access_token_button.grid(row=7, column=0, sticky="W")

access_token_label = Label(root, text='Enter Access Token', relief = "flat")
access_token_label.grid(row=8, column=1, sticky="W")

# =============== PRINT VARIABLES FOR TESTING ===========
def print_vars():
	print('----------------------------')
	print('master_account : ',master_account)
	print('export_folder :',export_folder)
	print('excel_filename :',excel_filename)
	print('excel_file_full_path :',excel_file_full_path)
	print('access_token :',access_token)
	print('-----------------------------')
	return

print_vars_button = Button(root, text='PRINT VARIABLES', command=print_vars)
print_vars_button.grid(row=15, column=0, sticky="W")



#=========================  POP UP BOX ==================
#def popup():
#	messagebox.askokcancel('Popup Title', "Look at my message!")
	# showinfo, showwarning, showerror, askquestion, askokcancel,askyesno

#pop_button=Button(root, text="Click to pop up", command=popup)
#pop_button.grid(row=10, column=0,pady=20)

#======================= COMBO BOX =====================

#options = [
#	"corporate1",
#	"corporate2",
#	"personal",
#]

#my_combo = ttk.Combobox(root, value=options)
#my_combo.current(0)
#my_combo.grid(row=11, column=0)


# new window button
#new_window_button = Button(root, text='NEW WINDOW', command=open_new_window)
#new_window_button.grid(row=15, column=0, sticky="W")

#=========== MENU ===============
#my_menu = Menu(root)
#root.config(menu=my_menu)
#	#---- FILE MENU
#file_menu = Menu(my_menu)
#my_menu.add_cascade(label="File", menu=file_menu)
#file_menu.add_command(label="New", command=fake_command)
#file_menu.add_separator()
#file_menu.add_command(label="Exit", command=root.quit)

	# ----- EDIT MENU
#edit_menu = Menu(my_menu)
#my_menu.add_cascade(label="Edit", menu=edit_menu)
#edit_menu.add_command(label="New", command=fake_command)
#edit_menu.add_separator()
#edit_menu.add_command(label="Exit", command=root.quit)




#ACCOUNT BUTTONS
#corporate1_button = Button(root, text="Corporate 1", command=lambda: master_account_selected("corporate1"))
#corporate1_button.grid(row=0, column=0, sticky='W')
#corporate2_button = Button(root, text="Corporate 2", command=lambda: master_account_selected("corporate2"))
#corporate2_button.grid(row=1, column=0, sticky='W')
#personal_button = Button(root, text="Personal", command=lambda: master_account_selected("personal"))
#personal_button.grid(row=2, column=0, sticky='W')
#current_account_label = Label(root, text=master_account, relief = 'flat')
#current_account_label.grid(row=1, column=2)#can pad with pady or padx

# ========== EXPERIMENTAL AREA ==========
#current_status = StringVar()
#current_status.set("Wating")

#show_button = Button(root, text="Show", command=show)
#hide_button = Button(root, text="Hide", command=hide)
#show_button.grid(row=5, column = 0)
#hide_button.grid(row=5, column = 1)

#my_frame = Frame(root, width=200, height= 200, bd=1, bg='blue', relief="flat")
#my_frame.grid(row=6, column=0)

#frame_label = Label(my_frame, text="hello world", font=('Helvetical', 20))
#frame_label.pack()



#my_status = Label(root, textvariable=current_status, bd=2, relief="sunken", width=100, anchor=E)
#my_status.grid(row=15, column=0)

# ======== RADIO BUTTON EXAMPLE
#r_master_account_button_1 = Radiobutton(root, text="Corporate 1", variable=master_account_selection, value='corporate1', anchor=E).grid(row=0, column=0, sticky="W")
#r_master_account_button_2 = Radiobutton(root, text="Corporate 2", variable=master_account_selection, value='corporate2', anchor=E).grid(row=1, column=0, sticky="W")
#r_master_account_button_3 = Radiobutton(root, text="Personal", variable=master_account_selection, value='personal', anchor=E).grid(row=2, column=0, sticky="W")

#master_account_label = Label(root, text=master_account, relief = "flat", font=('Arial', 16))
#master_account_label.grid(row=0, column=1, sticky="W")

#def open_new_window():
#	new_window = Toplevel()
#	new_window.title("Second Window")
#	new_window.geometry("500x500")

#	destroy_button=Button(new_window, text="Quit", command=new_window.destroy).pack()
#	hide_button=Button(new_window, text="Hide Main Window", command=root.iconify).pack()# minimizes
#	show_button=Button(new_window, text="Show Main Window", command=root.deiconify).pack()

#	destroy_main_button=Button(new_window, text="Destroy Main Window", command=root.destroy).pack()# minimizes
	#show_button=Button(new_window, text="Show Main Window", command=root.deiconify).pack()





#def fake_command():
#	pass

#def hide():
#	my_frame.grid_forget()
#	current_status.set('it is now hiden!')
#	return

#def show():
#	my_frame.grid(row=6, column=0)
#	current_status.set('is is now shown!')
#	return























root.mainloop()
# ================== END GUI ==================
