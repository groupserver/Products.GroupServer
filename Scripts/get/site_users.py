## Script (Python) "site_users"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##
site_root = context.site_root()

return site_root.acl_users.getUsers()
