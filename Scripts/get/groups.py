## Script (Python) "groups"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=groups_object=None
##title=
##
from Products.GSContent.groupsInfo import GSGroupsInfo

visible_groups = GSGroupsInfo(context).get_visible_groups() or []

groups = []
for group in visible_groups:
    groups.append((group.title_or_id().lower(), group))

return groups
