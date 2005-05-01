## Script (Python) "unset_default_email"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=email
##title=
##
user = context.REQUEST.AUTHENTICATED_USER

email = filter(None, email)

for e in email:
    user.remove_preferredEmailAddress(e)

return context.REQUEST.RESPONSE.redirect(context.REQUEST.SESSION['last_url'])
