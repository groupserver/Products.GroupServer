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

user = site_root.acl_users.getUser(user_id)

if user:
    return user.get_image()

return ''
