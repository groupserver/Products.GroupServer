## Script (Python) "group_files_visibility"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##
from Products.XWFCore.XWFUtils import deprecated
deprecated(context, script, "Use Zope permissions instead.")
group_object = context.Scripts.get.group_object()
files_object = getattr(group_object, 'files', None)

if not files_object:
    return 'nobody'

view_roles = filter(None, map(lambda x: x['selected'] and x['name'] or None, files_object.rolesOfPermission('View')))

if 'Anonymous' in view_roles and 'Authenticated' in view_roles:
    return 'anyone'
elif 'DivisionMember' in view_roles:
    return 'division'
elif 'GroupMember' in view_roles:
    return 'group'

return 'default'
