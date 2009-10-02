## Script (Python) "proxy_user_object"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=user_id
##title=
##
site_root = context.site_root()

user = getattr(site_root.contacts, user_id, None)
return user
