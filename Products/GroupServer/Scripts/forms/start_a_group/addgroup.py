## Script (Python) "addgroup"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=siteId='',templateId='',groupId='',groupName='',realLifeGroup='',privacy=''
##title=Add Group
##
from Products.XWFCore.XWFUtils import getOption, assign_ownership
from gs.groups.groupsInfo import GSGroupsInfoFactory

assert siteId != '', 'No site ID set'
assert templateId != '', 'No template ID set'
assert groupId != '', 'No group ID set'
assert groupName != '', 'No group name set'
assert realLifeGroup != '', 'No realLifeGroup set'
assert privacy in ('public', 'private', 'secret'),\
  'Privacy must be "public","private" or "secret"'

site_root = context.site_root()
assert hasattr(site_root.Content, siteId), 'No site with ID %s found' % siteId
site = getattr(site_root.Content, siteId)
groups = getattr(site, 'groups')
assert not hasattr(groups, groupId), 'The group "%s" already exists'

group = container.create.group_folder(groups, groupId, groupName,
                                       realLifeGroup, templateId)
container.create.group_index(group)
container.create.javascript(group)
container.create.files_area(group)
container.create.messages_area(group)
container.create.charter(group, templateId)
container.create.email_settings(group)
container.create.administration(group)
if templateId == 'standard':
    container.create.members_area(group)
    container.create.chat(group)

canonicalHost = getOption(site, 'canonicalHost', 'onlinegroups.net')
if ('onlinegroups.net' in canonicalHost):
    mailHost = 'onlinegroups.net'
else:
    mailHost = canonicalHost
groupList = container.create.list_instance(group, mailHost, siteId, privacy)
container.create.default_administrator(group)

# Set the permissions for the group.
everyone = ['Anonymous', 'Authenticated', 'DivisionMember',
              'DivisionAdmin', 'GroupAdmin','GroupMember','Manager',
              'Owner']
grpOnly = ['DivisionAdmin', 'GroupAdmin', 'GroupMember',
              'Manager', 'Owner'] 

if privacy == 'secret':
    joinCondition = 'invite'
    grpVisibility = grpOnly
    msgVisibility = grpOnly
elif privacy == 'private':
    joinCondition = 'apply'
    grpVisibility = everyone
    msgVisibility = grpOnly
elif privacy == 'public':
    joinCondition = 'anyone'
    grpVisibility = everyone
    msgVisibility = everyone

group.manage_addProperty('join_condition', joinCondition, 'string')
group.manage_permission('View', grpVisibility)
group.manage_permission('Access contents information', grpVisibility)
group.messages.manage_permission('View', msgVisibility)
group.messages.manage_permission('Access contents information', msgVisibility)
group.files.manage_permission('View', msgVisibility) # Files follow message settings
group.files.manage_permission('Access contents information', msgVisibility)

# Set the administration interface to site and group admins only
adminGroups = ['DivisionAdmin', 'GroupAdmin', 'Manager', 'Owner']
group.admingroup.manage_permission('View', adminGroups)
group.admingroup.manage_permission('Access contents information', adminGroups)

# Add the start date to the group
group.manage_addProperty('date_open', str(DateTime().day())+' '+str(DateTime().Month())+' '+str(DateTime().year()), 'string')

if templateId == 'announcement':
    # Add the "mailinlist_members" script to the mailing list object
    assert(hasattr(context.CodeTemplates.ListManager, 
            'mailinlist_members')), "No 'mailinlist_members' in CodeTemplates."
    groupList.manage_clone(getattr(context.CodeTemplates.ListManager, 
                                    'mailinlist_members'),
                            'mailinlist_members') 
    user = context.REQUEST.AUTHENTICATED_USER
    groupList.manage_addProperty('posting_members', user.getId(), 'lines')

    # Add the "replyto" property to the mailing list object
    # with a value of "sender" so that replies do not go to the list
    groupList.manage_addProperty('replyto', 'sender', 'string')

# --=rrw=--
#   The group needs to be 'owned' by a top level user, since the Scripts are
#   above the context of the site, and some of them require Manager level
#   proxy access. Yes, this is darker magic than we'd like. Any suggestions
#   welcome.
assign_ownership(group, 'admin', 1, '/acl_users')
assign_ownership(groupList, 'admin', 1, '/acl_users')

groupsInfo = GSGroupsInfoFactory()(site)
groupsInfo.clear_groups_cache()

return group

