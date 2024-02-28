import tkinter as tk
from tkinter import simpledialog, messagebox

# Main Class for To do list App
class TodoList_App:
    def __init__(self, master):
        self.master = master
        self.master.title("To-Do List App")
        self.master.configure(bg='aquamarine1')

        self.create_widgets()

        # TO Store Tasks
        self.tasks = []
 
 # For Frames
    def create_widgets(self):
        # First Frame - Title
        self.first_frame = tk.Frame(self.master)
        self.first_frame.pack(pady=10)

        self.title_label = tk.Label(self.first_frame, text=" Wel-Come To-Do List App : ", font=("Helvetica", 16, 'bold', 'underline'), bg='aquamarine1')
        self.title_label.pack()

        # Second Frame - Buttons
        self.second_frame = tk.Frame(self.master)
        self.second_frame.configure(bg='aquamarine1')
        self.second_frame.pack(pady=10)

        tk.Button(self.second_frame, text=" Add Task ", command=self.open_add_task_window, font=("Helvetica", 12, "bold"), bg='hotpink', height=1).grid(row=0, column=0, padx=1)
        tk.Button(self.second_frame, text=" Edit Task ", command=self.open_edit_task_window, font=("Helvetica", 12, "bold"), bg='hotpink', height=1).grid(row=0, column=1, padx=10)
        tk.Button(self.second_frame, text=" Delete Task ", command=self.delete_task, font=("Helvetica", 12, "bold"), bg='hotpink', height=1).grid(row=0, column=2, padx=10)
        tk.Button(self.second_frame, text=" Track Tasks ", command=self.open_track_tasks_window, font=("Helvetica", 12, "bold"), bg='hotpink', height=1).grid(row=0, column=3, padx=10)

        # Third Frame - Display Tasks
        self.third_frame = tk.Frame(self.master)
        self.third_frame.pack(pady=10)

        self.task_listbox = tk.Listbox(self.third_frame, width=50, height=15, bg='ghostwhite')
        self.task_listbox.pack(padx=10, pady=10)

# Methods for operating Buttons
        
        
    def open_add_task_window(self): # For Add Button
        add_task_window = self.create_dialog_window("Add Task")
        add_task_window.configure(bg='aquamarine1')

        tk.Label(add_task_window, text="Title:", bg='aquamarine1', font=('bold')).grid(row=0, column=0, padx=10, pady=5)
        tk.Label(add_task_window, text="Description:", bg='aquamarine1', font=('bold')).grid(row=1, column=0, padx=10, pady=5)
        tk.Label(add_task_window, text="Status:", bg='aquamarine1', font=('bold')).grid(row=2, column=0, padx=10, pady=5)

        title_entry = tk.Entry(add_task_window)
        description_entry = tk.Entry(add_task_window)
        status_var = tk.StringVar(value="Pending")
        status_radio_pending = tk.Radiobutton(add_task_window, text="Pending", variable=status_var, value="Pending", bg='aquamarine1')
        status_radio_complete = tk.Radiobutton(add_task_window, text="Completed", variable=status_var, value="Completed", bg='aquamarine1')

        title_entry.grid(row=0, column=1, padx=10, pady=5)
        description_entry.grid(row=1, column=1, padx=10, pady=5)
        status_radio_pending.grid(row=2, column=1, padx=10, pady=5)
        status_radio_complete.grid(row=2, column=2, padx=10, pady=5)

        tk.Button(add_task_window, text="Save", command=lambda: self.save_task(title_entry.get(), description_entry.get(), status_var.get(), add_task_window), bg='hotpink', height=1).grid(row=3, column=0, columnspan=3, pady=10)

    def open_edit_task_window(self): # For Edit Button
        selected_task_index = self.display_tasks()
        if selected_task_index is not None:
            selected_task = self.tasks[selected_task_index]
            edit_task_window = self.create_dialog_window("Edit Task")
            edit_task_window.configure(bg='aquamarine1')


            tk.Label(edit_task_window, text="Title : ",bg='aquamarine1', font=('bold')).grid(row=0, column=0, padx=10, pady=5)
            tk.Label(edit_task_window, text="Description : ",bg='aquamarine1', font=('bold')).grid(row=1, column=0, padx=10, pady=5)
            tk.Label(edit_task_window, text="Status : ",bg='aquamarine1', font=('bold')).grid(row=2, column=0, padx=10, pady=5)

            title_entry = tk.Entry(edit_task_window)
            description_entry = tk.Entry(edit_task_window)
            status_var = tk.StringVar(value=selected_task['status'])
            status_radio_pending = tk.Radiobutton(edit_task_window, text="Pending",bg='aquamarine1', font=('bold'), variable=status_var, value="Pending")
            status_radio_complete = tk.Radiobutton(edit_task_window, text="Completed", bg='aquamarine1', font=('bold'),variable=status_var, value="Completed")

            title_entry.insert(tk.END, selected_task['title'])
            description_entry.insert(tk.END, selected_task['description'])

            title_entry.grid(row=0, column=1, padx=10, pady=5)
            description_entry.grid(row=1, column=1, padx=10, pady=5)
            status_radio_pending.grid(row=2, column=1, padx=10, pady=5)
            status_radio_complete.grid(row=2, column=2, padx=10, pady=5)

            tk.Button(edit_task_window, text="Save",bg='hotpink', command=lambda: self.save_edited_task(title_entry.get(), description_entry.get(), status_var.get(), selected_task_index, edit_task_window)).grid(row=3, column=0, columnspan=3, pady=10)

    def delete_task(self): # Delete Button
        selected_task_index = self.display_tasks()
        if selected_task_index is not None:
            del self.tasks[selected_task_index]
            self.update_display()

    def save_task(self, title, description, status, add_task_window):
        self.tasks.append({"title": title, "description": description, "status": status})
        messagebox.showinfo("Success", "Task added successfully!")
        add_task_window.destroy()
        self.update_display()

    def save_edited_task(self, title, description, status, selected_task_index, edit_task_window):
        self.tasks[selected_task_index]["title"] = title
        self.tasks[selected_task_index]["description"] = description
        self.tasks[selected_task_index]["status"] = status
        messagebox.showinfo("Success", "Task edited successfully!")
        edit_task_window.destroy()
        self.update_display()

    def display_tasks(self): # For Display Tasks
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            return selected_task_index[0]
        return None

    def open_track_tasks_window(self): # To Track Tasks
        track_window = self.create_dialog_window("Track Tasks")
        track_window.configure(bg='aquamarine1')

        tk.Label(track_window, text="Pending Tasks :",bg='aquamarine1', font=('bold')).grid(row=0, column=0, padx=10, pady=5)
        tk.Label(track_window, text="Completed Tasks :",bg='aquamarine1', font=('bold',)).grid(row=2, column=0, padx=10, pady=5)

        pending_tasks = [task for task in self.tasks if task['status'] == 'Pending']
        complete_tasks = [task for task in self.tasks if task['status'] == 'Completed']

        self.create_listbox(track_window, pending_tasks, row=1)
        self.create_listbox(track_window, complete_tasks, row=3)

    def create_dialog_window(self, title):
        dialog_window = tk.Toplevel(self.master)
        dialog_window.title(title)
        return dialog_window

        

    def create_listbox(self, parent, tasks, row):
        listbox = tk.Listbox(parent, width=50, height=10)
        for task in tasks:
            listbox.insert(tk.END, f"Title: {task['title']} | Description: {task['description']} | Status: {task['status']}")
        listbox.grid(row=row, column=0, padx=10, pady=5)

    def update_display(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.tasks:
            self.task_listbox.insert(tk.END, f"Title: {task['title']} | Description: {task['description']} | Status: {task['status']}")

    def delete_task(self):
        selected_task_index = self.display_tasks()
        if selected_task_index is not None:
            del self.tasks[selected_task_index]
            self.update_display()

    def save_task(self, title, description, status, add_task_window):
        self.tasks.append({"title": title, "description": description, "status": status})
        messagebox.showinfo("Success", "Task added successfully!")
        add_task_window.destroy()
        self.update_display()

# Main Tk Window
def main():
    to_do_list = tk.Tk()
    app = TodoList_App(to_do_list)
    to_do_list.configure(bg='aquamarine1')
    to_do_list.geometry('500x500')
    to_do_list.resizable('False','False')
    to_do_list.iconbitmap('icon file.ico')
    to_do_list.mainloop()

if __name__ == "__main__":
    main()

