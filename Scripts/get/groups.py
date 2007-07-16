## Script (Python) "groups"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=groups_object=None
##title=
##
groups_object = groups_object or context.Scripts.get.groups_object()
groups = []
if not groups_object:
    return groups

for id in groups_object.objectIds(('Folder', 'Folder (Ordered)')):
    try:
        object = getattr(groups_object, id)
        groups.append((object.title_or_id().lower(), object))
    except:
        pass

# quickly sort alphabetically -- we do this to avoid
# fetching the title_or_id multiple times
groups.sort()
groups = map(lambda x: x[1], groups)

return groups
