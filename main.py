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

window.mainloop()
