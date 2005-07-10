## Script (Python) "list_property"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=group_id, group_property, default=None
##title=
##
site_root = context.site_root()
listManager = site_root.objectValues('XWF Mailing List Manager')[0]
group = getattr(listManager.aq_explicit, group_id)

val = group.getProperty(group_property, None)
if not val:
    val = listManager.getProperty(group_property, default)

return val
