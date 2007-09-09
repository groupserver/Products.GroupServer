## Script (Python) "ogn_add_support_group"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=siteId='',templateId=''
##title=OnlineGroups.Net Add Support Group
##
from Products.XWFCore.XWFUtils import getOption

assert siteId != '', 'No site ID set'
assert templateId != '', 'No template ID set'

site_root = context.site_root()
assert hasattr(site_root.Content, siteId), 'No site with ID %s found' % siteId
site = getattr(site_root.Content, siteId)
groups = getattr(site, 'groups')

groupId = '%s_support' % siteId
groupName = '%s Support' % site.title_or_id()
assert not hasattr(groups, groupId), 'The group "%s" already exists'

realLife = groupName

group = container.create.group_folder(groups, groupId, groupName,
                                       realLife, templateId)

# Add everything except members, chat and charter
container.create.group_index(group)
container.create.javascript(group)
container.create.files_area(group)
container.create.messages_area(group)
container.create.email_settings(group)


canonicalHost = getOption(site, 'canonicalHost', 'onlinegroups.net')
if ('onlinegroups.net' in canonicalHost):
    mailHost = 'onlinegroups.net'
else:
    mailHost = canonicalHost
groupList = container.create.list_instance(group, mailHost, siteId,
  'private')
container.create.administration(group)
container.create.default_administrator(group)

# Set the permissions for the group.
joinCondition = 'invite'
userGroups = ['DivisionAdmin', 'GroupAdmin', 'GroupMember',
                  'Manager', 'Owner']
group.manage_changeProperties(join_condition=joinCondition)
group.manage_permission('View', userGroups)
group.manage_permission('Access contents information', userGroups)

# Set the rest to default, following the group.
group.files.manage_permission('View', [], 1)
group.files.manage_permission('Access contents information', [], 1)
group.messages.manage_permission('View', [], 1)
group.messages.manage_permission('Access contents information', [], 1)

# Remove the "subscribe" property from the group
groupList.manage_delProperties(['subscribe',])

# Add the "unclosed" property to the mailing list object
# to allow anyone to post to the group
groupList.manage_addProperty('unclosed', 1, 'boolean')

# Add the "replyto" property to the mailing list object
# with a value of "sender" so that replies do not go to the list
groupList.manage_addProperty('replyto', 'sender', 'string')

return group
