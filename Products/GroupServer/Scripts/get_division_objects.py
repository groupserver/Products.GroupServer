## Script (Python) "get_division_objects"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##
site_root = context.site_root()

user = context.REQUEST.AUTHENTICATED_USER

# if the user is an unverified member, they don't officially belong
# to anything other than the unverified division until they
# confirm their registration
if user and 'unverified_member' in user.getGroups():
    division = getattr(site_root.Content, 'unverified', None)
    if division:
        return [division]
    return []

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