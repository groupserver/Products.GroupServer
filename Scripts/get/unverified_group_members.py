## Script (Python) "get_unverified_members"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=Get Unverified Members
##
from Products.PythonScripts.standard import html_quote
from Products.PythonScripts.standard import url_quote

site_object = context.site_root()
group_object = context.Scripts.get.group_object()
gId_member = '%s_member' % group_object.getId()

unverifiedUsersInGroup = []
for user in context.Scripts.get.users_from_groups([gId_member], []):
    if len(user.get_verifiedEmailAddresses()) < 1:
        unverifiedUsersInGroup.append(user)

return unverifiedUsersInGroup
