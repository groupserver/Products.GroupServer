## Script (Python) "get_unverified_members"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=Get Unverified Members
##
from Products.GSGroupMember.groupmembership import get_group_users

group_object = context.Scripts.get.group_object()

unverifiedUsersInGroup = []
for user in get_group_users(context, group_object.getId()):
    if len(user.get_verifiedEmailAddresses()) < 1:
        unverifiedUsersInGroup.append(user)

return unverifiedUsersInGroup
