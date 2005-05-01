## Script (Python) "group_members"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##
users = []
site_object = context.site_root()
group_object = context.Scripts.get.group_object()

for group_id in group_object.groups_with_local_role('GroupMember'):
    group = site_object.acl_users.getGroupById(group_id)
    user_ids = group.getUsers()
    for user_id in user_ids:
        users.append(site_object.acl_users.getUser(user_id))

return users
