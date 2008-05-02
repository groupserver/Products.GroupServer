## Script (Python) "chat"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=group=None
##title=Create a group chat interface
##
# Create a chat interface in a group
#
# ARGUMENTS
#    "group"      The group that chat is added to.
#
# RETURNS
#    Nothing.
#
# SIDE EFFECTS
#    A email-settings area is created in the group.
#
from Products.XWFCore.XWFUtils import add_marker_interfaces

assert group
interfaces = ('Products.XWFChat.interfaces.IGSChat',
              'Products.XWFChat.interfaces.IGSGroupFolder')
add_marker_interfaces(group, interfaces)
