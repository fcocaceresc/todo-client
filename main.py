import os
import tkinter as tk
from tkinter import ttk

import requests
from dotenv import load_dotenv

load_dotenv()
API_HOST = os.getenv('API_HOST')
API_PORT = os.getenv('API_PORT')


class TodoApp(tk.Tk):

    def __init__(self, api_host, api_port):
        super().__init__()
        self.title('TODO App')

        self.api = TodoAPI(api_host, api_port)

        self.show_login()

    def clear_window(self):
        for widget in self.winfo_children():
            widget.pack_forget()

    def show_login(self):
        self.clear_window()
        self.login_frame = LoginFrame(self, show_signup=self.show_signup)
        self.login_frame.pack()

    def show_signup(self):
        self.clear_window()
        self.signup_frame = SignupFrame(self, show_login=self.show_login)
        self.signup_frame.pack()

    def show_dashboard(self):
        self.tasks_frame = TasksFrame(self, self.api)
        self.tasks_frame.pack()

        self.create_task_frame = CreateTaskFrame(
            self,
            self.api,
            on_task_created=self.tasks_frame.refresh_tasks
        )
        self.create_task_frame.pack()

        self.update_task_frame = UpdateTaskFrame(
            self,
            self.api,
            on_task_updated=self.tasks_frame.refresh_tasks
        )
        self.update_task_frame.pack()

        self.delete_task_frame = DeleteTaskFrame(
            self,
            self.api,
            on_task_deleted=self.tasks_frame.refresh_tasks
        )
        self.delete_task_frame.pack()


class TodoAPI:

    def __init__(self, api_host, api_port):
        self.base_url = f'http://{api_host}:{api_port}/todos'

    def get_tasks(self):
        response = requests.get(self.base_url).json()
        return response['tasks']

    def create_task(self, task_name):
        task = {'name': task_name}
        response = requests.post(self.base_url, json=task)

    def update_task(self, task_id, task_name):
        url = f'{self.base_url}/{task_id}'
        task_data = {'name': task_name}
        response = requests.put(url, json=task_data)

    def delete_task(self, task_id):
        url = f'{self.base_url}/{task_id}'
        response = requests.delete(url)


class LoginFrame(tk.Frame):

    def __init__(self, parent, show_signup):
        super().__init__(parent)

        self.show_signup = show_signup

        self.login_title = tk.Label(self, text='Login')
        self.login_title.grid(row=0, column=0, columnspan=2)

        self.username_label = tk.Label(self, text='Username')
        self.username_label.grid(row=1, column=0)

        self.username_entry = tk.Entry(self)
        self.username_entry.grid(row=1, column=1)

        self.password_label = tk.Label(self, text='Password')
        self.password_label.grid(row=2, column=0)

        self.password_entry = tk.Entry(self)
        self.password_entry.grid(row=2, column=1)

        self.submit_btn = tk.Button(self, text='Submit')
        self.submit_btn.grid(row=3, column=0, columnspan=2)

        self.signup_btn = tk.Button(self, text="Don't have an account? Sign up", command=self.show_signup)
        self.signup_btn.grid(row=4, column=0, columnspan=2)


class SignupFrame(tk.Frame):

    def __init__(self, parent, show_login):
        super().__init__(parent)

        self.show_login = show_login

        self.signup_title = tk.Label(self, text='Sign up')
        self.signup_title.grid(row=0, column=0, columnspan=2)

        self.username_label = tk.Label(self, text='Username')
        self.username_label.grid(row=1, column=0)

        self.username_entry = tk.Entry(self)
        self.username_entry.grid(row=1, column=1)

        self.password_label = tk.Label(self, text='Password')
        self.password_label.grid(row=2, column=0)

        self.password_entry = tk.Entry(self)
        self.password_entry.grid(row=2, column=1)

        self.submit_btn = tk.Button(self, text='Submit')
        self.submit_btn.grid(row=3, column=0, columnspan=2)

        self.signup_btn = tk.Button(self, text="Already have an account? Log in", command=self.show_login)
        self.signup_btn.grid(row=4, column=0, columnspan=2)


class TasksFrame(tk.Frame):

    def __init__(self, parent, api):
        super().__init__(parent)

        self.tasks_title = tk.Label(self, text='Tasks')
        self.tasks_title.grid(row=0, column=0)

        self.tasks_treeview = ttk.Treeview(self, columns=('id', 'task'), show='headings')
        self.tasks_treeview.heading('id', text='id')
        self.tasks_treeview.heading('task', text='task')
        self.tasks_treeview.grid(row=1, column=0)

        self.api = api

        self.refresh_tasks()

    def refresh_tasks(self):
        tasks = self.api.get_tasks()

        for row in self.tasks_treeview.get_children():
            self.tasks_treeview.delete(row)

        for task in tasks:
            task_id = task['id']
            task_name = task['name']
            self.tasks_treeview.insert('', tk.END, values=(task_id, task_name))


class CreateTaskFrame(tk.Frame):

    def __init__(self, parent, api, on_task_created):
        super().__init__(parent)

        self.api = api

        self.on_task_created = on_task_created

        self.create_task_title = tk.Label(self, text='Create task')
        self.create_task_title.grid(row=0, column=0, columnspan=2)

        self.create_task_name_label = tk.Label(self, text='New task name:')
        self.create_task_name_label.grid(row=1, column=0)

        self.create_task_name_entry = tk.Entry(self)
        self.create_task_name_entry.grid(row=1, column=1)

        self.create_task_btn = tk.Button(self, text='Create task', command=self.create_task)
        self.create_task_btn.grid(row=2, column=0, columnspan=2)

    def create_task(self):
        task_name = self.create_task_name_entry.get()
        self.create_task_name_entry.delete(0, tk.END)
        self.api.create_task(task_name)
        self.on_task_created()


class UpdateTaskFrame(tk.Frame):

    def __init__(self, parent, api, on_task_updated):
        super().__init__(parent)

        self.api = api

        self.on_task_updated = on_task_updated

        self.update_task_title = tk.Label(self, text='Update task')
        self.update_task_title.grid(row=0, column=0, columnspan=2)

        self.update_task_id_label = tk.Label(self, text='Id of the task to update:')
        self.update_task_id_label.grid(row=1, column=0)

        self.update_task_id_entry = tk.Entry(self)
        self.update_task_id_entry.grid(row=1, column=1)

        self.update_task_name_label = tk.Label(self, text='Updated task name:')
        self.update_task_name_label.grid(row=2, column=0)

        self.update_task_name_entry = tk.Entry(self)
        self.update_task_name_entry.grid(row=2, column=1)

        self.update_task_btn = tk.Button(self, text='Update task', command=self.update_task)
        self.update_task_btn.grid(row=3, column=0, columnspan=2)

    def update_task(self):
        task_id = int(self.update_task_id_entry.get())
        task_name = self.update_task_name_entry.get()
        self.update_task_id_entry.delete(0, tk.END)
        self.update_task_name_entry.delete(0, tk.END)
        self.api.update_task(task_id, task_name)
        self.on_task_updated()


class DeleteTaskFrame(tk.Frame):

    def __init__(self, parent, api, on_task_deleted):
        super().__init__(parent)

        self.api = api

        self.on_task_deleted = on_task_deleted

        self.delete_task_title = tk.Label(self, text='Delete task')
        self.delete_task_title.grid(row=0, column=0, columnspan=2)

        self.delete_task_id_label = tk.Label(self, text='Id of the task to delete')
        self.delete_task_id_label.grid(row=1, column=0)

        self.delete_task_id_entry = tk.Entry(self)
        self.delete_task_id_entry.grid(row=1, column=1)

        self.delete_task_btn = tk.Button(self, text='Delete task', command=self.delete_task)
        self.delete_task_btn.grid(row=2, column=0, columnspan=2)

    def delete_task(self):
        task_id = int(self.delete_task_id_entry.get())
        self.delete_task_id_entry.delete(0, tk.END)
        self.api.delete_task(task_id)
        self.on_task_deleted()


app = TodoApp(API_HOST, API_PORT)
app.mainloop()
