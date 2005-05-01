## Script (Python) "index_redirect"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##
# If we're logged in, make sure we're in the right division
user = context.REQUEST.AUTHENTICATED_USER
division = ''
if user.getUserName() != 'Anonymous User':
    try:
       division = user.get_division()
    except:
       division = ''

if division:
    context.REQUEST.RESPONSE.redirect(division)
    return 0

return 1
