## Script (Python) "siteReviewReview"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=Site Review Review
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

context.REQUEST.RESPONSE.redirect('siteintroduction.xml?sitename=%s&subdomain=%s&introduction=%s' %
                                  (form['sitename'], form['subdomain'],
                                   form['introduction']))
