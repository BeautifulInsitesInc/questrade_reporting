from tkinter import *
from tkinter import ttk, simpledialog


root=Tk()
root.title('FearandGreed.io Help App')
root.geometry('200x200')


def get_imput():
	help_string = simpledialog.askstring(title="SEARCH", prompt='TERM : ')
	print("searching for :	", help_string)
	my_help = str(help(help_string))  
	print(my_help)


better_help = str(help(Label))
print(better_help)

mybutton = Button(root, text="SEARCH FOR HELP", command=get_imput)
mybutton.pack()





root.mainloop()