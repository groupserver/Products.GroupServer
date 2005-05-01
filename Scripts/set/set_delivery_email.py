## Script (Python) "set_delivery_email"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=group_id, email, came_from=''
##title=
##
user = context.REQUEST.AUTHENTICATED_USER

user.set_enableDeliveryByKey(group_id)

email = filter(None, email)

for e in email:
    if e.lower() == 'default delivery':
        if user.get_deliverySettingsByKey(group_id) != 1:
            for de in user.get_deliveryEmailAddressesByKey(group_id):
                user.remove_deliveryEmailAddressByKey(group_id, de)
    else:
        user.add_deliveryEmailAddressByKey(group_id, e)

return context.REQUEST.RESPONSE.redirect(came_from)
