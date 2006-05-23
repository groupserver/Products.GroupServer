## Script (Python) "request_contact"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=user_id=None,site=None
##title=Request Contact from User
##

site_root = context.site_root()
division_object = context.Scripts.get.division_object() #?
user = site_root.acl_users.getUser(user_id)

email_addresses = user.get_defaultDeliveryEmailAddresses()
if email_addresses:
    n_dict = {'requesting_user': context.REQUEST.AUTHENTICATED_USER}
    user.send_notification('request_contact',
                           'default',
                           n_dict=n_dict,
                           email_only=email_addresses)

url = '/%s/contacts/%s?mid=1040' % (division_object.getId(), user_id)
return context.REQUEST.RESPONSE.redirect(url)
