## Script (Python) "administration"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=group=None
##title=Create Group Administration Interface
##
# Create the group administration interface for the group
#
# ARGUMENTS
#    "group"      The group that the interface area is added to.
#
# RETURNS
#    Nothing.
#
# SIDE EFFECTS
#    An administration interface is created in the group.
#
assert group
fss = group.manage_addProduct['FileSystemSite']
fss.manage_addDirectoryView('GroupServer/admingroup')
assert hasattr(group.aq_explicit, 'admingroup')
