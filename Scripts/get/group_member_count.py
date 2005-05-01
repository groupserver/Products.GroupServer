## Script (Python) "group_member_count"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=group_object=None
##title=
##
users = []
site_object = context.site_root()
group_object = group_object or context.Scripts.get.group_object()

count = 0
for group_id in group_object.groups_with_local_role('GroupMember'):
    group = site_object.acl_users.getGroupById(group_id)
    user_ids = group.getUsers()
    count += len(user_ids)

return count
