## Script (Python) "division_level"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##
from Products.XWFCore.XWFUtils import deprecated
deprecated(context, script, "Use Zope Five traversal instead.")

request = container.REQUEST
RESPONSE =  request.RESPONSE
if getattr(context, 'supress_redirect', False):
    return True

user = context.REQUEST.AUTHENTICATED_USER
groups = user.getGroups()
if 'unverified_member' in groups:
    path_bits = filter(None, request.URLPATH0.split('/'))
    if path_bits and path_bits[0] != 'unverified':
        return RESPONSE.redirect('/unverified/', lock=1)

canonicalHost = context.Scripts.get.option('canonicalHost', None)
if canonicalHost:
    base_host = request.BASE0.split('/')[-1]
    if base_host != canonicalHost:
        URL = request.URL
        QUERY = request.QUERY_STRING
        new_url = URL.replace(base_host, canonicalHost)+'?'+QUERY
        return RESPONSE.redirect(new_url, lock=1)

#
# Switched off, 2007-02-21 - richard@iopen.net
#

#user = request.AUTHENTICATED_USER
#if user.getUserName() != 'Anonymous User':
#    if getattr(context, 'is_division', False):
#         div_object = context.Scripts.get.division_object()
#         div_id = div_object.getId()
#         if user.getProperty('currentDivision') != div_id:
#             user.manage_changeProperties(currentDivision=div_id)
#         return True
#    else:
#         division = user.getProperty('currentDivision')
#         nurl = division+request.URLPATH0
#         nurl = '/'+'/'.join(filter(None, nurl.split('/')))
#         return RESPONSE.redirect(nurl, lock=1)

return True
