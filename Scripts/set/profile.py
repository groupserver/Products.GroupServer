## Script (Python) "profile"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=user_id=None, came_from=None
##title=
##
import cgi
site_root = context.site_root()
request = context.REQUEST
if user_id:
    user = site_root.acl_users.getUser(user_id)
else:
    user = context.REQUEST.AUTHENTICATED_USER

for key in request.form.keys():
    prop = getattr(context.UserProperties, key, None)
    if prop and user.hasProperty(prop.getId()):
        text = cgi.escape(request.form[key])
        user.manage_changeProperties({key:text})
    elif prop:
        user.manage_addProperty(prop.getId(), request.form[key], prop.getProperty('property_type'))


return context.REQUEST.RESPONSE.redirect('%s?message=Your profile was updated successfully' % came_from)
