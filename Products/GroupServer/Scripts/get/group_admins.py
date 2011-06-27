## Script (Python) "group_admins"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##
from Products.XWFCore.XWFUtils import deprecated
deprecated(context, script, "Use Products.GSGroupMember instead.")

users = []
site_object = context.site_root()
group_object = context.Scripts.get.group_object()

for user_id in group_object.users_with_local_role('GroupAdmin'):
    user = site_object.acl_users.getUser(user_id)
    users.append(user)

return users
