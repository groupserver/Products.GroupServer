## Script (Python) "request_contact"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=Request Contact from User
##

from Products.XWFCore.XWFUtils import get_support_email, get_user_realnames

result = {}

form = context.REQUEST.form
assert form.has_key('contactedUser')
assert form.has_key('site')
assert form.has_key('siteName')
assert form.has_key('siteId')
result['form'] = form

for field in form:
    try:
        form[field] = form[field].strip()
    except AttributeError:
        pass

requestingUser = context.REQUEST.AUTHENTICATED_USER
site_root = context.site_root()
siteId = form['siteId']
assert siteId
site = getattr(site_root.Content, siteId)
contactedUser = site_root.acl_users.getUser(form['contactedUser'])
canonical = form['site']
requesting_id = requestingUser.getId()

email_addresses = contactedUser.get_defaultDeliveryEmailAddresses()
if email_addresses:
    n_dict = {
        'siteName'       : form['siteName'],
        'supportEmail'   : get_support_email(context, siteId),
        'requestingName' : get_user_realnames(requestingUser, requesting_id),
        'requestingEmail': requestingUser.get_defaultDeliveryEmailAddresses()[0],
        'canonical'      : canonical,
        'requestingId'   : requesting_id
    }
  
    contactedUser.send_notification('request_contact', 'default', n_dict=n_dict)

result['error'] = False
result['message'] = '''The contact request has been sent.'''

return result

