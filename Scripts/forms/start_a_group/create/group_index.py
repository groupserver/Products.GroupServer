## Script (Python) "group_index"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=group=None
##title=Create the group index folder
##
# Create a group index page
#
# ARGUMENTS
#    "group"      The group that the index is added to.
#
# RETURNS
#    Nothing.
#
# SIDE EFFECTS
#    An index-page for the group is created.
#
assert group
site_root = context.site_root()
assert hasattr(site_root.CodeTemplates.group, 'content_en'), \
  'No "content_en" in "CodeTemplates/group"'

group.manage_clone(getattr(context.CodeTemplates.group, 'content_en'),
                   'content_en')
interfaces =  ('Products.GSContent.interfaces.IGSContentFolder',)
context.add_marker_interfaces(group, interfaces)

assert hasattr(group.aq_explicit, 'content_en')
