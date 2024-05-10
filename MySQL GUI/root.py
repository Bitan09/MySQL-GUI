import mysql.connector as sql
import pickle
from tkinter import *
from tkinter import messagebox
window = Tk()

def rename_host_user():
    def user_host_add_submit_funcn():
        global username
        global hostname
        user = user_add_entry.get()
        user_add_entry.delete(0,END)
        userfile_objw = open("userfile.dat","wb")
        pickle.dump(user,userfile_objw)
        userfile_objw.close()
        host = host_add_entry.get()
        host_add_entry.delete(0,END)
        hostfile_objw = open("hostfile.dat","wb")
        pickle.dump(host,hostfile_objw)
        hostfile_objw.close()

        userfile_objr = open("userfile.dat","rb")
        username = pickle.load(userfile_objr)
        userfile_objr.close()
        hostfile_objr = open("hostfile.dat","rb")
        hostname = pickle.load(hostfile_objr)
        hostfile_objr.close()
        user_toplevel.destroy()

    user_toplevel = Toplevel()
    user_toplevel.title("Define host")
    user_add_label = Label(user_toplevel,text="Name of user")
    user_add_entry = Entry(user_toplevel)
    host_add_label = Label(user_toplevel,text="Name of user")
    host_add_entry = Entry(user_toplevel)
    host_user_add_submit = Button(user_toplevel,text='Submit',bg='#444444',fg='#00FFFF',command=user_host_add_submit_funcn,activebackground='#444444',activeforeground='#00FFFF')
    user_add_label.grid(row=0,column=0)
    user_add_entry.grid(row=0,column=1)
    host_add_label.grid(row=1,column=0)
    host_add_entry.grid(row=1,column=1)
    host_user_add_submit.grid(row=2,column=0,columnspan=2)

try:
    userfile_objr = open("userfile.dat","rb")
    username = pickle.load(userfile_objr)
    userfile_objr.close()
    hostfile_objr = open("hostfile.dat","rb")
    hostname = pickle.load(hostfile_objr)
    hostfile_objr.close()
except:
    rename_host_user()

window.resizable(False,False)

passeye_bool = False

def data_table():
    pass

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
    global cur1
    cur1 = con1.cursor()
    def database_frame_update():
        global databases_list
        global database_frame
        cur1.execute('show databases')
        def database_submit():
            global dbname
            dbname = databases_list[database_int.get()][0]
            cur1.execute(f'use {dbname}')
            Select_database.destroy()
            database_frame.destroy()
            new_database_frame.destroy()
            del_database_frame.destroy()
            data_table()
        databases_list = cur1.fetchall()
        database_int = IntVar()
        database_frame = Frame(window,pady=10,bg='#000000')
        database_frame.grid(row=1,column=0,columnspan=2)
        for index in range(0,len(databases_list)):
            new_row = index//5
            database_radio = Radiobutton(database_frame,variable=database_int,text=databases_list[index][0],value=index,font=('Impact',20),indicatoron=0,width=20,command=database_submit)
            database_radio.grid(row=(new_row),column=(index%5))
    def add_new_database(event=None):
        new_database = new_database_entry.get()
        new_database_entry.delete(0,END)
        try:
            cur1.execute(f'create database {new_database}')
            database_frame.destroy()
            database_frame_update()
        except: messagebox.showerror(title='Wrong name',message='Put a better name!')
    def drop_database(event=None):
        del_database = del_database_entry.get()
        del_database_entry.delete(0,END)
        try:
            cur1.execute(f'drop database {del_database}')
            database_frame.destroy()
            database_frame_update()
        except: messagebox.showerror(title="Database doesn't exist",message='Put an existing database!')
    
    Select_database = Label(window,text='Select prefered database',padx=20,pady=10,font=('Calibri',40))
    Select_database.grid(row=0,column=0,columnspan=2)
    database_frame_update()

    new_database_frame = Frame(window,bg='#000000')
    new_database_label = Label(new_database_frame,text='Add new database',fg='#FFFFFF',bg='#000000',font=30)
    new_database_entry = Entry(new_database_frame,width=20)
    new_database_submit = Button(new_database_frame,text='Submit',bg='#444444',fg='#00FFFF',activebackground='#444444',activeforeground='#00FFFF',command=add_new_database)
    new_database_label.grid(row=0,column=0)
    new_database_entry.grid(row=0,column=1)
    new_database_submit.grid(row=0,column=2)
    new_database_frame.grid(row=2,column=0,)

    del_database_frame = Frame(window,bg='#000000')
    del_database_label = Label(del_database_frame,text='Delete a database',fg='#FFFFFF',bg='#000000',font=30)
    del_database_entry = Entry(del_database_frame,width=20)
    del_database_submit = Button(del_database_frame,text='Submit',bg='#444444',fg='#00FFFF',activebackground='#444444',activeforeground='#00FFFF',command=drop_database)
    del_database_label.grid(row=0,column=0)
    del_database_entry.grid(row=0,column=1)
    del_database_submit.grid(row=0,column=2)
    del_database_frame.grid(row=2,column=1,)

    new_database_entry.bind('<Return>',add_new_database)
    del_database_entry.bind('<Return>',drop_database)

def password_submit(event=None):
    global con1
    passwd_value = pass_entry.get()
    pass_entry.delete(0,END)
    try:
        con1 = sql.connect(host=hostname,user=username,passwd=passwd_value)
        window.geometry('1360x765')
        pass_frame.destroy()
        database_window()
        messagebox.showinfo(title='Correct Password',message='Password entered by user is correct!\nConnection succesful!')
    except:
        messagebox.showerror(title='Password mismatch',message='Password entered by user is wrong!')

close_eye = PhotoImage(file='eyeclose.png')
open_eye = PhotoImage(file='eyeopen.png')
window.config(background='#000000')

window.geometry('370x64')

pass_frame = Frame(window,pady=10,bg='#000000')
pass_label = Label(pass_frame,text='Enter Password',bg='#000000',fg='#F7F308')
pass_entry = Entry(pass_frame,width=20,font=('consolas',14),show='*')
pass_show = Button(pass_frame,image=close_eye,bg='#0d0d0d',command=show_password,activebackground='#0d0d0d')
pass_submit = Button(pass_frame,text='Submit',command=password_submit,bg='#444444',fg='#00FFFF',activebackground='#444444',activeforeground='#00FFFF')
rename = Button(pass_frame,text='Redefine user and host',command=rename_host_user,bg='#444444',fg='#FFFF00',activebackground='#444444',activeforeground='#FFFF00')
pass_entry.focus()
pass_entry.bind('<Return>',password_submit)

pass_label.grid(row=0,column=0)
pass_entry.grid(row=0,column=1)
pass_show.grid(row=0,column=2)
pass_submit.grid(row=0,column=3)
rename.grid(row=1,column=0,columnspan=4)
pass_frame.pack(fill=BOTH)
window.mainloop()
