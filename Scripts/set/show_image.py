## Script (Python) "show_image"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=showimage=0, user_id=None
##title=
##
try:
    showimage = int(showimage)
except:
    showimage = 1
if user_id:
    user = context.acl_users.getUser(user_id)
else:
    user = context.REQUEST.AUTHENTICATED_USER

restrictimage = not showimage # we actually _suppress_ the user's image

user.manage_changeProperties({'restrictImage': restrictimage})

try:
    return context.REQUEST.RESPONSE.redirect(context.REQUEST.SESSION['last_url'])
except:
    return 1
