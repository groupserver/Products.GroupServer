## Script (Python) "default_administrator"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=group=None,mailhost='',siteId=''
##title=Create a Defaulty Administrator
##
# Make the current user the default administrator for the group
#
# ARGUMENTS
#    "group"      The group that user will administer.
#
# RETURNS
#    Nothing
#
# SIDE EFFECTS
#    The current user is added to the group, and is made the group 
#    administrator.
#
assert group

user = context.REQUEST.AUTHENTICATED_USER
assert user
user.add_groupWithNotification('%s_member' % group.getId())
group.manage_addLocalRoles(user.getId(), ['GroupAdmin'])

