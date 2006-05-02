## Script (Python) "siteNameNext"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=Site Name Next
##

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
context.REQUEST.RESPONSE.redirect('sitedomain.xml?sitename=%s' % form['sitename'])
 
