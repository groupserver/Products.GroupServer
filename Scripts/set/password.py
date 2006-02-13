## Script (Python) "password"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=password1, password2, user_id=None, came_from=None
##title=
##
error = 0
site_root = context.site_root
if user_id:
    user = site_root.acl_users.getUser(user_id)
else:
    user = context.REQUEST.AUTHENTICATED_USER

password1 = password1.strip()
password2 = password2.strip()

if password1 != password2:
    error = 1

if not password1:
    error = 1

if not error:
    user.set_password(password)

if came_from:
    return context.REQUEST.RESPONSE.redirect('%s?message=Your password was updated successfully' % came_from)

elif context.REQUEST.SESSION.has_key('last_url'):
    last_url = context.REQUEST.SESSION['last_url']
    if last_url and error:
        url = '%s?error=pw' % last_url
        return context.REQUEST.RESPONSE.redirect(url)
    elif last_url:
        lbits = last_url.split('/')
        if len(lbits) and len(lbits[-1]) > 8 and lbits[-1][:8] != 'set_pass':
            return context.REQUEST.RESPONSE.redirect(last_url)

return context.REQUEST.RESPONSE.redirect('/Scripts/switches/switch_division')
