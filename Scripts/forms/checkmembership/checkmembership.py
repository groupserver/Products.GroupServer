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
n_dict = {'to_addr': emailAddr,
          'user_name': ''}
if user:
    # Member of OnlineGroups.Net
    n_dict['user_name'] = user.getUserName()
    user.send_notification('checkmembership',
                           'is_member',
                           n_dict=n_dict)
else:
    # Not a member of OnlineGroups.Net
    try:
        mailhost = site_root.superValues('Mail Host')[0]
    except:
        raise AttributeError, "Can't find a Mail Host object"
    presentation = site_root.Templates.email.notifications.aq_explicit
    
    ptype_templates = getattr(presentation, n_type, None)
    if not ptype_templates:
        return None
    template = (getattr(ptype_templates.aq_explicit, n_id, None) or
                getattr(ptype_templates.aq_explicit, 'default', None))
    if not template:
        return None

    template(None, self.REQUEST, emailAddr, 'not_member', 'checkmembership',
             n_dict=n_dict)

result['error'] = False
result['message'] = '''A message, detailing the membership of
    OnlineGroups.Net, has been sent to %s.''' % emailAddr
return result
