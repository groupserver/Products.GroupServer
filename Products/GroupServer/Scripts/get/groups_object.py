## Script (Python) "groups_object"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##
try:
    division_object = context.Scripts.get.division_object()
    groups_object = division_object.groups
except:
    groups_object = context

found = False
while groups_object:
    try:
        if getattr(groups_object.aq_explicit, 'is_groups', 0):
            found = True
            break
        groups_object = groups_object.aq_parent
    except:
        break

if found:
    return groups_object.aq_inner.aq_explicit

return None
