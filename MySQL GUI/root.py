import mysql.connector as sql
from tkinter import *
from tkinter import messagebox

window = Tk()

passeye_bool = False

def show_password():
    global passeye_bool
    passeye_bool = not passeye_bool
    if passeye_bool == True:
        pass_show.config(image=open_eye)
        pass_entry.config(show='')
    else:
        pass_show.config(image=close_eye)
        pass_entry.config(show='*')

def database_window():
    database_int = IntVar()
    database_frame = Frame(window,pady=10,bg='#000000')
    database_frame.pack()
    def database_submit():
        print(database_int.get())
    Label(database_frame,text='Select prefered database',padx=20,pady=10,font=('Calibri',40)).grid(row=0,column=0,columnspan=4)
    for i in range(0,len(databases_list)):
        c = i//4
        database_radio = Radiobutton(database_frame,variable=database_int,text=databases_list[i][0],value=i,font=('Impact',20),indicatoron=0,width=20,command=database_submit)
        database_radio.grid(row=(c+1),column=(i%4))

def password_submit(event=None):
    global con1
    global cur1
    global databases_list
    passwd_value = pass_entry.get()
    pass_entry.delete(0,END)
    try:
        con1 = sql.connect(host='localhost',user='root',passwd=passwd_value)
        cur1 = con1.cursor()
        cur1.execute('show databases')
        databases_list = cur1.fetchall()
        window.geometry('1280x720')
        pass_frame.destroy()
        database_window()
        messagebox.showinfo(title='Correct Password',message='Password entered by user is correct!\nConnection succesful!')
    except:
        messagebox.showerror(title='Password mismatch',message='Password entered by user is wrong!')

close_eye = PhotoImage(file='eyeclose.png')
open_eye = PhotoImage(file='eyeopen.png')
window.config(background='#000000')

window.geometry('380x50')

pass_frame = Frame(window,pady=10,bg='#000000')
pass_lab = Label(pass_frame,text='Enter Password',bg='#000000',fg='#F7F308')
pass_entry = Entry(pass_frame,width=20,bg='#FFFFFF',fg='#000000',font=('consolas',14),show='*')
pass_show = Button(pass_frame,image=close_eye,bg='#000000',command=show_password,activebackground='#000000')
pass_submit = Button(pass_frame,text='Submit',command=password_submit,bg='#000000',fg='#00ff00',activebackground='#000000',activeforeground='#00ff00')

pass_entry.focus()
window.bind('<Return>',password_submit)

pass_lab.grid(row=0,column=0)
pass_entry.grid(row=0,column=1)
pass_show.grid(row=0,column=2)
pass_submit.grid(row=0,column=3)
pass_frame.pack()
window.mainloop()
