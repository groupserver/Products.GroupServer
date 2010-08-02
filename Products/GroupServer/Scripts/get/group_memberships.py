## Script (Python) "group_memberships"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=groups_object, user_id=None
##title=
##
group_object = {}
user = user_id and groups_object.acl_users.getUser(user_id) or context.REQUEST.AUTHENTICATED_USER
objects = context.Scripts.get.object_values(groups_object, ['Folder'])
for object in objects:
    if object and 'GroupMember' in user.getRolesInContext(object):
        group_template = object.getProperty('group_template', 'unknown')
        group_object.setdefault(group_template, []).append(object)

return group_object
