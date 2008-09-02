## Script (Python) "group_members_moderated"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=ids_only=False
##title=Get Moderated Group Members
##

def sorter(a,b):
    if a.getProperty('lastName') > b.getProperty('lastName'):
        return 1
    else:
        return -1

site_object = context.site_root()
group_object = context.Scripts.get.group_object()
group_id = group_object.getId()

members = filter(None, context.list_property(group_id, 'moderated_members', []))

retval = []
if ids_only:
    retval = members
else:
    member_objects = []
    for member in members:
        obj = site_object.acl_users.getUserById(member)
        if obj:
            member_objects.append(obj)
    retval = member_objects
    retval.sort(sorter)
return retval
