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
#    * An administration interface is created in the group.
#    * The IGSGroupFolder is added to the group, for the "admin_join*html"
#      pages.
#
from Products.XWFCore.XWFUtils import add_marker_interfaces
from Products.GroupServer.pathutil import get_groupserver_path

assert group
fss = group.manage_addProduct['FileSystemSite']
fss.manage_addDirectoryView(get_groupserver_path('admingroup'))

# Add the IGSGroupFolder, so the Zope Five pages work!
interfaces = ('Products.XWFChat.interfaces.IGSGroupFolder',)
add_marker_interfaces(group, interfaces)
# In an OGN goup, group and site administrators can add users.
group.manage_permission('Manage users', 
                        ['DivisionAdmin','GroupAdmin','Manager','Owner'],0)
# In an OGN goup, only site administrators can alter the properties
group.manage_permission('Manage properties', 
                        ['DivisionAdmin','Manager','Owner'],0)

assert hasattr(group.aq_explicit, 'admingroup')

