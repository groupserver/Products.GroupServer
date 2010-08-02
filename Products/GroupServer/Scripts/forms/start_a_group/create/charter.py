## Script (Python) "charter"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=group,templateId
##title=Create a charter for a group
##
# Create a charter in a group
#
# ARGUMENTS
#    "group"          The group that the charter is added to.
#    "templateId"     String containing the template ID.
#
# RETURNS
#    Nothing.
#
# SIDE EFFECTS
#    A charter is created in the group.
#
from Products.XWFCore.XWFUtils import add_marker_interfaces

assert group
assert templateId
site_root = context.site_root()
assert(hasattr(site_root.Templates.groups, templateId)), \
  'Template "%s" not found in "Templates/groups"' % templateId

templatedir = getattr(site_root.Templates.groups, templateId)
if hasattr(templatedir, 'charter'):
    assert hasattr(site_root.CodeTemplates.group, 'charter'), \
      'No "charter" folder in "CodeTemplates/group"'
    charter = getattr(site_root.CodeTemplates.group, 'charter')
    group.manage_clone(charter, 'charter')
    assert group.charter.aq_explicit, '%s/charter not created' % group.getId()
    if hasattr(group.charter.aq_explicit, 'index.xml'):
        group.charter.manage_delObjects(['index.xml'])
    interfaces =  ('Products.GSContent.interfaces.IGSContentFolder',)
    add_marker_interfaces(group.charter, interfaces)
