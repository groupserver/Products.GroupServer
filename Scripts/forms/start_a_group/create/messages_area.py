## Script (Python) "messages_area"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=group=None
##title=Create a messages-area
##
# Create a messages-area in a group
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

# Add a messages area
xwfmail = group.manage_addProduct['XWFMailingListManager']
xwfmail.manage_addXWFVirtualMailingListArchive2('messages', 'messages')

assert group.messages, 'Messages area not added to "s"' % group.getId()

messages = group.messages
messages.manage_changeProperties(xwf_mailing_list_manager_path='ListManager',
                                 xwf_mailing_list_ids=[group.getId()])
