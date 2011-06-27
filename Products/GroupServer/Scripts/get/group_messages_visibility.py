## Script (Python) "group_messages_visibility"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##
from Products.XWFCore.XWFUtils import deprecated
deprecated(context, script, "Use gs.group.messages.post instead.")
group_object = context.Scripts.get.group_object()
messages_object = getattr(group_object, 'messages', None)

if not messages_object:
    retval = 'nobody'
else:
    view_roles = filter(None, map(lambda x: x['selected'] and x['name'] or None,
                              messages_object.rolesOfPermission('View')))

    if 'Anonymous' in view_roles and 'Authenticated' in view_roles:
        retval = 'anyone'
    elif 'DivisionMember' in view_roles:
        retval = 'division'
    elif 'GroupMember' in view_roles:
        retval = 'group'
    else:
        retval = context.Scripts.get.group_visibility()

return retval
