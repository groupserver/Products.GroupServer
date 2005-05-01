## Script (Python) "get_unrestricted_division_objects"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##
site_root = context.site_root()
objects = []
for object_id in site_root.Content.objectIds(('Folder', 'Folder (Ordered)')):
    object = site_root.Content.restrictedTraverse(object_id, None)
    if object:
        try:
            if object.getProperty('is_division', 0):
                objects.append(object)
        except:
            pass
return objects
