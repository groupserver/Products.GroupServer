## Script (Python) "group_joinability"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=division_id=None, group_id=None
##title=
##
if not division_id:
    group_object = context.Scripts.get.group_object()
elif division_id and group_id:
    site_root = context.site_root()
    group_object = getattr(getattr(site_root.Content, division_id).groups, group_id)
else:
    return invite

view_roles = filter(None, map(lambda x: x['selected'] and x['name'] or None, group_object.rolesOfPermission('View')))

subscribe = context.list_property(group_object.getId(), 'subscribe')
if subscribe:
    return 'anyone'

join_condition = group_object.getProperty('join_condition', 'open')
if join_condition == 'apply':
    return 'apply'

return 'invite'
