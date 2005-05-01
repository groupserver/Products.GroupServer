## Script (Python) "email"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=email='', user_id=None
##title=
##
if user_id:
    user = context.acl_users.getUser(user_id)
else:
    user = context.REQUEST.AUTHENTICATED_USER

email = email.strip()

error = 0
try:
    user.add_emailAddress(email)
except:
    error = 1

if error:
    return context.REQUEST.RESPONSE.redirect('%s?error=email' % context.REQUEST.SESSION['last_url'])
else:
    return context.REQUEST.RESPONSE.redirect(context.REQUEST.SESSION['last_url'])
