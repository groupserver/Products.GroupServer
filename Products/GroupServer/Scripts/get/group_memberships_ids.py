## Script (Python) "group_memberships_ids"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=groups_object=None, gtype=None, user_id=None
##title=
##
from Products.XWFCore.XWFUtils import deprecated
deprecated(context, script, "Use Products.GSGroupMember instead.")
if not groups_object:
    groups_object = context.Scripts.get.groups_object()
    
memberships = context.group_memberships(groups_object, user_id)
if gtype:
    memberships = memberships.get(gtype, [])
else:
    m = []
    for gtype in memberships:
        m += memberships.get(gtype, [])
    memberships = m

group_title_ids = []
for membership in memberships:
    group_title_ids.append((membership.getProperty('title'), membership.getId(), membership.absolute_url(1)))

return group_title_ids
