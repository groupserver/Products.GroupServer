## Script (Python) "site_users"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##
from Products.XWFCore.XWFUtils import deprecated
deprecated(context, script, "Use site_root.acl_users.getUsers() instead.")
site_root = context.site_root()

return site_root.acl_users.getUsers()

