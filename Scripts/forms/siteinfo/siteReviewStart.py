## Script (Python) "siteReviewStart"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=Site Review Start
##

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

context.start_site(siteId=form['subdomain'],
                   sitename=form['sitename'],
                   siteintro=form['introduction'],
                   userId='michaeljasonsmith') # --=change=--

result['error'] = False
result['message'] = 'Starting a site has not been implemented yet.'
return result
