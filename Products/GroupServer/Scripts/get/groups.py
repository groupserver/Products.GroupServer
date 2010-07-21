## Script (Python) "groups"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=groups_context=None
##title=
##
from Products.XWFCore.XWFUtils import deprecated
deprecated(context, script, "Use 'GSGroupsInfo(context).get_visible_groups()' instead")

from gs.groups.groupsInfo import GSGroupsInfo

context = groups_context or context
visible_groups = GSGroupsInfo(context).get_visible_groups() or []

return visible_groups
