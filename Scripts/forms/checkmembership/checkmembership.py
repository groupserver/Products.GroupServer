## Script (Python) "checkmembership"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=Check Membership
##
site_root = context.site_root()
result = {}

form = context.REQUEST.form
assert form.has_key('emailAddr')
result['form'] = form

for field in form:
    try:
        form[field] = form[field].strip()
    except AttributeError:
        pass

emailAddr = form['emailAddr'].lower()

if '@' not in emailAddr:
    result['error'] = True
    result['message'] = '''The address that was entered, %s, was not
      valid. Please enter a valid email address.''' % emailAddr
    return result

user = site_root.acl_users.get_userByEmail(emailAddr)
n_dict{'to_addr': emailAddr,
       'user_name': ''}
if user:
    # Member of OnlineGroups.Net
    n_dict['user_name'] = user.getUserName()
    user.send_notification('checkmembership',
                           'is_member',
                           n_dict=n_dict)
else:
    # Not a member of OnlineGroups.Net
    user.send_notification('checkmembership',
                           'not_member',
                           n_dict=n_dict)

result['error'] = False
result['message'] = '''A message, detailing the membership of
    OnlineGroups.Net, has been sent to %s.''' % emailAddr
