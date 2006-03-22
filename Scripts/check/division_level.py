## Script (Python) "division_level"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##
request = container.REQUEST
RESPONSE =  request.RESPONSE
if getattr(context, 'supress_redirect', False):
    return True

user = context.REQUEST.AUTHENTICATED_USER
groups = user.getGroups()
if 'unverified_member' in groups:
    return RESPONSE.redirect('/unverified', lock=1)

canonicalHost = context.Scripts.get.option('canonicalHost', None)
if canonicalHost:
    base_host = request.BASE0.split('/')[-1]
    if base_host != canonicalHost:
        URL = request.URL
        new_url = URL.replace(base_host, canonicalHost)
        return RESPONSE.redirect(new_url, lock=1)

user = request.AUTHENTICATED_USER
if user.getUserName() != 'Anonymous User':
    if getattr(context, 'is_division', False):
         return True
    else:
         division = user.getProperty('currentDivision')
         nurl = division+request.URLPATH0
         nurl = '/'+'/'.join(filter(None, nurl.split('/')))
         return RESPONSE.redirect(nurl, lock=1)

return True
