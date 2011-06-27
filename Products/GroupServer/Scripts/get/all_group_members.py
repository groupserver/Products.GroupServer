## Script (Python) "all_group_members"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=All members of a group, including unverified
##
from Products.XWFCore.XWFUtils import deprecated
deprecated(context, script, "Products.GSGroupMember.groupmembership instead.")
from Products.GSGroupMember.groupmembership import get_group_users

def sorter(a,b):
    if a.getProperty('fn', '').lower() > b.getProperty('fn', '').lower():
        return 1
    else:
        return -1

group_object = context.Scripts.get.group_object()

retval = get_group_users(context, group_object.getId())

retval.sort(sorter)

return retval
