import os
import tkinter as tk
from tkinter import ttk, messagebox

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

    def on_login(self, username, password):
        response = self.api.login(username, password)
        if response.status_code == 200:
            messagebox.showinfo('Success', 'Logged in successfully')
            self.show_dashboard()
        else:
            messagebox.showerror('Error', 'Login failed')

    def on_signup(self, username, password):
        response = self.api.signup(username, password)
        if response.status_code == 201:
            messagebox.showinfo('Success', 'Signed up successfully')
            self.show_login()
        else:
            messagebox.showerror('Error', 'Sign up failed')

    def show_login(self):
        self.clear_window()
        self.login_frame = LoginFrame(self, show_signup=self.show_signup, on_login=self.on_login)
        self.login_frame.pack()

    def show_signup(self):
        self.clear_window()
        self.signup_frame = SignupFrame(self, show_login=self.show_login, on_signup=self.on_signup)
        self.signup_frame.pack()

    def show_dashboard(self):
        self.clear_window()
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
        self.token = None
        self.headers = {'Content-Type': 'application/json'}
        self.base_url = f'http://{api_host}:{api_port}'

    def login(self, username, password):
        user_data = {
            'username': username,
            'password': password
        }
        response = requests.post(f'{self.base_url}/login', json=user_data)
        if response.status_code == 200:
            self.token = response.json()['token']
            self.generate_headers()
        return response

    def signup(self, username, password):
        user_data = {
            'username': username,
            'password': password
        }
        response = requests.post(f'{self.base_url}/signup', json=user_data)
        return response

    def generate_headers(self):
        self.headers['Authorization'] = f'Bearer {self.token}'

    def get_tasks(self):
        response = requests.get(
            f'{self.base_url}/todos',
            headers=self.headers
        ).json()
        return response['tasks']

    def create_task(self, title, description):
        task = {
            'title': title,
            'description': description
        }
        response = requests.post(
            f"{self.base_url}/todos",
            headers=self.headers,
            json=task
        )
        return response

    def update_task(self, task_id, title, description):
        task_data = {
            'title': title,
            'description': description
        }
        response = requests.put(
            f"{self.base_url}/todos/{task_id}",
            headers=self.headers,
            json=task_data
        )
        return response

    def delete_task(self, task_id):
        response = requests.delete(
            f"{self.base_url}/todos/{task_id}",
            headers=self.headers
        )
        return response


class LoginFrame(tk.Frame):

    def __init__(self, parent, show_signup, on_login):
        super().__init__(parent)

        self.show_signup = show_signup

        self.on_login = on_login

        self.login_title = tk.Label(self, text='Login')
        self.login_title.grid(row=0, column=0, columnspan=2)

        self.username_label = tk.Label(self, text='Username')
        self.username_label.grid(row=1, column=0)

        self.username_entry = tk.Entry(self)
        self.username_entry.grid(row=1, column=1)

        self.password_label = tk.Label(self, text='Password')
        self.password_label.grid(row=2, column=0)

        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.grid(row=2, column=1)

        self.submit_btn = tk.Button(self, text='Submit', command=self.login)
        self.submit_btn.grid(row=3, column=0, columnspan=2)

        self.signup_btn = tk.Button(self, text="Don't have an account? Sign up", command=self.show_signup)
        self.signup_btn.grid(row=4, column=0, columnspan=2)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        self.on_login(username, password)


class SignupFrame(tk.Frame):

    def __init__(self, parent, show_login, on_signup):
        super().__init__(parent)

        self.show_login = show_login

        self.on_signup = on_signup

        self.signup_title = tk.Label(self, text='Sign up')
        self.signup_title.grid(row=0, column=0, columnspan=2)

        self.username_label = tk.Label(self, text='Username')
        self.username_label.grid(row=1, column=0)

        self.username_entry = tk.Entry(self)
        self.username_entry.grid(row=1, column=1)

        self.password_label = tk.Label(self, text='Password')
        self.password_label.grid(row=2, column=0)

        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.grid(row=2, column=1)

        self.submit_btn = tk.Button(self, text='Submit', command=self.signup)
        self.submit_btn.grid(row=3, column=0, columnspan=2)

        self.signup_btn = tk.Button(self, text="Already have an account? Log in", command=self.show_login)
        self.signup_btn.grid(row=4, column=0, columnspan=2)

    def signup(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        self.on_signup(username, password)


class TasksFrame(tk.Frame):

    def __init__(self, parent, api):
        super().__init__(parent)

        self.tasks_title = tk.Label(self, text='Tasks')
        self.tasks_title.grid(row=0, column=0)

        self.tasks_treeview = ttk.Treeview(self, columns=('id', 'title', 'description'), show='headings')
        self.tasks_treeview.heading('id', text='ID')
        self.tasks_treeview.heading('title', text='Title')
        self.tasks_treeview.heading('description', text='Description')
        self.tasks_treeview.grid(row=1, column=0)

        self.api = api

        self.tasks_treeview.bind('<<TreeviewSelect>>', self.on_select_task)

        self.refresh_tasks()

    def refresh_tasks(self):
        tasks = self.api.get_tasks()

        for row in self.tasks_treeview.get_children():
            self.tasks_treeview.delete(row)

        for task in tasks:
            task_id = task['_id']
            task_title = task['title']
            task_description = task['description']
            self.tasks_treeview.insert('', tk.END, values=(task_id, task_title, task_description))

    def on_select_task(self, event):
        selected_item = self.tasks_treeview.selection()
        if selected_item:
            task_id = self.tasks_treeview.item(selected_item, 'values')[0]
            self.master.update_task_frame.set_task_id(task_id)
            self.master.delete_task_frame.set_task_id(task_id)


class CreateTaskFrame(tk.Frame):

    def __init__(self, parent, api, on_task_created):
        super().__init__(parent)

        self.api = api

        self.on_task_created = on_task_created

        self.create_task_title = tk.Label(self, text='Create task')
        self.create_task_title.grid(row=0, column=0, columnspan=2)

        self.create_task_name_label = tk.Label(self, text='New task title:')
        self.create_task_name_label.grid(row=1, column=0)

        self.create_task_name_entry = tk.Entry(self)
        self.create_task_name_entry.grid(row=1, column=1)

        self.create_task_description_label = tk.Label(self, text='New task description:')
        self.create_task_description_label.grid(row=2, column=0)

        self.create_task_description_entry = tk.Entry(self)
        self.create_task_description_entry.grid(row=2, column=1)

        self.create_task_btn = tk.Button(self, text='Create task', command=self.create_task)
        self.create_task_btn.grid(row=3, column=0, columnspan=2)

    def create_task(self):
        task_name = self.create_task_name_entry.get()
        self.create_task_name_entry.delete(0, tk.END)

        task_description = self.create_task_description_entry.get()
        self.create_task_description_entry.delete(0, tk.END)

        response = self.api.create_task(task_name, task_description)
        if response.status_code == 201:
            messagebox.showinfo('Success', 'Task created successfully')
            self.on_task_created()
        else:
            messagebox.showerror('Error', 'Failed to create task')


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

        self.update_task_name_label = tk.Label(self, text='Updated task title:')
        self.update_task_name_label.grid(row=2, column=0)

        self.update_task_name_entry = tk.Entry(self)
        self.update_task_name_entry.grid(row=2, column=1)

        self.update_task_description_label = tk.Label(self, text='Updated task description:')
        self.update_task_description_label.grid(row=3, column=0)

        self.update_task_description_entry = tk.Entry(self)
        self.update_task_description_entry.grid(row=3, column=1)

        self.update_task_btn = tk.Button(self, text='Update task', command=self.update_task)
        self.update_task_btn.grid(row=4, column=0, columnspan=2)

    def set_task_id(self, task_id):
        self.update_task_id_entry.delete(0, tk.END)
        self.update_task_id_entry.insert(0, task_id)

    def update_task(self):
        task_id = self.update_task_id_entry.get()
        task_name = self.update_task_name_entry.get()
        task_description = self.update_task_description_entry.get()

        self.update_task_id_entry.delete(0, tk.END)
        self.update_task_name_entry.delete(0, tk.END)
        self.update_task_description_entry.delete(0, tk.END)

        response = self.api.update_task(task_id, task_name, task_description)
        if response.status_code == 200:
            messagebox.showinfo('Success', 'Task updated successfully')
            self.on_task_updated()
        else:
            messagebox.showerror('Error', 'Failed to update task')


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

    def set_task_id(self, task_id):
        self.delete_task_id_entry.delete(0, tk.END)
        self.delete_task_id_entry.insert(0, task_id)

    def delete_task(self):
        task_id = self.delete_task_id_entry.get()
        self.delete_task_id_entry.delete(0, tk.END)
        response = self.api.delete_task(task_id)
        if response.status_code == 200:
            messagebox.showinfo('Success', 'Task deleted successfully')
            self.on_task_deleted()
        else:
            messagebox.showerror('Error', 'Failed to delete task')


app = TodoApp(API_HOST, API_PORT)
app.mainloop()
