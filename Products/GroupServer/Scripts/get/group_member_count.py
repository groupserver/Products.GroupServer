## Script (Python) "group_member_count"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=group_object=None
##title=
##
from Products.XWFCore.XWFUtils import deprecated
deprecated(context, script, "Use Products.GSGroupMember instead.")
users = []
site_object = context.site_root()
group_object = group_object or context.Scripts.get.group_object()

count = 0
# Count the number of members in the online group, but do not
#   worry if there is no user-group corresponding to the online
#   group.
try:
    group = site_object.acl_users.getGroupById('%s_member' % group_object.getId())
    user_ids = group.getUsers()
    count += len(user_ids)
except:
    pass

return count
