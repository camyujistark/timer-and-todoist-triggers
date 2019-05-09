#!/usr/local/bin/python

# TODOIST

from datetime import date, timedelta, datetime
from dateutil import parser
from todoist.api import TodoistAPI
import creds

# PROJECTS / IDs

todoist_api = TodoistAPI()

# GET ALL TASKS WITH DUE DATE


def todoist_list(date):

    # Sync (load) data
    todoist_api.sync()

    tasks = []

    for item in todoist_api.state['items']:
        due = item['due_date_utc']
        if due:
            # Slicing :10 gives us the relevant parts
            if due[:10] == date:
                tasks.append(item)

    # Sort by priority
    return sorted(tasks, key=lambda items: items['priority'], reverse=True)

# SCHEDULED WORK


def todoist_list_work(date, projects=None):

    todos = {}

    for item in todoist_list(date):
        name = get_todoist_project_name(item['project_id'])
        parent = get_todoist_parent_name(item)

        # if picking projects
        if(projects):
            if (name in projects):
                content = item['content']
                # subtasks
                if(parent):
                    todos.setdefault(parent, []).append({name: content})
                else:
                    todos.setdefault('Tasks', []).append({name: content})
        # or pick all
        else:
            if(parent):
                todos.setdefault(parent, []).append({name: content})
            else:
                content = item['content']
                todos.setdefault('Tasks', []).append({name: content})

    return todos


def todoist_list_todays_work(projects=None):

    day = (date.today()).strftime("%a %d %b")
    return todoist_list_work(day, projects)


def todoist_list_previous_work(projects=None, date_int=1):

    day = (date.today() - timedelta(date_int)).strftime("%a %d %b")
    return todoist_list_work(day, projects)


def todoist_list_future_work(projects=None, date_int=1):

    day = (date.today() + timedelta(date_int)).strftime("%a %d %b")
    return todoist_list_work(day, projects)


# COMPLETED WORK

def todoist_list_all_completed():

    # Sync (load) data
    todoist_api.sync
    completed = todoist_api.completed.get_all()

    return completed['items']


def todoist_list_completed_date(data, projects=None):

    completed = todoist_list_all_completed()

    if(isinstance(data, list)):
        completed_tasks = {}
        for d in data:
            day = (date.today() - timedelta(d)).strftime("%a %d %b")
            completed_day = []
            for item in completed:
                completed_date = ' '.join(item['completed_date'].split()[:3])
                if(completed_date == day):
                    name = get_todoist_project_name(item['project_id'])
                    if(projects and name in projects):
                        content = item['content']
                        parent = get_todoist_parent_name(item)
                        if(parent):
                            default = completed_tasks.setdefault(parent, [])
                            default.append({name: content})
                        else:
                            content = item['content']
                            default = completed_tasks.setdefault('Tasks', [])
                            default.append({name: content})
            completed_tasks[day] = completed_day

    else:
        completed_tasks = {}
        for item in completed:
            completed_date = ' '.join(item['completed_date'].split()[:3])
            day = (date.today() - timedelta(data)).strftime("%a %d %b")
            if(completed_date == day):
                name = get_todoist_project_name(item['project_id'])
                if(projects and name in projects):
                    content = item['content']
                    parent = get_todoist_parent_name(item)
                    if(parent):
                        default = completed_tasks.setdefault(parent, [])
                        default.append({name: content})
                    else:
                        content = item['content']
                        default = completed_tasks.setdefault('Tasks', [])
                        default.append({name: content})

    return completed_tasks


def todoist_list_completed(projects=None, date_int=1):

    return todoist_list_completed_date(date_int, projects)


def todoist_list_completed_last_seven_days(projects=None):

    dates = [6, 5, 4, 3, 2, 1, 0]
    return todoist_list_completed_date(dates, projects)

# HELPERS


def get_todoist_project_name(project_id):

    name = "Other"

    for project_name, project_key in creds.todoist_projects.iteritems():
        if project_id == project_key:
            name = project_name
            break

    return name


def get_todoist_parent_name(item):
    if not item:
        return

    name = ''
    check = 0
    parent_id = 0
    if type(item) is dict:
        check = 'parent_id' in item
        if(check):
            parent_id = item['parent_id']
    else:
        check = item['parent_id']
        if(check):
            parent_id = item['parent_id']

    if check:
        if parent_id is not None:
            parent = todoist_api.items.get_by_id(parent_id)
            name = parent['content']

    return name
