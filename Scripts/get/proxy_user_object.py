## Script (Python) "proxy_user_object"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=user_id
##title=
##
site_root = context.site_root

user = getattr(site_root.contacts, user_id)
return user

proxy_properties = context.proxy_properties
proxy_properties.manage_addProperty('preferredEmailAddresses', user.get_preferredEmailAddresses(), 'lines')
#proxy_properties.manage_addProperty('biography', user.getProperty('biography'), 'string')

return proxy_properties
