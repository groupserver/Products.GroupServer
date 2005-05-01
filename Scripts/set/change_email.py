## Script (Python) "change_email"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=delete=None, preferred=None, user_id=None
##title=
##
if user_id:
    user = context.acl_users.getUser(user_id)
else:
    user = context.REQUEST.AUTHENTICATED_USER

if preferred and delete:
    preferred = filter(lambda x: not x in delete, preferred)

if delete:
    for email in delete:
        user.remove_emailAddress(email)

if preferred:
    user.add_preferredEmailAddresses(preferred)
else:
    # we actually want a toggle effect, so if we have NO preferred email addresses, we should say so
    user.add_preferredEmailAddresses([])

return context.REQUEST.RESPONSE.redirect(context.REQUEST.SESSION['last_url'])
