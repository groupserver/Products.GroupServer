## Script (Python) "request_contact"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=Request Contact from User
##

result = {}

form = context.REQUEST.form
assert form.has_key('contactedUser')
assert form.has_key('site')
result['form'] = form

for field in form:
    try:
        form[field] = form[field].strip()
    except AttributeError:
        pass


site_root = context.site_root()
division_object = context.Scripts.get.division_object() #?
user = site_root.acl_users.getUser(form['contactedUser'])

email_addresses = user.get_defaultDeliveryEmailAddresses()
if email_addresses:
    n_dict = {'requesting_user': context.REQUEST.AUTHENTICATED_USER,
              'site': form['site']}
    user.send_notification('request_contact',
                           'default',
                           n_dict=n_dict,
                           email_only=email_addresses)

result['error'] = False
result['message'] = '''The contact request has been sent.'''

return result

# url = '/%s/contacts/%s?mid=1040' % (division_object.getId(), user_id)
# return context.REQUEST.RESPONSE.redirect(url)
