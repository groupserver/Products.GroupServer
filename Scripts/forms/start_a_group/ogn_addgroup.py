## Script (Python) "ogn_addgroup"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=siteId='',templateId='',groupId='',groupName='',realLifeGroup='',privacy=''
##title=OnlineGroups.Net Add Group - Deprecated
##
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
container.create.group_index(group)
container.create.files_area(group)
container.create.messages_area(group)
container.create.charter(group, templateId)
container.create.members_area(group)
container.create.email_settings(group)
container.create.administration(group)
if templateId == 'standard':
    container.create.chat(group)
groupList = container.create.list_instance(group, 'onlinegroups.net', siteId,
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
# Set the rest to default, following the group.
group.files.manage_permission('View', [], 1)
group.files.manage_permission('Access contents information', [], 1)
group.messages.manage_permission('View', [], 1)
group.messages.manage_permission('Access contents information', [], 1)
# Add the "mailinlist_members" script to the mailing list object, if we
#    are creating an announcement group.
if templateId == 'announcement':
    assert(hasattr(context.CodeTemplates.ListManager, 
           'mailinlist_members')), "No 'mailinlist_members' in CodeTemplates."
    groupList.manage_clone(getattr(context.CodeTemplates.ListManager, 
                                   'mailinlist_members'),
                           'mailinlist_members') 
    user = context.REQUEST.AUTHENTICATED_USER
    groupList.manage_addProperty('posting_members', user.getId(), 'lines')
    
return group
