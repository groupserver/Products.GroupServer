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

# Check for errors in the site name
result = container.check_name(form['sitename'])
if result['error']:
    return result

# No error, redirect
result['error'] = False
result['message'] = 'The site name has been changed'
return result
