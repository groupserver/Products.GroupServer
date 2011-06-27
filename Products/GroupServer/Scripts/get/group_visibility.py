## Script (Python) "group_visibility"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##
from Products.XWFCore.XWFUtils import deprecated
deprecated(context, script, "Use gs.group.privacy instead.")
group_object = context.Scripts.get.group_object()

view_roles = filter(None, map(lambda x: x['selected'] and x['name'] or None, group_object.rolesOfPermission('View')))

if 'Anonymous' in view_roles and 'Authenticated' in view_roles:
    retval = 'anyone'
elif 'DivisionMember' in view_roles:
    retval = 'division'
elif 'GroupMember' in view_roles:
    retval = 'group'
    
assert retval, 'Could not establish permissions for group %s' % group_object.getId()

return retval
