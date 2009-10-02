## Script (Python) "group_blocked_members"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##
site_object = context.site_root()
group_object = context.Scripts.get.group_object()

userids = context.list_property(group_object.getId(), 'blocked_members', [])
users = []
for userid in userids:
    user = site_object.acl_users.getUser(userid)
    if user: users.append(user)

return users
