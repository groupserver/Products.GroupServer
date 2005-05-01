## Script (Python) "user_realnames"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=user_id, preferred_name_only=0
##title=
##
site_root = context.site_root()

try:
    user = site_root.acl_users.getUser(user_id)
except:
    user = None

if user:
    if preferred_name_only:
        return '%s' % (user.getProperty('preferredName'))
    return '%s %s' % (user.getProperty('preferredName'), user.getProperty('lastName'))

return '%s (account removed)' % user_id
