## Script (Python) "group_by_id"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=group_id
##title=
##
#
# This is a Manager level script, designed to be run with elevated
# priviledges. Do not allow to be run as a non-Manager user.
#
from Products.XWFCore.XWFUtils import deprecated
deprecated(context, script, "Use Products.GSGroup.groupInfo instead.")

divisions = context.Scripts.get_unrestricted_division_objects()
group = None
for division in divisions:
    groups = getattr(division, 'groups', None)
    if groups and getattr(groups, 'is_groups', None):
        group = getattr(groups, group_id, None)
        if group and getattr(group, 'is_group', None):
            return group

return group
