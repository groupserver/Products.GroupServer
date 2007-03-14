## Script (Python) "members_area"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=group=None
##title=Create a memebers-area
##
# Create a members-area in a group
#
# ARGUMENTS
#    "group"      The group that the messages area is added to.
#
# RETURNS
#    Nothing.
#
# SIDE EFFECTS
#    A messages-area is created in the group.
#
assert group
site_root = context.site_root()
assert hasattr(site_root.CodeTemplates.group, 'members'), \
  'No "members" folder in CodeTemplates/group'

members = getattr(site_root.CodeTemplates.group, 'members')
group.manage_clone(members, 'members')
assert group.members, '"%s/members" not created' % group.getId()
if hasattr(group.members, 'index.xml'):
    group.members.manage_delObjects(['index.xml'])
interfaces =  ('Products.GSContent.interfaces.IGSContentFolder',)
context.add_marker_interfaces(group.members, interfaces)
