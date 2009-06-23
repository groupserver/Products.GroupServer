## Script (Python) "javascript"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=group=None
##title=Create the group latest-topics javascript
##
# Create a group latest-topics AJAX loader
#
# ARGUMENTS
#    "group"      The group that the index is added to.
#
# RETURNS
#    Nothing.
#
# SIDE EFFECTS
#    A "javascript.xml" in the group-folder is created.
#
assert group
site_root = context.site_root()
assert hasattr(site_root.CodeTemplates.group, 'javascript.xml'), \
  'No "javascript.xml" in "CodeTemplates/group"'

group.manage_clone(getattr(context.CodeTemplates.group, 'javascript.xml'),
                   'javascript.xml')

assert hasattr(group.aq_explicit, 'javascript.xml')

