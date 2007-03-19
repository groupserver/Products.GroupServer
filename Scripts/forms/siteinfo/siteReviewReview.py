## Script (Python) "siteReviewReview"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=Site Review Review
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

# Check the three fields. Most of the following is cut 'n' paste from
#   the "Next" scripts

# - Site name
#   Remove Online Groups from the end of the name
if (form['sitename'][-13:].lower() == 'online groups'):
    form['sitename'] = form['sitename'][:-13].strip()
#   Check for errors in the site name
result = container.check_name(form['sitename'])
if result['error']:
    return result

# - Subdomain
#   Remove .onlinegroups.net from the end of the name; in fact,
#   remove everything after the first ".".
subdomain = form['subdomain'].split('.')[0].lower()
result = container.check_subdomain(subdomain)
if result['error']:
    return result

# - Introduction
result = container.check_introduction(form['introduction'])
if result['error']:
    return result

nextURL = form.get('nextURL', 'sitereview.xml')
nextURL = '%s?sitename=%s&subdomain=%s&introduction=%s' % (nextURL, 
                                                           form['sitename'], 
                                                           form['subdomain'],
                                                           form['introduction'])
nextURL = url_quote(nextURL)
context.REQUEST.RESPONSE.redirect(nextURL)
