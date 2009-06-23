## Script (Python) "siteNameNext"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=Site Name Next
##
from Products.PythonScripts.standard import url_quote
result = {}

form = context.REQUEST.form
assert form.has_key('sitename')
result['form'] = form

for field in form:
    try:
        form[field] = form[field].strip()
    except AttributeError:
        pass

# Remove Online Groups from the end of the name
if (form['sitename'][-13:].lower() == 'online groups'):
    form['sitename'] = form['sitename'][:-13].strip()

# Check for errors in the site name
result = container.check_name(form['sitename'])
if result['error']:
    return result

# No error, redirect
nextURL = form.get('nextURL', 'sitedomain.xml')
nextURL = '%s?sitename=%s' % (nextURL, url_quote(form['sitename']))
context.REQUEST.RESPONSE.redirect(nextURL)
