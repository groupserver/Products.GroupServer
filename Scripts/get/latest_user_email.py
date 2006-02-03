## Script (Python) "latest_topics"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=user_id, limit=15
##title=
##
division_object = context.get.division_object()

def sorter(x, y):
    if x['mailDate'] < y['mailDate']:
        return 1
    else:
        return -1

messages = []
for group in filter(lambda x: getattr(x, 'is_group', 0), context.Scripts.get.object_values(division_object.groups, 'Folder')):
    try:
        messages += group.messages.find_email({'mailUserId': user_id})
    except:
        pass

messages.sort(sorter)

return messages[:limit]
