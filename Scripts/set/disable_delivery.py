## Script (Python) "disable_delivery"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=group_id
##title=
##
user = context.REQUEST.AUTHENTICATED_USER

user.set_disableDeliveryByKey(group_id)

return context.REQUEST.RESPONSE.redirect(context.REQUEST.SESSION['last_url'])
