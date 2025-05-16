#Password manager
from tkinter import Tk, Label, Button, Entry, Frame, END, Toplevel
from tkinter import ttk 
from db_operations import DbOperations


class LoginWindow:
    def __init__(self, root, on_success):
        self.root = root
        self.root.title("Login - Master Password")
        self.root.geometry("300x120+500+300")
        self.on_success = on_success

        Label(root, text="Enter Master Password", font=("Times New Roman", 12)).pack(pady=5)
        self.password_entry = Entry(root, show="*", width=25, font=("Times New Roman", 12))
        self.password_entry.pack(pady=5)

        Button(root, text="Login", font=("Times New Roman", 12), command=self.check_password).pack(pady=5)

    def check_password(self):
        entered_password = self.password_entry.get()
        if entered_password == "admin123":  # You can change the master password here
            self.root.destroy()             # Close login window
            self.on_success()              # Launch the actual app
        else:
            self.password_entry.delete(0, END)
            self.password_entry.insert(0, "")
            self.password_entry.config(bg="misty rose")



class root_window:
    
    def __init__(self, root, db):
        self.db= db
        self.root= root
        self.root.title("Passowrd Manager")
        self.root.geometry("924x550+300+40")

        head_title= Label(self.root, text= "Password Manager", width=42, 
        bg= "royal blue", font=("Times New Roman", 20), fg= "white" , padx=150, pady=10).grid(columnspan=4)
        
        self.crud_frame= Frame(self.root, highlightbackground="black", highlightthickness=3, padx=7, pady=10)
        self.crud_frame.grid()
        self.create_entry_labels()
        self.create_entry_boxes()
        self.create_crud_buttons()
        self.search_entry= Entry(self.crud_frame, width=30, font=('Times New Roman', 12))
        self.search_entry.grid(row=self.row_no, column=self.col_no)
        self.col_no+=1
        Button(self.crud_frame, text='Search', bg='yellow', font=('Times New Roman', 12), width=22).grid(row=self.row_no, column=self.col_no, padx=5, pady=5)

        self.create_records_tree()
        


    def create_entry_labels(self):
        self.col_no, self.row_no= 0, 0
        labels_info= ('ID', 'Website', 'Username', 'Password')
        for label_info in labels_info:
            Label(self.crud_frame, text=label_info, bg='grey', fg="white", font= ("Times New Roman", 15), padx= 5, pady=2).grid(row=self.row_no, column=self.col_no, padx= 5, pady=2)
            self.col_no +=1
   

    def create_crud_buttons(self):
        self.row_no+=1
        self.col_no= 0
        buttons_info= (('Save', 'green', self.save_record), ('Update', 'blue', self.update_record), ('Delete', 'red', self.delete_record), ('Copy Password', 'purple', self.copy_password), ('Show All Records', 'Teal', self.show_records))
        for btn_info in buttons_info:
            if btn_info[0]== 'Show All Records':
                self.row_no+=1
                self.col_no=0
            Button(self.crud_frame, text=btn_info[0], bg=btn_info[1], fg="white", font= ("Times New Roman", 15), padx= 2, pady=1, width=18, command= btn_info[2]).grid(row=self.row_no, column=self.col_no, padx= 5, pady=2)
            self.col_no +=1


    def create_entry_boxes(self):
        self.row_no+=1
        self.entry_boxes= []
        self.col_no = 0
        for i in range(4):
            show=""
            if i == 3:
                show = "*"  
            entry_box= Entry(self.crud_frame, width=21, bg= "lightgrey", font=("Times New Roman", 15), show=show)
            entry_box.grid(row= self.row_no, column= self.col_no, padx=1, pady=2)
            self.col_no+=1
            self.entry_boxes.append(entry_box)

    #CRUD Functions

    def save_record(self):
        website= self.entry_boxes[1].get()
        username= self.entry_boxes[2].get()
        password= self.entry_boxes[3].get()
        data= {'website': website, 'username': username, 'password': password}
        self.db.create_record(data)
        self.show_records()

    def update_record(self):
        ID= self.entry_boxes[0].get()
        website= self.entry_boxes[1].get()
        username= self.entry_boxes[2].get()
        password= self.entry_boxes[3].get()
        data= {'ID': ID, 'website': website, 'username': username, 'password': password}
        self.db.update_record(data)
        self.show_records()

    def delete_record(self):
        ID= self.entry_boxes[0].get()
        self.db.delete_record(ID)
        self.show_records()

    def show_records(self):
        for item in self.records_tree.get_children():
            self.records_tree.delete(item)
        records_list = self.db.show_records()
        for record in records_list:
            self.records_tree.insert('', END, values=(record[0], record[3], record[4], record[5]))

    def create_records_tree(self):
        columns= ('ID', 'Website', 'Username', 'Password')
        self.records_tree= ttk.Treeview(self.root, columns=columns, show='headings')
        self.records_tree.heading('ID', text='ID')
        self.records_tree.heading('Website', text='Website Name')
        self.records_tree.heading('Username', text='Username')
        self.records_tree.heading('Password', text='Password')
        self.records_tree['displaycolumns']= ('Website', 'Username', 'Password')
        self.records_tree.grid()
    
        def item_selected(event):
            for selected_item in self.records_tree.selection():
                item= self.records_tree.item(selected_item)
                record= item['values']
                for entry_box, item in zip(self.entry_boxes, record):
                    entry_box.delete(0, END)
                    entry_box.insert(0, item)
    
        self.records_tree.bind('<<TreeviewSelect>>', item_selected)

        self.records_tree.grid()


    #Copy to Clipboard
    def copy_password(self):
        self.root.clipboard_clear()
        self.root.clipboard_append(self.entry_boxes[3].get())
        message= "Password Copied"
        title= "Copy"
        if self.entry_boxes[3].get()=="":
            message= "Box is empty"
            title= "Error"
        self.showmessage(title, message)

    def showmessage(self, title_box:str=None, message:str=None):
        TIME_TO_WAIT= 900 #in milliseconds
        root= Toplevel(self.root)
        background='green'
        if title_box== "Error":
            background= "red"
        root.geometry('200x30+600+200')
        root.title(title_box)
        Label(root, text=message, background=background, font=("Times New Roman", 15), fg='white').pack(padx=4, pady=2)
        try:
            root.after(TIME_TO_WAIT, root.destroy)
        except Exception as e:
            print("Error occured", e)
    
    


def launch_main_app():
    root = Tk()
    db_class = DbOperations()
    db_class.create_table()
    root_class = root_window(root, db_class)
    root.mainloop()

if __name__ == "__main__":
    login_root = Tk()
    LoginWindow(login_root, on_success=launch_main_app)
    login_root.mainloop()
