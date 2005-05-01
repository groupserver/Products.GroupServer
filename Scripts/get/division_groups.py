## Script (Python) "division_groups"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##
division = context.division_object()

groups_object = None
for object in division.objectValues(['Folder','Folder (Ordered)']):
    if getattr(object, 'is_groups', 0):
        groups_object = object
        break

groups = []
if groups_object:
    for object in groups_object.objectValues(['Folder','Folder (Ordered)']):
        try:
            if getattr(object, 'is_group', 0):
                groups.append(object)
        except:
            pass

return groups
