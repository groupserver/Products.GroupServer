## Script (Python) "change"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=Change Group Email Addresses
##

#--=mpj17=-- Based on the forms/specific_delivery/start_delivery.py
#  and forms/specific_delivery/stop_delivery.py scripts.

result = {}

form = context.REQUEST.form
assert form.has_key('group_id'), 'No group_id in form'
assert form.has_key('group_title'), 'No group_title in form'
assert form.has_key('emailAddressDelivery'), 'No emailAddressDelivery'\
  'in form'
assert form.has_key('emailAddresses'), 'No emailAddresses in form'
result['form'] = form
user =  context.REQUEST.AUTHENTICATED_USER
for field in form:
    try:
        form[field] = form[field].strip()
    except AttributeError:
        pass

group_id = form.get('group_id')
assert group_id != '', 'group_id is empty'
group_title = form.get('group_title')
assert group_id != '', 'site_id is empty'
user = context.REQUEST.AUTHENTICATED_USER
assert user != None, 'user is %s' % user
email_addressess_delivery = form.get('emailAddressDelivery')
assert email_addressess_delivery in 'sd', 'email_address_delivery is %s,'\
  'not "s" or "d"' % email_addressess_delivery
email_addresses = form.get('emailAddresses')

# crude, really crude, way of telling if we're a list
try:
    email_addresses.append
except:
    email_addresses = [email_addresses]

if email_addressess_delivery == 's':
    # Specific address delivery
    for address in user.get_specificEmailAddressesByKey(group_id):
        user.remove_deliveryEmailAddressByKey(group_id, address)
    for address in email_addresses:
        user.add_deliveryEmailAddressByKey(group_id, address)
    e = email_addresses
else:
    # Default Delivery: We have default delivery when there is no
    #   specific email addreesses set.
    for address in user.get_deliveryEmailAddressesByKey(group_id):
        user.remove_deliveryEmailAddressByKey(group_id, address)

    e = user.get_defaultDeliveryEmailAddresses()
    
if len(e) == 1:
    addressesAsText = 'address %s' % email_addresses[0]
else:
    addressesAsText = 'addresses %s and %s' % (', '.join(e[:-1]),
                                               e[-1])
if email_addressess_delivery == 's':
    result['message'] = '''<paragraph>Messages from %s will be
    delivered to the specific email %s.</paragraph>''' % (group_title,
                                                          addressesAsText)
else:
    result['message'] = '''<paragraph>Messages from %s will be
    delivered to the default email %s.</paragraph>''' % (group_title,
                                                          addressesAsText)
result['error'] = False

return result

