## Script (Python) "changeName"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=Change Site Name (Standard Version)
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

sitename = form['sitename']
# For most sites, the siteId is the subdomain, but not always.
siteId = form['siteId'] 

# Check for errors in the site name
result = container.check_name(sitename)
if result['error']:
    return result

site = context.restrictedTraverse('Content/%s' % siteId)
site.manage_changeProperties(title=sitename)
site.DivisionConfiguration.manage_changeProperties(siteName=sitename)

# No error, redirect
result['error'] = False
result['message'] = """<p>The site name has been
  changed to &#8220;%s&#8221;.</p>""" % sitename
return result
