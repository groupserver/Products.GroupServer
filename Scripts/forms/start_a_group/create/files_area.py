## Script (Python) "files_area"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=group=None
##title=Create a files-area
##
# Create a files-agrea in a group
#
# ARGUMENTS
#    "group"      The group that the files area is added to.
#
# RETURNS
#    Nothing.
#
# SIDE EFFECTS
#    A files-area is created in the group.
#
assert group

xwffiles = group.manage_addProduct['XWFFileLibrary2']
xwffiles.manage_addXWFVirtualFileFolder2('files', 'files')

assert hasattr(group.aq_explicit, 'files'), \
  'Files area not added to "%s"' % group.getId()
