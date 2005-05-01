## Script (Python) "update_session"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##
if context.REQUEST.AUTHENTICATED_USER.getId() == 'Anonymous User':
    return 1

if context.REQUEST.URL.split('/')[-1] in ('userinfo.xml', 'useremail.xml'):
    context.REQUEST.SESSION['last_url'] = context.REQUEST.URL

return 1
