 ## Script (Python) "ogn_addgroup"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=divisionId='',groupId='',groupName='',realLifeGroup='',privacy=''
##title=OnlineGroups.Net Add Group
##
from Products.XWFCore.XWFUtils import assign_ownership

# --=mpj17=-- Non-Standard Script for OGN
#
# AddGroup for OnlineGroups.Net. This is essentially the same as
#   addgroup.py, except the mailto address is not set by the user, but
#   it is constructed from the group ID. This script is designed to
#   work with input that has been verified to be correct: all error
#   checking is done with assert statements.

assert divisionId != ''
assert groupId != ''
assert groupName != ''
assert realLifeGroup != ''
assert privacy in ('public', 'private')

# the group needs to be 'owned' by a top level user, since the Scripts are
# above the context of the site, and some of them require Manager level
# proxy access. Yes, this is darker magic than we'd like. Any suggestions
# welcome.
owner = 'admin'

site_root = context.site_root()
division = context.Scripts.get.division_object()
groups = getattr(division, 'groups')
assert not hasattr(groups, groupId)

templateId = 'standard'
assert(hasattr(site_root.Templates.groups, templateId))
templatedir = getattr(site_root.Templates.groups, templateId)
assert(hasattr(templatedir, 'home'))
create_charter = hasattr(templatedir, 'charter')

# Create the group folder, with the right properties set.
groups.manage_addFolder(groupId)
group = getattr(groups.aq_explicit, groupId)
group.manage_addProperty('is_group', True, 'boolean')
group.manage_addProperty('short_name', groupName.lower(), 'string')
group.manage_addProperty('real_life_group', realLifeGroup, 'string')
group.manage_changeProperties(title=groupName)

# add a files area
group.manage_addProduct['XWFFileLibrary2'].manage_addXWFVirtualFileFolder2('files',
                                                                           'files')

# add a messages area
group.manage_addProduct['XWFMailingListManager'].manage_addXWFVirtualMailingListArchive('messages',
                                                                                        'messages')
group.messages.manage_changeProperties(xwf_mailing_list_manager_path='ListManager',
                                       xwf_mailing_list_ids=[groupId])

if templateId:
    group.manage_clone(getattr(context.CodeTemplates.group, 'index.xml'),
                       'index.xml')
    group.manage_addProperty('group_template', templateId, 'string')
    if create_charter:
        group.manage_addFolder('charter', 'Charter')
        charterIndex = getattr(context.CodeTemplates.group.charter,
                               'index.xml')
        group.charter.manage_clone(charterIndex, 'index.xml')
        
# create a members folder
group.manage_addFolder('members', 'Members')
membersIndex = getattr(context.CodeTemplates.group.members, 'index.xml')
group.members.manage_clone(membersIndex, 'index.xml')

# create a email settings folder
group.manage_addFolder('email_settings', 'Email Settings')
emailSettings = getattr(site_root.CodeTemplates.group.email_settings,
                        'index.xml')
group.email_settings.manage_clone(emailSettings, 'index.xml')

# secure the group
site_root.acl_users.userFolderAddGroup('%s_member' % groupId)
group.manage_defined_roles('Add Role', {'role':'GroupMember'})
group.manage_defined_roles('Add Role', {'role':'GroupAdmin'})
group.manage_addLocalGroupRoles('%s_member' % groupId, ['GroupMember'])

# Set the privacy permissions
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
assign_ownership(group, 'admin', 1, '/acl_users')
# The email settings should be different: only group members can see
#   them.
justUsers = ['GroupAdmin','GroupMember','Manager', 'Owner']
group.email_settings.manage_permission('View', justUsers)
group.email_settings.manage_permission('Access contents information',
                                       justUsers)

mailto = '%s@onlinegroups.net' % groupId
site_root.ListManager.manage_addProduct['XWFMailingListManager'].manage_addXWFMailingList(groupId,
                                                                                          mailto, groupName.lower())
groupList = getattr(site_root.ListManager, group.getId())
assert groupList
groupList.manage_addProperty('siteId', division.getId(), 'string')


user = context.REQUEST.AUTHENTICATED_USER
user.add_groupWithNotification('%s_member' % groupId)

groupPage = '/groups/%s' % groupId
context.REQUEST.RESPONSE.redirect(groupPage)

# The following should not be reached
return 'The group &#8220;%s&#8221; has been created.' % groupName
