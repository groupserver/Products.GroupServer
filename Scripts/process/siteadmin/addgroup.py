## Script (Python) "addgroup"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##
from Products.XWFCore.XWFUtils import assign_ownership

# the group needs to be 'owned' by a top level user, since the Scripts are
# above the context of the site, and some of them require Manager level
# proxy access. Yes, this is darker magic than we'd like. Any suggestions
# welcome.
owner = 'admin'

form = context.REQUEST.form
site_root = context.site_root()
division = context.Scripts.get.division_object()
groups = getattr(division, 'groups')

message = []
error = 0

submit = form.get('__submit__', '')
if not submit:
    return ''

groupid = form.get('groupid', '').strip().lower()
title = form.get('title', '').strip().lower() or groupid
mailto = form.get('mailto','').strip().lower()
templateid = form.get('templateid','').strip().lower()

divisionid = form.get('divisionid')

if hasattr(groups.aq_explicit, groupid):
    message.append('<paragraph>Unfortunately group ID %s already exists. Please choose another ID for your group.</paragraph>' % groupid)
    error = 1

if groupid == divisionid:
    message.append('<paragraph>Unfortunately you may not have a group with the same ID as the division ID. Please choose another ID for your group.</paragraph>' % groupid)
    error = 1

try:
    site_root.acl_users.getGroupById('%s_member' % groupid)
    message.append('<paragraph>Unfortunately a group corresponding to %s already exists. Please choose another ID for your group.</paragraph>' % groupid)
    error = 1
except KeyError:
    pass

if not title:
    message.append('<paragraph>The group title is required, but was not specified.</paragraph>')
    error = 1

if not groupid:
    message.append('<paragraph>The group ID is required, but was not specified.</paragraph>')
    error = 1

if not mailto:
    message.append('<paragraph>The email address is required, but not specified.</paragraph>')
    error = 1
elif not (mailto.find('@') > 1):
    message.append('<paragraph>%s is not a valid email address.</paragraph>' % mailto)
    error = 1

create_charter = 0
if templateid and not hasattr(site_root.Templates.groups, templateid):
    message.append('<paragraph>%s does not exist as a template.</paragraph>' % templateid)
elif templateid:
    templatedir = getattr(site_root.Templates.groups, templateid)
    if hasattr(templatedir, 'charter'):
        create_charter = 1
    if not hasattr(templatedir, 'home'):
        message.append('<paragraph>Selected template %s does not have a home page template, which is necessary.</paragraph>')
        error = 1

if error:
    return '\n'.join(message)

groups.manage_addFolder(groupid)
group = getattr(groups.aq_explicit, groupid)

group.manage_addProperty('is_group', True, 'boolean')
group.manage_addProperty('short_name', title, 'string')
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

site_root.ListManager.manage_addProduct['XWFMailingListManager'].manage_addXWFMailingList(groupid, mailto, title)

message.append('<paragraph>Please ask your server administrator to add a mail server mapping for %s</paragraph>' % groupid)

return '\n'.join(message)
