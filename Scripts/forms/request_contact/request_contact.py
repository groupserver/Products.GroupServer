## Script (Python) "request_contact"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=Request Contact from User
##

from Products.XWFCore.XWFUtils import get_support_email

result = {}

form = context.REQUEST.form
assert form.has_key('contactedUser')
assert form.has_key('site')
assert form.has_key('siteName')
result['form'] = form

for field in form:
    try:
        form[field] = form[field].strip()
    except AttributeError:
        pass

requestingUser = context.REQUEST.AUTHENTICATED_USER
site_root = context.site_root()
site = context.Scripts.get.division_object()
contactedUser = site_root.acl_users.getUser(form['contactedUser'])
canonical = form['site']

email_addresses = contactedUser.get_defaultDeliveryEmailAddresses()
if email_addresses:
    n_dict = {
        'siteName'            : form['siteName'],
        'supportEmail'        : get_support_email(context, site.getId()),
        'requestingPreferredName' : requestingUser.getProperty('preferredName'),
        'requestingEmail'     : requestingUser.get_defaultDeliveryEmailAddresses()[0],
        'requestingFirstName' : requestingUser.getProperty('firstName'),
        'requestingLastName'  : requestingUser.getProperty('lastName'),
        'canonical'           : canonical,
        'requestingId'        : requestingUser.getId(),
        'site'                : canonical,
        'requesting_user'     : requestingUser
    } # last two are for backwards-compatibility
  
    contactedUser.send_notification('request_contact', 'default', n_dict=n_dict)

result['error'] = False
result['message'] = '''The contact request has been sent.'''

return result

# url = '/%s/contacts/%s?mid=1040' % (division_object.getId(), user_id)
# return context.REQUEST.RESPONSE.redirect(url)
