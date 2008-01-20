## Script (Python) "administration"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=group=None
##title=Create Group Administration Interface for eDem
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
#    An eDem-specific administration interface is created in the group.
#
assert group
site_root = context.site_root()
mainSite = getattr(site_root.Content, 'main')
edemAdminGroup = mainSite.manage_copyObjects(('admingroup',))
group.manage_pasteObjects(edemAdminGroup)
assert hasattr(group.aq_explicit, 'admingroup')
