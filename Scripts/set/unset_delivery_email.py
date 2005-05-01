## Script (Python) "unset_delivery_email"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=group_id, email
##title=
##
user = context.REQUEST.AUTHENTICATED_USER

email = filter(None, email)

for e in email:
    user.remove_deliveryEmailAddressByKey(group_id, e)

return context.REQUEST.RESPONSE.redirect(context.REQUEST.SESSION['last_url'])
