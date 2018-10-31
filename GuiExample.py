from tkinter import *

root = Tk()
root.geometry('500x500')
root.title("SearchEngine")

label_0 = Label(root, text="SearchEngine",width=20,font=("bold", 20))
label_0.place(x=90,y=53)


label_1 = Label(root, text="Enter",width=20,font=("bold", 10))
label_1.place(x=80,y=130)

entry_1 = Entry(root)
entry_1.place(x=240,y=130)

label_4 = Label(root, text="Language",width=20,font=("bold", 10))
label_4.place(x=70,y=280)

list1 = ['English','Spanish','Hebrew'];
c=StringVar()
droplist=OptionMenu(root,c, *list1)
droplist.config(width=15)
c.set('Select')
droplist.place(x=240,y=280)

label_4 = Label(root, text="Stemming",width=20,font=("bold", 10))
label_4.place(x=85,y=330)
var1 = IntVar()
Checkbutton(root, text="Yes", variable=var1).place(x=235,y=330)
var2 = IntVar()
Checkbutton(root, text="No", variable=var2).place(x=290,y=330)

Button(root, text='Run',width=20,bg='blue',fg='white').place(x=180,y=380)

root.mainloop()























