## Script (Python) "image"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=file_image=None, came_from='', submit_remove=None
##title=Set Image
##
user = context.REQUEST.AUTHENTICATED_USER

origimage = getattr(context.contactsimages, '%s.jpg' % user.getId(), None)

if submit_remove and origimage:
    context.contactsimages.manage_delObjects([origimage.getId()])
    return context.REQUEST.RESPONSE.redirect('%s?mid=1047' % came_from)

try:
    try:
        context.contactsimages.manage_delObjects(['%s.jpg_temp' % user.getId()])
    except:
        pass
    context.contactsimages.manage_addImage('%s.jpg_temp' % user.getId(), file_image, '%s %s' % (user.getProperty('preferredName', ''), user.getProperty('lastName', '')))
    image = getattr(context.contactsimages, '%s.jpg_temp' % user.getId())
    if image.content_type != 'image/jpeg' or image.width > 150 or image.height > 200:
        raise
    
    if origimage:
        context.contactsimages.manage_delObjects([origimage.getId()])
    context.contactsimages.manage_addImage('%s.jpg' % user.getId(), file_image, '%s %s' % (user.getProperty('preferredName', ''), user.getProperty('lastName', '')))
    context.contactsimages.manage_delObjects([image.getId()])
except:
    try:
        context.contactsimages.manage_delObjects(['%s.jpg_temp' % image.getId()])
    except:
        pass
    return context.REQUEST.RESPONSE.redirect('%s?mid=1046' % (came_from))

return context.REQUEST.RESPONSE.redirect('%s?mid=1045' % came_from)

