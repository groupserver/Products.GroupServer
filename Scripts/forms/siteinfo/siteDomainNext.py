import string
result = {}

form = context.REQUEST.form
assert form.has_key('sitename')
assert form.has_key('subdomain')
result['form'] = form

for field in form:
    try:
        form[field] = form[field].strip()
    except AttributeError:
        pass

# Remove .onlinegroups.net from the end of the name; in fact,
#   remove everything after the first ".".
subdomain = form['subdomain'].split('.')[0].lower()

result = container.check_subdomain(subdomain)
if result['error']:
    return result

# No error, redirect
nextURL = form.get('nextURL', 'siteintroduction.xml')
nextURL = '%s?sitename=%s&subdomain=%s' % (nextURL, form['sitename'],
                                           subdomain)
context.REQUEST.RESPONSE.redirect(nextURL)
