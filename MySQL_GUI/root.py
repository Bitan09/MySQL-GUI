import mysql.connector as sql
import pickle
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from idlelib.tooltip import Hovertip

window = Tk()

window.resizable(False,False)

passeye_bool = False

constraint_list = ["Not Null","Primary Key","Unique","No constraint"]

datatype_list = ["Char","Varchar","Int","Date"]

unallowed_keywords = [",",".","[","]","(",")","/","\\",";",":","'",'"']

conditions = ["=","<>",">","<",">=","<=","between","in","like","is null","is not null"]

def clean_treview(treeview:ttk.Treeview):
    for record in treeview.get_children():
        treeview.delete(record)

def delete_from_table(table,where_str,treeview:ttk.Treeview,button:Button):
    try:
        cur1.execute(f"DELETE FROM {table} {where_str}")
        clean_treview(treeview)
        new_frame.destroy()
        show_table(show_values_table,table)
    except:
        messagebox.showerror(title="Error",message="There was an error while executing!")
    button.config(state=DISABLED)

def where_frame(frame:Frame,treeview:ttk.Treeview,table,*button:Button):
    def show_table_required():
        global str_where
        clean_treview(treeview)
        str_exec = f"select * from {table} "
        value_list = list()
        try:
            for i in entry_list:
                value_list.append(i.get())
        except:pass
        str_where = where_statement(col.get(),operator_var.get(),relational_entry.get(),[between_entry_1.get(),between_entry_2.get()],value_list,like_entry.get())
        cur1.execute(str_exec+str_where)
        rows = cur1.fetchall()
        for i in range(len(rows)):
            if i%2 == 0:
                treeview.insert(parent='',index=END,iid=i,text="",values=rows[i],tags=('evenrow'))
            else:
                treeview.insert(parent='',index=END,iid=i,text="",values=rows[i],tags=('oddrow'))
        for i in button:
            i.config(state=NORMAL)

    def enter_entries(event=None):
        global entry_list
        entry_list = list()
        try:
            no_of_rows = int(no_of_rows_entry.get())
            if no_of_rows <= 0:
                messagebox.showerror(title="Enter number",message="Enter a natural number")
            else:
                no_of_rows_label.grid_forget()
                no_of_rows_entry.grid_forget()
                for i in range(no_of_rows):
                    entrybox = Entry(in_frame,font=(None,15))
                    entrybox.grid(row=i//3,column=i%3)
                    entry_list.append(entrybox)
        except ValueError: messagebox.showerror(title="Enter number",message="Enter a natural number")
    
    def grid_frames(value):
        if value in conditions[0:6]:
            for frames in framelist:
                if frames == framelist[0]:
                    frames.grid(row=0,column=3)
                else:
                    frames.grid_forget()
        elif value == conditions[6]:
            for frames in framelist:
                if frames == framelist[1]:
                    frames.grid(row=0,column=3)
                else:
                    frames.grid_forget()
        elif value == conditions[7]:
            for frames in framelist:
                if frames == framelist[2]:
                    frames.grid(row=0,column=3)
                else:
                    frames.grid_forget()
            try:
                for i in entry_list:
                    i.grid_forget()
                no_of_rows_label.grid(row=0,column=0)
                no_of_rows_entry.grid(row=0,column=1)
            except:pass
        elif value == conditions[8]:
            for frames in framelist:
                if frames == framelist[3]:
                    frames.grid(row=0,column=3)
                else:
                    frames.grid_forget()
        else:
            for frames in framelist:
                frames.grid_forget()

    relational_frame = Frame(frame)
    relational_frame.grid(row=0,column=3)
    relational_entry = Entry(relational_frame,font=(None,15))
    relational_entry.grid(row=0,column=0)
    between_frame = Frame(frame)
    between_entry_1 = Entry(between_frame,font=(None,15))
    and_label = Label(between_frame,text="and",font=(None,15))
    between_entry_2 = Entry(between_frame,font=(None,15))
    between_entry_1.grid(row=0,column=0)
    and_label.grid(row=0,column=1)
    between_entry_2.grid(row=0,column=2)
    in_frame = Frame(frame)
    no_of_rows_label = Label(in_frame,text="Enter no.of args (Press enter after entering):")
    no_of_rows_entry = Entry(in_frame,font=(None,15),width=3)
    no_of_rows_entry.bind('<Return>',enter_entries)
    no_of_rows_label.grid(row=0,column=0)
    no_of_rows_entry.grid(row=0,column=1)
    like_frame = Frame(frame)
    like_entry = Entry(like_frame,font=(None,15))
    like_entry.grid(row=0,column=0)
    framelist = [relational_frame,between_frame,in_frame,like_frame]

    text_label =Label(frame,text="Delete where")
    text_label.grid(row=0,column=0)
    col = StringVar()
    col.set(columns[0])
    col_name = OptionMenu(frame,col,*columns)
    col_name.grid(row=0,column=1)
    operator_var = StringVar()
    operator_var.set(conditions[0])
    condition_menu = OptionMenu(frame,operator_var,*conditions,command=grid_frames)
    condition_menu.grid(row=0,column=2)
    check_values = Button(frame,text='Check rows',bg='#444444',font=(None,15) ,fg='#00FFFF',activebackground='#444444',activeforeground='#00FFFF',command=show_table_required)
    check_values.grid(row=0,column=4)

def where_statement(columnname,condition,*mainvalue):
    str_to_exec = f"WHERE {columnname} {condition} "
    if condition in conditions[0:6]:
        str_to_exec += f'"{mainvalue[0]}"'
    elif condition == conditions[6]:
        str_to_exec += f'"{mainvalue[1][0]}" and "{mainvalue[1][1]}"'
    elif condition == conditions[7]:
        for i in range(len(mainvalue[2])):
            if mainvalue[2][i] == mainvalue[2][0]:
                str_to_exec += f'("{mainvalue[2][i]}",'
            elif mainvalue[2][i] == mainvalue[2][-1]:
                str_to_exec += f'"{mainvalue[2][i]}")'
            else:
                str_to_exec += f'"{mainvalue[2][i]}",'
    elif condition == conditions[8]:
        str_to_exec += f'"{mainvalue[3]}"'
    return str_to_exec

def show_table(frame,tablename):
    global columns
    global new_frame
    cur1.execute(f"select * from {tablename}")
    columns = cur1.column_names
    rows = cur1.fetchall()
    new_frame = Frame(frame)
    new_frame.pack(fill=Y,expand=1)
    scrollbary = ttk.Scrollbar(new_frame,orient=VERTICAL)
    scrollbarx = ttk.Scrollbar(new_frame,orient=HORIZONTAL)
    style_tree = ttk.Style()
    style_tree.theme_use('clam')
    style_tree.configure("Treeview",background="#BCBCBC",rowheight=25,fieldbackground="#BCBCBC",font=(None,15))
    style_tree.configure("Treeview.Heading",font=(None,15,"bold"))
    style_tree.map("Treeview",background=[('selected',"#01AB2C")])
    table = ttk.Treeview(new_frame,yscrollcommand=scrollbary.set,xscrollcommand=scrollbarx.set)
    table['columns'] = columns
    table.column('#0',width=0,stretch=NO)
    table.heading('#0',text='')
    for i in range(len(columns)):
        table.column(columns[i],anchor=W,width=250)
        table.heading(columns[i],text=columns[i],anchor=W)
    table.tag_configure('oddrow',background="#E6F5FE")
    table.tag_configure('evenrow',background="#49BDFF")
    for i in range(len(rows)):
        if i%2 == 0:
            table.insert(parent='',index=END,iid=i,text="",values=rows[i],tags=('evenrow'))
        else:
            table.insert(parent='',index=END,iid=i,text="",values=rows[i],tags=('oddrow'))
    scrollbary.pack(side=LEFT,fill=Y)
    scrollbarx.pack(side=TOP,fill=X)
    table.pack(side=LEFT,fill=BOTH)
    scrollbary.config(command=table.yview)
    scrollbarx.config(command=table.xview)

def insert_into_table(table,list,entries):
    str_exec = f"INSERT INTO {table}("
    for col in list[0]:
        str_exec += col
        if col != list[0][-1]:
            str_exec += ","
        else:
            str_exec += ") "
    str_exec += "VALUES("
    for i in range(len(list[1])):
        str_exec += f'"{list[1][i]}"'
        if list[1][i] != list[1][-1]:
            str_exec += ","
        else:
            str_exec += ")"
    try:
        cur1.execute(str_exec)
        for i in entries:
            i.delete(0,END)
        new_frame.destroy()
        show_table(show_values_table,table)
    except:messagebox.showerror(title="Error",message="There was an error executing\nPlease try again")

def insert_values(frame,tablename):
    global description
    cur1.execute(f"desc {tablename}")
    description = cur1.fetchall()
    def insert_submit():
        value_list = list()
        for i in range(len(col_vals)):
            value_list.append(col_vals[i].get())
        col_names = list()
        for val in range(len(value_list)):
            if value_list[val] != "":
                col_names.append(description[val][0])
        if len(col_names) != 0:
            for j in range(value_list.count('')):
                value_list.remove('')
            cols = [col_names,value_list]
            insert_into_table(tablename,cols,col_vals)
        else:
            messagebox.showerror(title="NO values",message="Enter values to proceed")
        
    col_vals = list()
    column_value = Frame(frame)
    for i in range(len(columns)):
        col_frame = Frame(column_value)
        col_label = Label(col_frame,text=f"{columns[i]}:",font=('calibri',20))
        col_label.grid(row=0,column=0)
        col_entry = Entry(col_frame,font=('calibri',15))
        col_vals.append(col_entry)
        col_entry.grid(row=0,column=1)
        Hovertip(col_entry,f"{description[i][1:4:2]}")
        col_frame.grid(row=i//2,column=i%2,sticky=W,padx=10,pady=10)
    column_value.pack(anchor=NW)
    submit_button = Button(frame,text='Submit',command=insert_submit,bg='#444444',fg='#00FFFF',activebackground='#444444',activeforeground='#00FFFF')
    submit_button.pack(anchor=SW)

def delete_values(frame,table):
    def truncate_confirm():
        if messagebox.askyesno(title="confirm deletion",message="Do you want to delete all the values"):
            cur1.execute(f"truncate {table}")
            new_frame.destroy()
            show_table(show_values_table,table)

    truncate_button = Button(frame,text='Delete all values',bg='#444444',font=(None,15) ,fg='#00FFFF',activebackground='#444444',activeforeground='#00FFFF',command=truncate_confirm)
    truncate_button.pack(pady=10)
    delete_frame = Frame(frame)
    delete_frame.pack()

    delete_table_frame = Frame(frame)
    delete_table_frame.pack()

    scrollbary = ttk.Scrollbar(delete_table_frame,orient=VERTICAL)
    scrollbarx = ttk.Scrollbar(delete_table_frame,orient=HORIZONTAL)
    delete_treeview = ttk.Treeview(delete_table_frame,yscrollcommand=scrollbary.set,xscrollcommand=scrollbarx.set)
    delete_treeview['columns'] = columns
    delete_treeview.column('#0',width=0,stretch=NO)
    delete_treeview.heading('#0',text='')
    for i in range(len(columns)):
        delete_treeview.column(columns[i],anchor=W,width=250)
        delete_treeview.heading(columns[i],text=columns[i],anchor=W)
    delete_treeview.tag_configure('oddrow',background="#E6F5FE")
    delete_treeview.tag_configure('evenrow',background="#49BDFF")
    scrollbary.pack(side=LEFT,fill=Y)
    scrollbarx.pack(side=TOP,fill=X)
    delete_treeview.pack(side=LEFT,fill=BOTH)
    scrollbary.config(command=delete_treeview.yview)
    scrollbarx.config(command=delete_treeview.xview)

    delete_rows = Button(frame,text='Delete rows',bg='#444444',font=(None,15) ,fg='#00FFFF',activebackground='#444444',activeforeground='#00FFFF',command=lambda:delete_from_table(table,str_where,delete_treeview,delete_rows),state=DISABLED)
    delete_rows.pack()

    where_frame(delete_frame,delete_treeview,table,delete_rows)

def modify_table_(frame,table):
    pass

def update_values(frame,table):
    pass

def table_creation(tablename,tablelist):
    command_exec = f"CREATE TABLE {tablename}("
    for column in tablelist:
        command_exec += f"{column[0]} {column[1]}"
        if column[1] != datatype_list[-1]:
            command_exec += f"({column[2]})"
        if column[3] != constraint_list[-1]:
            command_exec += " "
            command_exec += f"{column[3]}"
        if column != tablelist[-1]:
            command_exec += ", "
        else:
            command_exec += ")"
    return command_exec

def checking(val):
    if any(character.isdigit() for character in val.get()):
        messagebox.showwarning(title="Error naming",message="Names with numbers not allowed")
        return False
    elif any(char in unallowed_keywords for char in val.get()):
        messagebox.showwarning(title="Error naming",message=f"Names with {unallowed_keywords} not allowed")
        return False
    elif len(val.get().split()) > 1:
        messagebox.showwarning(title="Error naming",message="Names with space not allowed")
        return False
    else:
        return True

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
    user_toplevel.resizable(False,False)
    user_toplevel.title("Define")
    user_add_label = Label(user_toplevel,text="Name of user")
    user_add_entry = Entry(user_toplevel)
    try: user_add_entry.insert(0,username)
    except: user_add_entry.insert(0,"root")
    host_add_label = Label(user_toplevel,text="Name of host")
    host_add_entry = Entry(user_toplevel)
    try: host_add_entry.insert(0,hostname)
    except: host_add_entry.insert(0,"localhost")
    host_user_add_submit = Button(user_toplevel,text='Submit',bg='#444444',fg='#00FFFF',command=user_host_add_submit_funcn,activebackground='#444444',activeforeground='#00FFFF')
    user_add_label.grid(row=0,column=0)
    user_add_entry.grid(row=0,column=1)
    host_add_label.grid(row=1,column=0)
    host_add_entry.grid(row=1,column=1)
    host_user_add_submit.grid(row=2,column=0,columnspan=2)
    user_add_entry.focus()

try:
    userfile_objr = open("userfile.dat","rb")
    username = pickle.load(userfile_objr)
    userfile_objr.close()
    hostfile_objr = open("hostfile.dat","rb")
    hostname = pickle.load(hostfile_objr)
    hostfile_objr.close()
except:rename_host_user()

def table_dml():
    global tablename
    global dml_commands_frame
    global show_values_table
    tablename = table_list[table_int.get()][0]
    dml_commands_frame = Frame(window,bg='#000000',width=1420,height=780)
    dml_commands_frame.pack(fill=BOTH)
    back_button = Button(dml_commands_frame,image=back_image,bg='#0d0d0d',activebackground='#0d0d0d',command=table_window_back)
    back_button.pack(anchor=NW)
    dml_label = Label(dml_commands_frame,text=tablename,padx=20,pady=10,font=('Calibri',35,'bold'),bg='#000000',fg='#FFFFFF',relief=RAISED)
    dml_label.pack(anchor=N)
    style_notebook = ttk.Style()
    style_notebook.configure('TNotebook.Tab', font=('URW Gothic L','18','bold'))
    table_commands = ttk.Notebook(dml_commands_frame,height=700)
    show_values_table = Frame(table_commands,bg="#000000")
    insert_in_table = Frame(table_commands,bg="#000000")
    delete_from_table = Frame(table_commands,bg="#000000")
    modify_table = Frame(table_commands,bg="#000000")
    update_values_table = Frame(table_commands,bg="#000000")
    table_commands.add(show_values_table,text="Show table")
    table_commands.add(insert_in_table,text="Insert values")
    table_commands.add(delete_from_table,text="Delete values")
    table_commands.add(modify_table,text="Modify table")
    table_commands.add(update_values_table,text="Update values")
    table_commands.pack(fill=BOTH)
    show_table(show_values_table,tablename)
    insert_values(insert_in_table,tablename)
    delete_values(delete_from_table,tablename)
    modify_table_(modify_table,tablename)
    update_values(update_values_table,tablename)

def data_table():
    window.title("Table")
    def table_add_command():
        def fill_columns(event=None):
            def col_checking():
                for index in col_value_list:
                    for i in range(len(index)):
                        if index[i].get() == "":
                            messagebox.showwarning(title="Error",message="Enter values")
                            check_bool = False
                            break
                        if i == 0:
                            check_bool = checking(index[i])
                        if i == 1:
                            if index[i].get() == datatype_list[-1]:
                                index[i+1].delete(0,END)
                                index[i+1].insert(0,"1")
                                index[i+1].config(state=DISABLED)
                            else:
                                index[i+1].config(state=NORMAL)
                        if i ==2:
                            if (not index[i].get().isdigit()) and (int(index[i].get()) < 0):
                                messagebox.showwarning(title="Error",message="Only natural numbers are allowed in size")
                                check_bool = False
                                break
                    if not check_bool:
                        break
                if check_bool:
                    col_submit.config(state=NORMAL)
                else:
                    col_submit.config(state=DISABLED)
            def col_submission():
                global col_main_list
                col_main_list = list()
                confirm_bool = True
                for index in col_value_list:
                    col_parameters = list()
                    for i in range(len(index)):
                        if index[i].get() == "":
                            messagebox.showerror(title="Error",message="Enter values")
                            confirm_bool = False
                            break
                        if i == 0:
                            confirm_bool = checking(index[i])
                            if confirm_bool:
                                col_parameters.append(index[i].get())
                            else:
                                break
                        else:
                            col_parameters.append(index[i].get())
                        if i == 2:
                            if (not index[i].get().isdigit()) and (int(index[i].get()) < 0):
                                messagebox.showerror(title="Error",message="Only integers are allowed in size")
                                confirm_bool = False
                                break
                    if not confirm_bool:
                        break
                    col_main_list.append(col_parameters)
                if confirm_bool:
                    add_table_toplevel.destroy()
                    str_execute = table_creation(table_to_add,col_main_list)
                    cur1.execute(str_execute)
                    table_frame.destroy()
                    table_frame_update()
                else:
                    del col_main_list
            if number_entry.get().isdigit() and (int(number_entry.get()) > 0):
                no_of_columns = int(number_entry.get())
                col_value_list = list()
                number_entry.config(state=DISABLED)
                number_submit.config(state=DISABLED)
                col_check = Button(add_table_toplevel,text='Check Columns',bg='#444444',fg='#00FFFF',activebackground='#444444',activeforeground='#00FFFF',command=col_checking)
                col_submit = Button(add_table_toplevel,text='Submit Columns',bg='#444444',fg='#00FFFF',activebackground='#444444',activeforeground='#00FFFF',command=col_submission,state=DISABLED)
                col_check.grid(row=3,column=0)
                col_submit.grid(row=3,column=1)
                for index in range(0,no_of_columns):
                    col_vals = list()
                    datatype_var = StringVar(add_table_toplevel)
                    constraints_var = StringVar(add_table_toplevel)
                    datatype_var.set(datatype_list[0])
                    constraints_var.set(constraint_list[-1])
                    new_row = index//2
                    column_val = Frame(fill_cols)
                    column_lab = Label(column_val,text=f"Enter column name {index+1}")
                    column_entry = Entry(column_val)
                    column_datatype = OptionMenu(column_val,datatype_var,*datatype_list)
                    column_size = Entry(column_val,width=4)
                    column_constraint = OptionMenu(column_val,constraints_var,*constraint_list)
                    column_lab.grid(row=0,column=0)
                    column_entry.grid(row=0,column=1)
                    column_datatype.grid(row=0,column=2)
                    column_size.grid(row=0,column=3)
                    column_constraint.grid(row=0,column=4)
                    column_val.grid(row=new_row,column=((index)%2))
                    col_vals.append(column_entry)
                    col_vals.append(datatype_var)
                    col_vals.append(column_size)
                    col_vals.append(constraints_var)
                    col_value_list.append(col_vals)
            else: messagebox.showerror(title='Wrong value',message='Enter a natural number!')
        def submit_table_name(event=None):
            global table_to_add
            check_for_no_mistakes = checking(table_name_entry)
            if table_name_entry.get() == "":
                messagebox.showwarning(title="Blank value",message="Enter a name")
                check_for_no_mistakes = False
            if check_for_no_mistakes:
                table_to_add = table_name_entry.get()
                number_frame.grid(row=1,column=0)
                table_name_entry.config(state=DISABLED)
                table_name_submit.config(state=DISABLED)
        add_table_toplevel = Toplevel()
        table_name_frame = Frame(add_table_toplevel)
        table_name_label = Label(table_name_frame,text="Name of table:")
        table_name_entry = Entry(table_name_frame)
        table_name_submit = Button(table_name_frame,text='Submit',command=submit_table_name,bg='#444444',fg='#00FFFF',activebackground='#444444',activeforeground='#00FFFF')
        number_frame = Frame(add_table_toplevel)
        add_label = Label(number_frame,text="No.of rows:")
        number_entry = Entry(number_frame)
        number_submit = Button(number_frame,text='Submit',command=fill_columns,bg='#444444',fg='#00FFFF',activebackground='#444444',activeforeground='#00FFFF')
        add_label.grid(row=0,column=0)
        number_entry.grid(row=0,column=1)
        number_submit.grid(row=0,column=2)
        number_entry.bind('<Return>',fill_columns)
        table_name_submit.bind('<Return>',submit_table_name)
        table_name_frame.grid(row=0,column=0)
        table_name_label.grid(row=0,column=0)
        table_name_entry.grid(row=0,column=1)
        table_name_submit.grid(row=0,column=2)
        fill_cols = Frame(add_table_toplevel)
        fill_cols.grid(row=2,column=0)
    def table_drop_command():
        def drop_table_submit_command():
            try:
                deleted_table = drop_listbox.get(drop_listbox.curselection())
                cur1.execute(f"DROP TABLE {deleted_table}")
                drop_table_toplevel.destroy()
                table_frame.destroy()
                table_frame_update()
            except:messagebox.showerror(title="No selection",message="Select a value to be deleted")
        if len(table_list) == 0:
            messagebox.showwarning(title="No tables",message="No table inside the selected database")
        else:
            drop_table_toplevel = Toplevel()
            drop_table_selection = Frame(drop_table_toplevel,bg='#000000')
            drop_table_label = Label(drop_table_selection,text="Select table to be deleted",font=('Calibri',30),fg='#FFFFFF',bg='#000000')
            drop_table_submit = Button(drop_table_selection,text="Delete table",font=('calibri',20),command=drop_table_submit_command)
            drop_table_frame = Frame(drop_table_selection,bg='#000000')
            drop_listbox = Listbox(drop_table_frame,font=("calibri",20),bg="#101010",fg="#98F5F9")
            for index in range(0,len(table_list)):
                drop_listbox.insert(index,table_list[index][0])
            drop_table_label.pack()
            drop_listbox.pack()
            drop_table_frame.pack()
            drop_table_submit.pack(anchor=E)
            drop_table_selection.pack()    
    def select_table():
        table_selection.destroy()
        table_dml()
    def table_frame_update():
        global table_list
        global table_frame
        table_frame = Frame(show_tables,bg='#000000')
        cur1.execute("show tables")
        table_list = cur1.fetchall()
        for index in range(0,len(table_list)):
            new_row = index//5
            table_radio = Radiobutton(table_frame,variable=table_int,text=table_list[index][0],value=index,font=('Impact',20),indicatoron=0,width=20,command=select_table)
            table_radio.grid(row=(new_row),column=(index%5),sticky=W)
            Hovertip(table_radio,f'{table_list[index][0]}')
        table_frame.pack()

    global table_selection
    global table_int
    table_int =IntVar()
    table_selection = Frame(window,bg='#000000')
    table_selection.pack()
    add_and_drop = Frame(table_selection,bg='#000000')
    add_table = Button(add_and_drop,text="Add a table",font=('calibri',20),command=table_add_command)
    drop_table = Button(add_and_drop,text="Delete a table",font=('calibri',20),command=table_drop_command)
    spacer1 = Label(add_and_drop,text="",padx=100,bg='#000000')
    spacer2 = Label(add_and_drop,text="",pady=10,bg='#000000')
    back_button = Button(table_selection,image=back_image,bg='#0d0d0d',command=database_window_back,activebackground='#0d0d0d')
    back_button.grid(row=0,column=0)
    table_select_label = Label(table_selection,text="Select a table",font=('Calibri',30),fg='#FFFFFF',bg='#000000')
    table_select_label.grid(row=0,column=1)
    show_tables = Frame(table_selection,bg='#000000')
    add_table.grid(row=0,column=0)
    spacer1.grid(row=0,column=2)
    spacer2.grid(row=1,column=0,columnspan=3)
    drop_table.grid(row=0,column=3)
    add_and_drop.grid(row=1,column=0,columnspan=3)
    show_tables.grid(row=2,column=0,columnspan=3)
    table_frame_update()

def show_password():
    global passeye_bool
    passeye_bool = not passeye_bool
    if passeye_bool == True:
        pass_show.config(image=open_eye)
        pass_entry.config(show='')
    else:
        pass_show.config(image=close_eye)
        pass_entry.config(show='*')

def table_window_back():
    dml_commands_frame.destroy()
    data_table()

def database_window_back():
    table_selection.destroy()
    database_window()

def database_window():
    window.title("Database")
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
            Hovertip(database_radio,f'{databases_list[index][0]}')
    def add_new_database(event=None):
        new_database = new_database_entry.get()
        new_database_entry.delete(0,END)
        try:
            cur1.execute(f'create database {new_database}')
            database_frame.destroy()
            database_frame_update()
        except: messagebox.showerror(title='Wrong name',message='Put a better name!')
    def drop_database(event=None):
        if messagebox.askyesno(title="Confirm deletion",message="Do you want ot delete the database"):
            del_database = del_database_entry.get()
            del_database_entry.delete(0,END)
            try:
                cur1.execute(f'drop database {del_database}')
                database_frame.destroy()
                database_frame_update()
            except: messagebox.showerror(title="Database doesn't exist",message='Put an existing database!')
    
    Select_database = Label(window,text='Select prefered database',padx=20,pady=10,font=('Calibri',40),bg='#000000',fg='#FFFFFF')
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
        window.geometry('1420x780')
        window.resizable(True,True)
        pass_frame.destroy()
        database_window()
        messagebox.showinfo(title='Correct Password',message='Password entered by user is correct!\nConnection succesful!')
    except:
        messagebox.showerror(title='Parameters mismatch',message='Wrong Password or redefine username and hostname!')

close_eye = PhotoImage(file='eyeclose.png')
open_eye = PhotoImage(file='eyeopen.png')
back_image = PhotoImage(file='back.png')
window.config(background='#000000')

window.geometry('370x64')
window.title('Enter credentials')

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
try:
    con1.commit()
    con1.close()
except:pass
