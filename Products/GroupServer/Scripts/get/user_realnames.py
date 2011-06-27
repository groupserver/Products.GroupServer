## Script (Python) "user_realnames"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=user_id, preferred_name_only=1
##title=
##
#
# Previously took a preferred_name_only parameter, defaulting to 0,
# Now the behaviour is to lways return preferred name, so this parameter
# exists, but defaults to 1, and is meaningless :)
#
from Products.XWFCore.XWFUtils import deprecated
deprecated(context, script, "Use Products.GSProfile.userInfo instead.")
site_root = context.site_root()

try:
    user = site_root.acl_users.getUser(user_id)
except:
    user = None

if user:
    return '%s' % (user.getProperty('fn'))

return '%s (account removed)' % user_id
