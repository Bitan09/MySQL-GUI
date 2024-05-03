import mysql.connector as sql
from tkinter import *
from tkinter import messagebox

# WINDOW 1

def main_window():
    window.geometry('400x400')
    pass_frame.destroy()

def password_submit():
    global con1
    passwd_value = pass_entry.get()
    pass_entry.delete(0,END)
    try:
        con1 = sql.connect(host='localhost',user='root',passwd=passwd_value)
        main_window()
        messagebox.showinfo(title='Correct Password',message='Password entered by user is correct!\nConnection succesful!')
    except:
        messagebox.showerror(title='Password mismatch',message='Password entered by user is wrong!')


window = Tk()

show_eye = PhotoImage(file='eyeclose.png')

window.config(background='#000000')

window.geometry('380x50')
pass_frame =Frame(window,pady=10,bg='#000000')
pass_lab = Label(pass_frame,text='Enter Password',bg='#000000',fg='#F7F308')
pass_entry = Entry(pass_frame,width=20,bg='#000000',fg='#ffffff',font=('consolas',14))
pass_show = Button(pass_frame,image=show_eye,bg='#000000')
pass_submit = Button(pass_frame,text='Submit',command=password_submit,bg='#000000',fg='#00ff00',activebackground='#000000',activeforeground='#00ff00')

pass_lab.grid(row=0,column=0)
pass_entry.grid(row=0,column=1)
pass_show.grid(row=0,column=2)
pass_submit.grid(row=0,column=3)
pass_frame.pack()
window.mainloop()