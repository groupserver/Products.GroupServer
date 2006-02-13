## Script (Python) "switch_login"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=came_from=None
##title=
##
# if the user doesn't have a password set, nag them for it
user = context.REQUEST.AUTHENTICATED_USER
cd = user.getProperty('currentDivision')
if not cd:
    context.REQUEST.RESPONSE.redirect('/cookie_authentication/logout')
    
try:
    password = context.REQUEST.AUTHENTICATED_USER.get_password()
    if not password:
        return context.switch_division(set_password=1)
except:
    pass

if came_from:
    return context.REQUEST.RESPONSE.redirect(came_from)

return context.switch_division()
