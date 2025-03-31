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


def create_task(create_task_name_entry):
    task_name = create_task_name_entry.get()
    create_task_name_entry.delete(0, tk.END)
    url = f'http://{API_HOST}:{API_PORT}/todos'
    task = {'name': task_name}
    response = requests.post(url, json=task)
    populate_tasks_treeview()


def update_task(update_task_id_entry, update_task_name_entry):
    task_id = int(update_task_id_entry.get())
    new_task_name = update_task_name_entry.get()
    update_task_id_entry.delete(0, tk.END)
    update_task_name_entry.delete(0, tk.END)
    url = f'http://{API_HOST}:{API_PORT}/todos/{task_id}'
    task_data = {'name': new_task_name}
    response = requests.put(url, json=task_data)
    populate_tasks_treeview()


def delete_task(delete_task_id_entry):
    task_id = int(delete_task_id_entry.get())
    delete_task_id_entry.delete(0, tk.END)
    url = f'http://{API_HOST}:{API_PORT}/todos/{task_id}'
    response = requests.delete(url)
    populate_tasks_treeview()


def populate_tasks_treeview():
    tasks = get_tasks()
    for row in tasks_treeview.get_children():
        tasks_treeview.delete(row)

    for task in tasks:
        task_id = task['id']
        task_name = task['name']
        tasks_treeview.insert('', tk.END, values=(task_id, task_name))


def create_task_section(parent):
    create_task_frame = tk.Frame(parent)
    create_task_frame.pack()

    create_task_title = tk.Label(create_task_frame, text='Create task')
    create_task_title.grid(row=0, column=0, columnspan=2)

    create_task_name_label = tk.Label(create_task_frame, text='New task name:')
    create_task_name_label.grid(row=1, column=0)

    create_task_name_entry = tk.Entry(create_task_frame)
    create_task_name_entry.grid(row=1, column=1)

    create_task_btn = tk.Button(
        create_task_frame,
        text='Create task',
        command=lambda : create_task(create_task_name_entry)
    )
    create_task_btn.grid(row=2, column=0, columnspan=2)


def update_task_section(parent):
    update_task_frame = tk.Frame(parent)
    update_task_frame.pack()

    update_task_title = tk.Label(update_task_frame, text='Update task')
    update_task_title.grid(row=0, column=0, columnspan=2)

    update_task_id_label = tk.Label(update_task_frame, text='Id of the task to update:')
    update_task_id_label.grid(row=1, column=0)

    update_task_id_entry = tk.Entry(update_task_frame)
    update_task_id_entry.grid(row=1, column=1)

    update_task_name_label = tk.Label(update_task_frame, text='Updated task name:')
    update_task_name_label.grid(row=2, column=0)

    update_task_name_entry = tk.Entry(update_task_frame)
    update_task_name_entry.grid(row=2, column=1)

    update_task_btn = tk.Button(
        update_task_frame,
        text='Update task',
        command=lambda: update_task(update_task_id_entry, update_task_name_entry)
    )
    update_task_btn.grid(row=3, column=0, columnspan=2)


def delete_task_section(parent):
    delete_task_frame = tk.Frame(parent)
    delete_task_frame.pack()

    delete_task_title = tk.Label(delete_task_frame, text='Delete task')
    delete_task_title.grid(row=0, column=0, columnspan=2)

    delete_task_id_label = tk.Label(delete_task_frame, text='Id of the task to delete')
    delete_task_id_label.grid(row=1, column=0)

    delete_task_id_entry = tk.Entry(delete_task_frame)
    delete_task_id_entry.grid(row=1, column=1)

    delete_task_btn = tk.Button(
        delete_task_frame,
        text='Delete task',
        command=lambda : delete_task(delete_task_id_entry)
    )
    delete_task_btn.grid(row=2, column=0, columnspan=2)


window = tk.Tk()
window.title('TODO')

tasks_label = tk.Label(window, text='Tasks')
tasks_label.pack()

tasks_treeview = ttk.Treeview(window, columns=('id', 'task'), show='headings')
tasks_treeview.heading('id', text='id')
tasks_treeview.heading('task', text='task')
tasks_treeview.pack()
populate_tasks_treeview()

create_task_section(window)
update_task_section(window)
delete_task_section(window)

window.mainloop()
