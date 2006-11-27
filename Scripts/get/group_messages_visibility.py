## Script (Python) "group_messages_visibility"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##

#####################
### W A R N I N G ###
#####################
#
# Multiple returns below
#

group_object = context.Scripts.get.group_object()
messages_object = getattr(group_object, 'messages', None)

if not messages_object:
    return 'nobody'

view_roles = filter(None, map(lambda x: x['selected'] and x['name'] or None,
                              messages_object.rolesOfPermission('View')))

if 'Anonymous' in view_roles and 'Authenticated' in view_roles:
    return 'anyone'
elif 'DivisionMember' in view_roles:
    return 'division'
elif 'GroupMember' in view_roles:
    return 'group'

view_roles = filter(None, map(lambda x: x['selected'] and x['name'] or None,
                              group_object.rolesOfPermission('View')))

if 'Anonymous' in view_roles and 'Authenticated' in view_roles:
    return 'anyone'
elif 'DivisionMember' in view_roles:
    return 'division'
elif 'GroupMember' in view_roles:
    return 'group'

return 'default'
