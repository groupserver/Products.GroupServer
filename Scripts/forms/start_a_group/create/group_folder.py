## Script (Python) "group_folder"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=groups,groupId,groupName,realLifeGroup,templateId
##title=Create the group folder
##
# Create the group folder, with the right properties set.
#
# ARGUMENTS
#    "groups"         Groups object that the new group folder is added to.
#    "groupId"        ID of the group folder to add. Each group in "groups"
#                     must be unique.
#    "groupName"      The name of the group, as a string.
#    "realLifeGroup"  String describing the group membership.
#    "templateId"     String containing the template ID.
#
# RETURNS
#    The new group-folder instance.
#
# SIDE EFFECTS
#    A group-folder is created in the "groups" folder
#
import Products.XWFCore.XWFUtils
site_root = context.site_root()

assert not(hasattr(groups.aq_explicit, groupId)), \
  'Group "%s" exists' % groupId
# Check the template
assert(hasattr(site_root.Templates.groups, templateId)), \
  'Template "%s" not found in "Templates/groups"' % templateId
templatedir = getattr(site_root.Templates.groups, templateId)
assert(hasattr(templatedir, 'home')), \
  'No "home" in "Templates/groups/%s"' % templateId

# Create the group folder
groups.manage_addFolder(groupId)
assert hasattr(groups.aq_explicit, groupId),\
  'Could not create folder for "%s" in "groups"' % groupId
group = getattr(groups.aq_explicit, groupId)

# Secure the group
site_root.acl_users.userFolderAddGroup('%s_member' % groupId)
group.manage_defined_roles('Add Role', {'role':'GroupMember'})
group.manage_defined_roles('Add Role', {'role':'GroupAdmin'})
group.manage_addLocalGroupRoles('%s_member' % groupId, ['GroupMember'])

# Set the correct properties
group.manage_addProperty('is_group', True, 'boolean')
group.manage_addProperty('short_name', groupName.lower(), 'string')
group.manage_addProperty('real_life_group', realLifeGroup, 'string')
group.manage_addProperty('group_template', templateId, 'string')
group.manage_changeProperties(title=groupName)

return group
