## Script (Python) "register_user"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=first_name='', last_name='', email='', user_id='', site_id='', groups=[], manual=1, userproperties={}, sendVerification=True, came_from=''
##title=
##
from Products.XWFCore.XWFUtils import createRequestFromRequest, getOption
from Products.XWFCore.XWFUtils import get_support_email, get_site_by_id

redirect = context.REQUEST.RESPONSE.redirect
form = context.REQUEST.form

site_root = context.site_root()
error = []
if not first_name:
    error.append('error:list=fname')
if not last_name:
    error.append('error:list=lname')
if not email:
    error.append('error:list=email')

if manual:
    for prop_def in context.UserProperties.objectValues():
        if prop_def and prop_def.getId() not in ['email', 'first_name', 'last_name', 'user_id']:
            if prop_def.getProperty('required', 0) and not form.get(prop_def.getId(), None):
                error.append('error:list=required')

group_string = '&'.join(map(lambda x: 'groups:list=%s' % x.split('_member')[0], groups))

if error:
    if manual:
        error_string = '&'.join(error)
        rstring = str('/login/register.xml?%s&%s&%s' % (error_string, createRequestFromRequest(context.REQUEST, first_name=first_name, last_name=last_name, email=email, user_id=user_id), group_string))
        return redirect(rstring)
    return 0

try:
    user_id, password, verification_code = site_root.acl_users.register_user(email, user_id, first_name, last_name)
except Exception, x:
    exception_string = str(x)
    
    if exception_string.find('email address') > -1:
        error.append('error:list=email_exists')
    elif exception_string.find('%s already exists' % user_id) > -1:
        error.append('error:list=id_exists')
    elif exception_string.find('invalid') > -1:
        error.append('error:list=id_invalid')
    else:
        error.append('error:list=%s' % x)

if error:
    if manual:
        error_string = '&'.join(error)
        return redirect('/login/register.xml?%s&came_from=%s&first_name=%s&last_name=%s&email=%s&user_id=%s&%s' % (error_string, came_from, first_name, last_name, email, user_id, group_string))
    return 0
    
user = site_root.acl_users.getUser(user_id)

for prop in userproperties.keys():
    prop_def = getattr(context.UserProperties.aq_explicit, prop, None)
    if prop_def and prop != 'email':
        if user.hasProperty(prop):
            user.manage_changeProperties({prop: userproperties[prop]})
        else:
            user.manage_addProperty(prop, userproperties[prop], prop_def.getProperty('property_type'))

for prop in form:
    try:
        prop_def = getattr(context.UserProperties.aq_explicit, prop, None)
    except:
        continue
    
    if prop_def and getattr(prop_def, 'property_type', None) and prop not in ['email', 'first_name', 'last_name', 'user_id']:
        if user.hasProperty(prop):
            user.manage_changeProperties({prop: form[prop]})
        else:
            user.manage_addProperty(prop, form[prop], prop_def.getProperty('property_type'))

if groups:
    user.set_verificationGroups(groups)

if sendVerification:
	user.send_userVerification(password=password, site=context.REQUEST.SERVER_URL)
else:
	# --=mpj17=-- I should be punished for this:
	# If there is no verification email sent, then just verify the
	#   SOB. This creates a hole for spammers.
	verificationCode = user.get_verificationCode()
	user.verify_user(verificationCode)
	
	site = get_site_by_id(context, site_id)
	canonical = getOption(site, 'canonicalHost', 'onlinegroups.net')

	# Send an "Administrator-Verified Join" message
	n_dict = {
		'user_id'       : user_id,
		'password'      : password,
		'canonical'     : canonical,
    'siteName'      : site.title_or_id(),
    'supportEmail'  : get_support_email(context, site_id)
	}
	user.send_notification(n_type='admin_verified_join', 
		n_id='default', n_dict=n_dict)

if manual:
    if came_from:
        return redirect('/login/index.xml?error:list=register_thanks&came_from=%s' % came_from)
    else:
        return redirect('/login/index.xml?error:list=register_thanks')

return user
