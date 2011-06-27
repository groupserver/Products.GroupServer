## Script (Python) "group_member_count"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=group_ids=[], exclude_groups=['facilitator','abel_member','ecampus_staff', 'enabel_member']
##title=
##
from Products.XWFCore.XWFUtils import deprecated
deprecated(context, script, "Use Products.GSGroupMember instead.")
site_root = context.site_root()

def sorter(a,b):
    if a.getProperty('familyName') > b.getProperty('familyName'):
        return 1
    else:
        return -1

users = []
for group_id in group_ids:
    group = site_root.acl_users.getGroupById(group_id, [])
    if group:
        for user in group.getUsers():
            auser = site_root.acl_users.getUser(user)
            if auser and auser.getGroups() not in exclude_groups:
                users.append(auser)

users.sort(sorter)

return users

