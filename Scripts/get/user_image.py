## Script (Python) "test"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=user_id
##title=
##
site_root = context.site_root()

try:
    user = site_root.acl_users.getUser(user_id)
except:
    user = None

if user:
    return user.get_image()

return ''


user = context.acl_users.getUser(user_id)

imageurl = None
if user and (not user.getProperty('restrictImage', 1)):
    for id in ['%s.jpg' % user_id,'%s.JPG' % user_id]:
        image = getattr(context.contactsimages, id, None)
        if image:
            imageurl = image.absolute_url(1)
            break

return imageurl

