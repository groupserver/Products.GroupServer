## Script (Python) "list_instance"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=group=None,mailhost='',siteId='',privacy=''
##title=Create a mailing list instance
##
# Create a mailing list instance for the group
#
# ARGUMENTS
#    "group"      The group that chat is added to.
#    "mailhost"   The mail host for the list.
#    "siteId"     The Web site the group belongs to.
#    "privacy"    The privacy settings for the group: 'public' or 'private'.
#
# RETURNS
#    The mailing-list instance
#
# SIDE EFFECTS
#    A mailing-list is created for the group, with the privacy set 
#    accordingly.
#
assert group
assert mailhost
assert siteId
assert privacy in ('public', 'private')

site_root = context.site_root()
listManager = site_root.ListManager
assert not(hasattr(listManager.aq_explicit, group.getId())), \
    'The ListManager already has a list for "%s".' % group.getId()
mailto = '%s@%s' % (group.getId(), mailhost)
xwfmailingList = listManager.manage_addProduct['XWFMailingListManager']
xwfmailingList.manage_addXWFMailingList(group.getId(), mailto, 
                                        group.title_or_id().lower())
assert hasattr(listManager.aq_explicit, group.getId()), \
    'The list "%s" was not created in ListManager.' % group.getId()

groupList = getattr(site_root.ListManager.aq_explicit, group.getId())
groupList.manage_addProperty('siteId', siteId, 'string')

if privacy == 'public':
    groupList.manage_addProperty('subscribe', 'subscribe', 'string')
else:
    groupList.manage_addProperty('subscribe', '', 'string')

return groupList
