## Script (Python) "get_contacts"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=id_only=0, include_staff=1
##title=
##
user = context.REQUEST.AUTHENTICATED_USER
division_objects = context.get_division_objects()
site_root=context.site_root()

def mycmp(x, y):
    return cmp(x.firstName, y.firstName)

group_objects = []
for division in division_objects:
   if hasattr(division, 'groups'):
       objects = context.Scripts.get.object_values(division.groups, ['Folder'])
       for object in objects:
           if object and getattr(object, 'is_group', 0) and \
             (not object.getId().find('_announce') > -1) and \
             'GroupMember' in user.getRolesInContext(object):
               group_objects.append(object)

user_ids = []
for group_object in group_objects:
    groups = group_object.groups_with_local_role('GroupMember')
    for group in groups:
        sgroup = group_object.acl_users.getGroupById(group)
        for user_id in sgroup.getUsers():
            if user_id not in user_ids:
                user_ids.append(user_id)

staff_list = context.Scripts.contacts.get_staff(1)

for staff_id in staff_list:
    if staff_id not in user_ids:
        user_ids.append(staff_id)

uid = user.getId()
if not id_only:
    r = map(lambda x: site_root.acl_users.getUser(x), user_ids)
    r = filter(None, r)
    r.sort(mycmp)
    r = filter(lambda x: x.getId() != uid, r)
    return r

r = filter(lambda x: x and x.getId() != uid, user_ids)
return r
