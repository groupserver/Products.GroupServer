## Script (Python) "user_exists"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=user_id
##title=
##
from Products.XWFCore.XWFUtils import deprecated
deprecated(context, script, "Use Products.GSProfile.userInfo instead.")
site_root = context.site_root()

try:
    user = site_root.acl_users.getUser(user_id)
except:
    return False

if user:
    return True
return False
