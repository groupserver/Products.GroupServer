## Script (Python) "get_staff"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=id_only=0
##title=
##
site_root = context.site_root()
try:
    staff_group = site_root.acl_users.getGroupById('staff_member')
except:
    staff_group = None
if not staff_group:
   return ()

users = []
for user_id in staff_group.getUsers():
    users.append(site_root.acl_users.getUser(user_id))

if id_only:
    return map(lambda x: x.getId(), users)    
return users
