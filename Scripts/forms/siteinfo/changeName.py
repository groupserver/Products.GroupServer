## Script (Python) "changeName"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=Change Site Name
##

# Change the site name. This is *not* one of the assistant-scripts,
#   those are suffixed with "next"

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

sitename = form['sitename']
# For most sites, the siteId is the subdomain, but not always.
siteId = form['siteId'] 

# Check for errors in the site name
result = container.check_name(sitename)
if result['error']:
    return result


siteTitle = '%s Online Groups' % sitename
site = context.restrictedTraverse('Content/%s' % siteId)
site.manage_changeProperties(title=siteTitle)

# No error, redirect
result['error'] = False
result['message'] = 'The site name has been changed'
return result
