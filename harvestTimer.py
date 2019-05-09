#!/usr/local/bin/python

# harvest

import harvest, sys
import creds

client = harvest.Harvest(creds.url, creds.username, creds.password)

entries = client.today_user(creds.user)
day_entries = entries['day_entries']
timerToggle = ''


def timer(start):
    # Check to whether project already started
    linktree_entries = []
    for entry in day_entries:
        # Linktree Development
        if(entry['project_id'] == creds.project_id and
                entry['task_id'] == creds.task_id):
            linktree_entries.append(entry)

    selected = []
    for entry in linktree_entries:
        if(timer_started(entry)):
            selected = entry
            break
        else:
            # get last linktree task
            selected = linktree_entries[-1]
            break

    # Run Harvest Commands
    if(selected):
        update_timer(selected, start)
    else:
        new_timer("Linktree Development")


def timer_started(entry):
    if('timer_started_at' in entry):
        return 1
    else:
        return 0


def update_timer(entry, start):
    if(start == 'StartTimer'):
        client.toggle_timer(entry['id']) if timer_started(entry) == 0 else 0

    elif(start == 'StopTimer'):
        client.toggle_timer(entry['id']) if timer_started(entry) == 1 else 0


def new_timer(text):
    data = {
        "notes": text,
        "project_id": creds.project_id,
        "task_id": creds.task_id
    }
    client.add(data)


def start():
    timer('StartTimer')


def stop():
    timer('StopTimer')

