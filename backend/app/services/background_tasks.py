# app/services/background_tasks.py

from fastapi import BackgroundTasks

def run_in_background(task_func, *args):
    background = BackgroundTasks()
    background.add_task(task_func, *args)
    return background
