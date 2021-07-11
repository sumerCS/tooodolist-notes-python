##importing all lib.
from tkinter import*
import tkinter.messagebox as tkm
import pickle
import sqlite3, os

##double checking for pre-existing databases locally on device
if os.path.exists("tasks_demo.db"):
    print("already exists_todolist")

if os.path.exists("notes_demo.db"):
    print("already exists_notes")

##creating the main frame to pop up by using tkinter module
def main():
    root = Tk()
    app = Window1(root)

##main window with buttons to different options
class Window1:
    ##function with GUI features, created by tkinter module
    def __init__(self, master):
        #creates window to be visable 
        self.master = master
        #customisation 
        self.master.title("Todolist")
        self.master.geometry("350x190")
        self.master.config(bg='grey')
        self.frame = Frame(self.master,bg='grey')
        self.frame.pack()

        #title label
        self.label_main = Label(self.frame, text ="Welcome TODOLIST App", height = 2, width = 35)
        self.label_main.grid(row=2, column=0)
		
        #button for todolist option
        self.button_todo = Button(self.frame, text = 'todo', width = 17, command = self.new_window1)
        self.button_todo.grid(row=3, column=0)

        #button for notes option
        self.button_notes = Button(self.frame, text = 'notes', width = 17, command = self.new_window2)
        self.button_notes.grid(row=4, column=0)

        #button for script todo option
        self.button_script_todo = Button(self.frame, text = 'script todo', width = 17, command = self.new_window3)
        self.button_script_todo.grid(row=5, column=0)

        #button for script notes option
        self.button_script_note = Button(self.frame, text = 'script notes', width = 17, command = self.new_window4)
        self.button_script_note.grid(row=6, column=0)

        #button for exit option
        self.button_exit = Button(self.frame, text = 'EXIT', width = 17, command = self.master.destroy)
        self.button_exit.grid(row=7, column=0)

    ##functions for opening other windows from main window (Window1)
    def new_window1(self):
        self.newWindow1 = Toplevel(self.master)
        self.app = Window2(self.newWindow1)
    def new_window2(self):
        self.newWindow2 = Toplevel(self.master)
        self.app = Window3(self.newWindow2)
    def new_window3(self):
        self.newWindow3 = Toplevel(self.master)
        self.app = Window4(self.newWindow3)
    def new_window4(self):
        self.newWindow4 = Toplevel(self.master)
        self.app = Window5(self.newWindow4)

##----------Main TODOLIST Functions----------##
##todolist window (Window2)
class Window2:
    """"this is the function which allows the user to add and delete tasks based on the content given.
    The user can load information from the .dt file and the database stores all the inputs when add.
    The scripts allow the user to see all the past history of the contents of the database.

    """

    ##creating database for todolist window, with "todo" table
    def connect(self):
        self.connection_todo = sqlite3.connect("tasks_demo.db")
        self.cursor_todo = self.connection_todo.cursor()
        self.cursor_todo.execute("CREATE TABLE IF NOT EXISTS todo(name char(30), subject char(35), date char(30), priority char(30));")

    ##function to add task based on input GUI
    def add_tasks(self):
        # get the var inputted in textfield
        self.task_name = self.entry_task_name.get()
        self.task_subject = self.entry_task_subject.get()
        self.task_date = self.entry_task_date.get()
        self.task_priority = self.priority_task_entry.get()
        ##make sure to add items to listbox if fields are filled and delete contents in texfield
        if self.task_name or self.task_subject  or self.task_date !="":
            self.output = self.task_name + "  " + self.task_subject + "  " + self.task_date + "  " + self.task_priority
            self.listbox_task_input = self.listbox_task.insert(END,self.output)
            self.entry_task_name.delete(0,END)
            self.entry_task_subject.delete(0,END)
            self.entry_task_date.delete(0,END)
        else:
            ##warning message if fields arent completed
            self.message_box  = messagebox.showwarning(title="Warning!", message="You must enter a Todo.")

        ##add the contents into different categories in SQLdatabase
        self.connect()
        self.cursor_todo.execute("""INSERT INTO todo(name, subject, date, priority) VALUES (?,?,?,?)""",
                                 (self.task_name, self.task_subject, self.task_date, self.task_priority))
        self.connection_todo.commit()
        self.connection_todo.close()

    ##function to delete a task in listbox with try and except
    def delete_tasks(self):
        try:
            ##select specific list in box
            self.selection_task = self.listbox_task.curselection()
            ##delete selected list in box
            self.listbox_task.delete(self.selection_task)
        except:
            ##show warning when list wasnt selected in box and delete was pressed
            self.message_box = messagebox.showwarning(self.frame, title="Warning!", message="You must select a Todo.")

    ##function to load previous tasks saved on .dt file with try and except        
    def load_tasks(self):
        try:
            ##pickle opens and if file doesnt exist then it creates it
            self.tasks = pickle.load(open("tasks.dat", "rb"))
            self.listbox_task.delete(0,END)
            ##adds .dt information by looping through contents
            for task in self.tasks:
                self.listbox_task.insert(END, self.tasks)
                print(self.tasks)
        except:
            ##if .dt is relocated somewhere different or isnt existing then warning message is displayed
            self.message_box = messagebox.showwarning(self.frame, title="Warning!", message="You must select a Todo.")

    ## function to save newly added tasks to .dt
    def save_tasks(self):
        ##add newly added tasks to .dt
        self.task = self.listbox_task.get(0, self.listbox_task.size())
        pickle.dump(self.task, open("tasks.dat", "wb"))
        ## print statement to visualize that transaction is complete
        print('Todo data entered successfully.')

    ## GUI for todolist
    #create frame
    def __init__(self, master):
        self.master = master
        self.master.title("todo")
        self.master.geometry("800x239")
        self.master.config(bg='grey')
        self.frame = Frame(self.master,bg='grey')
        self.frame.pack()

        #option menu for priority
        self.priority_selections  = ['Low','Medium','High']
        self.priority_task_entry = StringVar() 
        self.priority_task_entry.set(self.priority_selections[0])
        
        self.optionmenu_task_priority = OptionMenu(self.frame, self.priority_task_entry, *self.priority_selections)
        self.optionmenu_task_priority.grid(row=7, column=1, sticky="ew")

        #label
        self.label_todolist = Label(self.frame, text ="To-Do-List")
        self.label_todolist.grid(row=0, column=0)

        self.label_tasks = Label(self.frame, text ="TASKS:")
        self.label_tasks.grid(row=0, column=2, sticky=W)

        #label and entry for name
        self.label_task_name = Label(self.frame,text="Task Name")
        self.label_task_name.grid(row=0, column=1, sticky=W)
        self.entry_task_name = Entry(self.frame, width=20)
        self.entry_task_name.grid(row=1, column=1)

        #label and entry for subject
        self.label_task_subject = Label(self.frame,text="Task Subject")
        self.label_task_subject.grid(row=2, column=1, sticky=W)
        self.entry_task_subject = Entry(self.frame, width=20)
        self.entry_task_subject.grid(row=3, column=1)

        #label and entry for date
        self.label_task_date = Label(self.frame,text="Task Date")
        self.label_task_date.grid(row=4, column=1, sticky=W)
        self.entry_task_date = Entry(self.frame, width=20)
        self.entry_task_date.grid(row=5, column=1)

        #label for priority
        self.label_task_priority = Label(self.frame,text="Task Priority")
        self.label_task_priority.grid(row=6, column=1, sticky=W)

        #buttons for function to be applied
        self.button_add_task = Button(self.frame, text = 'Add Task', width = 17, command = self.add_tasks)
        self.button_add_task.grid(row=1, column=0)

        self.button_save_task = Button(self.frame, text = 'Save Tasks', width = 17, command = self.save_tasks)
        self.button_save_task.grid(row=2, column=0)

        self.button_load_task = Button(self.frame, text = 'Load Tasks', width = 17, command = self.load_tasks)
        self.button_load_task.grid(row=3, column=0)

        self.button_delete_task = Button(self.frame, text = 'Delete Task', width = 17, command = self.delete_tasks)
        self.button_delete_task.grid(row=4, column=0)
        
        self.button_exit_todolist = Button(self.frame, text = 'Close', width = 17, command = self.master.destroy)
        self.button_exit_todolist.grid(row=7, column=0)

        #create list box
        self.listbox_task = Listbox(self.frame, height=11, width=45)
        self.listbox_task.grid(row=1, column=2, rowspan=8)

##notes window (Window3)
class Window3:
    """ this function allows the person to add and delete notes which they insert. The note is categorised 3 ways.
    The first is the name, then subject and third is the note itself. The contents are added to the database and .dt file.

    """

    ##creating database for notes window, with "notes" table
    def connect_nt(self):
        self.connection_note = sqlite3.connect("notes_demo.db")
        self.cursor_note = self.connection_note.cursor()
        self.cursor_note.execute("CREATE TABLE IF NOT EXISTS notes(name char(30), subject char(35), notes char(255));")

    ##function to add note based on input GUI
    def add_notes(self):
        # get the var inputted in textfield
        self.note_name = self.entry_note_name.get()
        self.note_subject = self.entry_note_name.get()
        self.note = self.entry_note_note.get()
        if self.note_name or self.note_subject  or self.note !="":
            self.output = " Name: {} \nSubject: {} \nNote: {}".format(self.note_name, self.note_subject, self.note)
            self.listbox_notes_input = self.listbox_notes.insert(END, self.output)
            self.entry_note_name.delete(0,END)
            self.entry_note_name.delete(0,END)
            self.entry_note_note.delete(0,END)
            #make sure to add items to listbox if fields are filled and delete contents in texfield
        else:
            #warning message if fields arent completed
            self.message_box  = messagebox.showwarning(self.frame, title="Warning!", message="You must enter a Note.")
        self.connect_nt()
        self.cursor_note.execute("""INSERT INTO notes(name, subject, notes) VALUES (?,?,?)""",
                                 (self.note_name, self.note_subject, self.note))
        self.connection_note.commit()
        self.connection_note.close()
        
    ##function to delete a note in listbox with try and except
    def delete_notes(self):
        try:
            #select specific list in box
            self.selection_note = self.listbox_notes.curselection()
            #delete selected list in box
            self.listbox_notes.delete(self.selection_note)
        except:
            #show warning when list wasnt selected in box and delete was pressed
            self.message_box = messagebox.showwarning(self.frame, title="Warning!", message="You must select a Note.")

    ##open selected note with try and except        
    def open_selection(self,event):
        try:
            #select specific list in box
            self.t_i = self.listbox_notes.curselection()
            self.t = self.listbox_notes.get(self.t_i[0])
            #print selected note with information
            self.nf = Toplevel()
            self.m = Message(self.nf, text=self.t)
            self.m.pack(side="top", fill="both", expand=True, padx=100, pady=100)
            self.btn = Button(self.nf, text="Close" ,command = self.nf.destroy)
            self.btn.pack()
        except:
            #warning message
            self.message_box = messagebox.showwarning(self.frame, title="Warning!", message="You must select a Note.")

    ##function to load previous tasks saved on .dt file with try and except           
    def load_notes(self):
        try:
            #pickle opens and if file doesnt exist then it creates it
            self.notes = pickle.load(open("notes.dat", "rb"))
            self.listbox_notes.delete(0,END)
            #adds .dt information by looping through contents
            for task in self.notes:
                self.listbox_notes.insert(END, self.notes)
                print(self.notes)
        except:
            ##if .dt is relocated somewhere different or isnt existing then warning message is displayed
            self.message_box = messagebox.showwarning(self.frame, title="Warning!", message="You must select a Note.")

    ## function to save newly added tasks to .dt
    def save_notes(self):
        #add newly added tasks to .dt
        self.note = self.listbox_notes.get(0, self.listbox_notes.size())
        pickle.dump(self.note, open("notes.dat", "wb"))
        #print statement to visualize that transaction is complete
        print('Note data entered successfully.')

    ##Create GUI for notes
    #create frame
    def __init__(self, master):
        self.master = master
        self.master.title("Notes")
        self.master.geometry("800x239")
        self.master.config(bg='grey')
        self.frame = Frame(self.master,bg='grey')
        self.frame.pack()

        #labels
        self.label_notes = Label(self.frame, text ="Notes")
        self.label_notes.grid(row=0, column=2)

        self.label_notes = Label(self.frame, text ="NOTES:")
        self.label_notes.grid(row=0, column=0, sticky=W)

        #label and entry for name
        self.label_note_name = Label(self.frame,text="Note Name")
        self.label_note_name.grid(row=0, column=1, sticky=W)
        self.entry_note_name = Entry(self.frame, width=20)
        self.entry_note_name.grid(row=1, column=1)

        #label and entry for subject
        self.label_note_subject = Label(self.frame,text="Note Subject")
        self.label_note_subject.grid(row=2, column=1, sticky=W)
        self.entry_note_name = Entry(self.frame, width=20)
        self.entry_note_name.grid(row=3, column=1)

        #label and entry for note
        self.label_note_note = Label(self.frame,text="Note")
        self.label_note_note.grid(row=4, column=1, sticky=W)
        self.entry_note_note = Entry(self.frame, width=20)
        self.entry_note_note.grid(row=5, column=1)
  
        #buttons for function to be applied
        self.button_add_note = Button(self.frame, text = 'Add Note', width = 17, command = self.add_notes)
        self.button_add_note.grid(row=1, column=2)

        self.button_save_note = Button(self.frame, text = 'Save Note', width = 17, command = self.save_notes)
        self.button_save_note.grid(row=2, column=2)
        
        self.button_load_note = Button(self.frame, text = 'Load Note', width = 17, command = self.load_notes)
        self.button_load_note.grid(row=3, column=2)

        self.button_delete_note = Button(self.frame, text = 'Delete Note', width = 17, command = self.delete_notes)
        self.button_delete_note.grid(row=4, column=2)
        
        self.button_exit_notes = Button(self.frame, text = 'Close', width = 17, command = self.master.destroy)
        self.button_exit_notes.grid(row=7, column=2)

        #create list box
        self.listbox_notes = Listbox(self.frame, height=11, width=45)
        self.listbox_notes.grid(row=1, column=0, rowspan=8)
        self.listbox_notes.bind("<Double-Button-1>", self.open_selection)

##----------Classes for SQL script for both Notes.db and TodoList.db----------##      

##Script Todo window (Window4)
class Window4:
    ##GUI for script 
    def __init__(self, master):
        self.master = master
        self.master.title("Script Todo Page")
        self.master.geometry("200x100")
        self.master.config(bg='grey')
        self.frame = Frame(self.master,bg='grey')
        self.frame.pack()

        self.label_script = Label(self.frame, text ="Script To-Do-List")
        self.label_script.grid(row=0, column=0)

        self.button_script_todo_table_database = Button(self.frame, text = 'script', width = 17, command = self.selection)
        self.button_script_todo_table_database.grid(row=1, column=0)
        
        self.button_script_todo_exit = Button(self.frame, text = 'close', width = 17, command = self.master.destroy)
        self.button_script_todo_exit.grid(row=7, column=0)

    def selection(self):
        #create connection
        self.connection_todo = sqlite3.connect("tasks_demo.db")
        self.cursor_todo = self.connection_todo.cursor()

        #create frame with info
        self.pop_up_todo_scripting = Toplevel()

        # sql command
        self.sql = "SELECT * FROM todo"
        self.cursor_todo.execute(self.sql)
        for i in self.cursor_todo:
            script = i[0], i[1], i[2]
            print(script)
            self.label_script_todo_pop_up = Message(self.pop_up_todo_scripting, text =script)
            self.label_script_todo_pop_up.pack(side="top", fill="both", expand=True, padx=10, pady=10)
        self.connection_todo.close()

##Script Notes window (Window5)       
class Window5:
    ##GUI for script 
    def __init__(self, master):
        self.master = master
        self.master.title("Script Notes Page")
        self.master.geometry("200x100")
        self.master.config(bg='grey')
        self.frame = Frame(self.master,bg='grey')
        self.frame.pack()

        self.label_script = Label(self.frame, text ="Script Notes")
        self.label_script.grid(row=0, column=0)

        self.button_script_notes_table_databasen = Button(self.frame, text = 'script', width = 17, command = self.selection)
        self.button_script_notes_table_databasen.grid(row=1, column=0)
        
        self.button_script_notes_exit = Button(self.frame, text = 'close', width = 17, command = self.master.destroy)
        self.button_script_notes_exit.grid(row=2, column=0)

    
    def selection(self):
        #create connection
        self.connection_note = sqlite3.connect("notes_demo.db")
        self.cursor_note = self.connection_note.cursor()
        
        #create frame with info
        self.pop_up_note_scripting = Toplevel()

        # sql command
        self.sql = "SELECT * FROM notes"
        self.cursor_note.execute(self.sql)
        for i in self.cursor_note:
            script = i[0], i[1], i[2]
            print(script)
            self.label_script_notes_pop_up = Message(self.pop_up_note_scripting, text =script)
            self.label_script_notes_pop_up.pack(side="top", fill="both", expand=True, padx=10, pady=10)
        self.connection_note.close()

## makes the whole code run with the GUI appear 
if __name__ == '__main__':
    main()
