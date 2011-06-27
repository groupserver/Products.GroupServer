## Script (Python) "group_templates"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##
from Products.XWFCore.XWFUtils import deprecated
deprecated(context, script, "Use gs.group.home instead.")
site_root = context.site_root()

templates = site_root.Templates.groups
template_ids = []
for object in templates.objectValues(['Folder','Folder (Ordered)']):
    template_ids.append((object.getId(), object.getProperty('title') or object.getId()))

return template_ids
