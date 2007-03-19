## Script (Python) "siteIntroductionNext"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=Site Introduction Next
##
from Products.PythonScripts.standard import url_quote

result = {}

form = context.REQUEST.form
assert form.has_key('sitename')
assert form.has_key('subdomain')
assert form.has_key('introduction')
result['form'] = form

for field in form:
    try:
        form[field] = form[field].strip()
    except AttributeError:
        pass

result = container.check_introduction(form['introduction'])
if result['error']:
    return result

# No error, redirect
nextURL = form.get('nextURL', 'sitereview.xml')
nextURL = '%s?sitename=%s&subdomain=%s&introduction=%s' % (nextURL, 
                                                           url_quote(form['sitename']), 
                                                           url_quote(form['subdomain']),
                                                           url_quote(form['introduction']))
context.REQUEST.RESPONSE.redirect(nextURL)
