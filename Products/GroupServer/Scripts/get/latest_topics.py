## Script (Python) "latest_topics"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=limit=12
##title=
##
division_object = context.get.division_object()

def sorter(x, y):
    if x[1][0]['mailDate'] < y[1][0]['mailDate']:
        return 1
    else:
        return -1

messages = []
for group in filter(lambda x: getattr(x, 'is_group', 0), context.Scripts.get.object_values(division_object.groups, 'Folder')):
    try:
        nm = group.messages.thread_results(context.REQUEST, 0, 5, 'mailDate', 'desc')[4]
    except:
        continue
    nt = []
    for thread in nm:
        thread = list(thread)
        thread += [group.getId(), group.title_or_id()]
        nt.append(thread)
    
    messages += nt

messages.sort(sorter)

return messages[:limit]
