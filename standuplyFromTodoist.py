#!/usr/local/bin/python

import todoistSchedule

projects = ['Linktree', 'Bolster']

completed = todoistSchedule.todoist_list_completed(projects)

if completed:
    print('*Completed Yesterday*')
    for k in completed:
        print(k)
        for p in completed[k]:
            for k in p:
                print(p[k])
    print('')

# scheduled = todoistSchedule.todoist_list_previous_work(projects)
#
# if scheduled:
#     print('*Was Looking to Complete Yesterday*')
#     for k in scheduled:
#         print(k)
#         for p in scheduled[k]:
#             for k in p:
#                 print(p[k])
#     print('')

today = todoistSchedule.todoist_list_todays_work(projects)
if today:
    print('*Working on today*')
    for k in today:
        print(k)
        for p in today[k]:
            for k in p:
                print(p[k])
