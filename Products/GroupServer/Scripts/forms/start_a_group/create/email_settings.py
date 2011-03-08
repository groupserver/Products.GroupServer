## Script (Python) "email_settings"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=group=None
##title=Create an email settings area
##
# Create a email-settings area in a group
#
# ARGUMENTS
#    "group"      The group that the email-settings area is added to.
#
# RETURNS
#    Nothing.
#
# SIDE EFFECTS
#    A email-settings area is created in the group. The securty of the
#    group is set so only the members of the group can see the email
#    settings.
#
from Products.XWFCore.XWFUtils import add_marker_interfaces

assert group
site_root = context.site_root()
assert hasattr(site_root.CodeTemplates.group, 'email_settings'), \
  'No "email_settings" folder in "CodeTemplates/group"'

emailSettings = getattr(site_root.CodeTemplates.group, 'email_settings')
group.manage_clone(emailSettings, 'email_settings')
assert hasattr(group.aq_explicit, 'email_settings'), \
  '"%s/email_settings" not created' % group.getId()

interfaces =  ('Products.GSContent.interfaces.IGSContentFolder',)
add_marker_interfaces(group.email_settings, interfaces)

# Only group members can see the email settings.
justUsers = ['GroupAdmin','GroupMember','Manager', 'Owner']
group.email_settings.manage_permission('View', justUsers)
group.email_settings.manage_permission('Access contents information',
                                       justUsers)
