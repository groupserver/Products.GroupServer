## Script (Python) "list_property"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=group_id, group_property, value
##title=
##
site_root = context.site_root()
listManager = site_root.objectValues('XWF Mailing List Manager')[0]
listObject = getattr(listManager, group_id)

# don't set the value if the value is the same
if getattr(listObject, group_property, None) == value:
    return

if listObject.hasProperty(group_property):
    listObject.manage_changeProperties({group_property: value})
else:
    listObject.manage_addProperty(group_property, value, 'string')
