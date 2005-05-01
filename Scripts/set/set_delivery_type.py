## Script (Python) "set_delivery_type"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=group_id, delivery_type, came_from=''
##title=
##
user = context.REQUEST.AUTHENTICATED_USER

delivery_settings = user.get_deliverySettingsByKey(group_id)
if 'disable' in delivery_type:
    user.set_disableDeliveryByKey(group_id)

    return context.REQUEST.RESPONSE.redirect(came_from)

elif 'disable' not in delivery_type:
    user.set_enableDeliveryByKey(group_id)

if 'topicdigest' in delivery_type:
    user.set_enableDigestByKey(group_id)
elif 'regular' in delivery_type:
    user.set_disableDigestByKey(group_id)

return context.REQUEST.RESPONSE.redirect(came_from)
