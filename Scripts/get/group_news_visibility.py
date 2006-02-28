## Script (Python) "group_news_visibility"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##
group_object = context.Scripts.get.group_object()
news_object = getattr(group_object, 'news', None)

if not news_object:
    return 'nobody'

view_roles = filter(None, map(lambda x: x['selected'] and x['name'] or None,
	news_object.rolesOfPermission('View')))

if 'Anonymous' in view_roles and 'Authenticated' in view_roles:
    return 'anyone'
elif 'DivisionMember' in view_roles:
    return 'division'
elif 'GroupMember' in view_roles:
    return 'group'

return 'default'
