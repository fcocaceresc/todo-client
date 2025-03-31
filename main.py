import os
import tkinter as tk
from tkinter import ttk

import requests
from dotenv import load_dotenv

load_dotenv()
API_HOST = os.getenv('API_HOST')
API_PORT = os.getenv('API_PORT')


def get_tasks():
    url = f'http://{API_HOST}:{API_PORT}/todos'
    response = requests.get(url).json()
    return response['tasks']


def create_task():
    task_name = new_task_name_entry.get()
    new_task_name_entry.delete(0, tk.END)
    url = f'http://{API_HOST}:{API_PORT}/todos'
    task = {'name': task_name}
    response = requests.post(url, json=task)
    populate_tasks_treeview()


def populate_tasks_treeview():
    tasks = get_tasks()
    for row in tasks_treeview.get_children():
        tasks_treeview.delete(row)

    for task in tasks:
        task_id = task['id']
        task_name = task['name']
        tasks_treeview.insert('', tk.END, values=(task_id, task_name))


window = tk.Tk()
window.title('TODO')

tasks_label = tk.Label(window, text='Tasks')
tasks_label.pack()

tasks_treeview = ttk.Treeview(window, columns=('id', 'task'), show='headings')
tasks_treeview.heading('id', text='id')
tasks_treeview.heading('task', text='task')
tasks_treeview.pack()
populate_tasks_treeview()

create_task_frame = tk.Frame()
create_task_frame.pack()

create_task_title = tk.Label(create_task_frame, text='Create new task')
create_task_title.grid(row=0, column=0, columnspan=2)

new_task_name_label = tk.Label(create_task_frame, text='New task name:')
new_task_name_label.grid(row=1, column=0)

new_task_name_entry = tk.Entry(create_task_frame)
new_task_name_entry.grid(row=1, column=1)

create_task_btn = tk.Button(create_task_frame, text='Create task', command=create_task)
create_task_btn.grid(row=2, column=0, columnspan=2)

window.mainloop()
