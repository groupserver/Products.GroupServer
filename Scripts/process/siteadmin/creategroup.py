## Script (Python) "creategroup"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=groupid='',title='',mailto='',templateid='',division=None
##title=Create Group
##
from Products.XWFCore.XWFUtils import assign_ownership

site_root = context.site_root()
# <preconditions>
assert title != ''
assert groupid !=''
assert mailto != ''
assert '@' in mailto
assert templateid != ''
assert division != None
assert groupid != division.title_or_id()
assert hasattr(site_root.Templates.groups, templateid)
try:
    site_root.acl_users.getGroupById('%s_member' % groupid)
except KeyError:
    assert False, 'Existing user-group'
# </preconditions>

# the group needs to be 'owned' by a top level user, since the Scripts are
# above the context of the site, and some of them require Manager level
# proxy access. Yes, this is darker magic than we'd like. Any suggestions
# welcome.
owner = 'admin'

# This is wrong
# division = context.Scripts.get.division_object()
groups = getattr(division, 'groups')
assert not hasattr(groups.aq_explicit, groupid)

message = []
error = 0
create_charter = 0

templatedir = getattr(site_root.Templates.groups, templateid)
assert hasattr(templatedir, 'home')
if hasattr(templatedir, 'charter'):
    create_charter = 1

groups.manage_addFolder(groupid)
group = getattr(groups.aq_explicit, groupid)

group.manage_addProperty('is_group', True, 'boolean')
group.manage_addProperty('short_name', title.lower(), 'string')
group.manage_changeProperties(title=title)

# add a files area
group.manage_addProduct['XWFFileLibrary2'].manage_addXWFVirtualFileFolder2('files', 'files')

# add a messages area
group.manage_addProduct['XWFMailingListManager'].manage_addXWFVirtualMailingListArchive('messages', 'messages')
group.messages.manage_changeProperties(xwf_mailing_list_manager_path='ListManager',
                                       xwf_mailing_list_ids=[groupid])

if templateid:
    group.manage_clone(getattr(context.CodeTemplates.group, 'index.xml'), 'index.xml')
    group.manage_addProperty('group_template', templateid, 'string')
    if create_charter:
        group.manage_addFolder('charter', 'Charter')
        group.charter.manage_clone(getattr(context.CodeTemplates.group.charter, 'index.xml'), 'index.xml')

# create a members folder
group.manage_addFolder('members', 'Members')
group.members.manage_clone(getattr(context.CodeTemplates.group.members, 'index.xml'), 'index.xml')

# secure the group
site_root.acl_users.userFolderAddGroup('%s_member' % groupid)
group.manage_defined_roles('Add Role', {'role':'GroupMember'})
group.manage_defined_roles('Add Role', {'role':'GroupAdmin'})
group.manage_addLocalGroupRoles('%s_member' % groupid, ['GroupMember'])
group.manage_permission('View', ['DivisionAdmin','GroupAdmin','GroupMember','Manager'])
group.manage_permission('Access contents information', ['DivisionAdmin','GroupAdmin','GroupMember','Manager'])

assign_ownership(group, 'admin', 1, '/acl_users')

site_root.ListManager.manage_addProduct['XWFMailingListManager'].manage_addXWFMailingList(groupid, mailto, title.lower())

return True
