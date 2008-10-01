## Script (Python) "groups"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##
from Products.XWFCore.XWFUtils import deprecated
deprecated(context, script)

from Products.GSContent.groupsInfo import GSGroupsInfo

visible_groups = GSGroupsInfo(context).get_visible_groups() or []

return visible_groups
