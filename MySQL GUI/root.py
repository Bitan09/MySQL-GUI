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

def main_window():
    window.geometry('1280x720')
    pass_frame.destroy()

def password_submit(event=None):
    global con1
    passwd_value = pass_entry.get()
    pass_entry.delete(0,END)
    try:
        con1 = sql.connect(host='localhost',user='root',passwd=passwd_value)
        main_window()
        messagebox.showinfo(title='Correct Password',message='Password entered by user is correct!\nSuccesful connection established!')
        window.unbind('<Return>')
    except:
        messagebox.showerror(title='Password mismatch',message='Password entered by user is wrong!')

close_eye = PhotoImage(file='eyeclose.png')
open_eye = PhotoImage(file='eyeopen.png')
window.config(background='#000000')

window.geometry('380x50')
pass_frame =Frame(window,pady=10,bg='#000000')
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
