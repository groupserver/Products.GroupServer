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

return getattr(getattr(listManager, group_id),group_property, default)
