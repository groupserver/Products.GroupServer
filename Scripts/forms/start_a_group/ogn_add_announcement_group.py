## Script (Python) "ogn_add_announcement_group"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=siteId='',templateId='',groupId='',groupName='',realLifeGroup='',privacy=''
##title=OnlineGroups.Net Add Announcement Group
##
from Products.XWFCore.XWFUtils import getOption

assert siteId != '', 'No site ID set'
assert templateId != '', 'No template ID set'
assert groupId != '', 'No group ID set'
assert groupName != '', 'No group name set'
assert realLifeGroup != '', 'No realLifeGroup set'
assert privacy in ('public', 'private'),\
  'Privacy must be "public" or "private"'

site_root = context.site_root()
assert hasattr(site_root.Content, siteId), 'No site with ID %s found' % siteId
site = getattr(site_root.Content, siteId)
groups = getattr(site, 'groups')
assert not hasattr(groups, groupId), 'The group "%s" already exists'

group = container.create.group_folder(groups, groupId, groupName,
                                       realLifeGroup, templateId)

# Create everything except a members area and chat
container.create.group_index(group)
container.create.javascript(group)
container.create.files_area(group)
container.create.messages_area(group)
container.create.charter(group, templateId)
container.create.email_settings(group)
container.create.administration(group)


canonicalHost = getOption(site, 'canonicalHost', 'onlinegroups.net')
if ('onlinegroups.net' in canonicalHost):
    mailHost = 'onlinegroups.net'
else:
    mailHost = canonicalHost
groupList = container.create.list_instance(group, mailHost, siteId,
  privacy)
container.create.default_administrator(group)

# Set the permissions for the group.
if privacy == 'private':
    joinCondition = 'apply'
    userGroups = ['DivisionAdmin', 'GroupAdmin', 'GroupMember',
                  'Manager', 'Owner']
elif privacy == 'public':
    joinCondition = 'anyone'
    userGroups = ['Anonymous', 'Authenticated', 'DivisionMember',
                  'DivisionAdmin', 'GroupAdmin','GroupMember','Manager',
                  'Owner']

group.manage_changeProperties(join_condition=joinCondition)
group.manage_permission('View', userGroups)
group.manage_permission('Access contents information', userGroups)

# Set the messages and files to default, following the group.
group.files.manage_permission('View', [], 1)
group.files.manage_permission('Access contents information', [], 1)
group.messages.manage_permission('View', [], 1)
group.messages.manage_permission('Access contents information', [], 1)

# Set the administration interface to site and group admins only
adminGroups = ['DivisionAdmin', 'GroupAdmin', 'Manager', 'Owner']
group.admingroup.manage_permission('View', adminGroups)
group.admingroup.manage_permission('Access contents information', adminGroups)

# Add the "mailinlist_members" script to the mailing list object
assert(hasattr(context.CodeTemplates.ListManager, 
        'mailinlist_members')), "No 'mailinlist_members' in CodeTemplates."
groupList.manage_clone(getattr(context.CodeTemplates.ListManager, 
                                'mailinlist_members'),
                        'mailinlist_members') 
user = context.REQUEST.AUTHENTICATED_USER
groupList.manage_addProperty('posting_members', user.getId(), 'lines')

# Add the start date to the group
group.manage_addProperty('date_open', str(DateTime().day())+' '+str(DateTime().Month())+' '+str(DateTime().year()), 'string')

# Add the "replyto" property to the mailing list object
# with a value of "sender" so that replies do not go to the list
groupList.manage_addProperty('replyto', 'sender', 'string')

return group

