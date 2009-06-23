## Script (Python) "changeIntroduction"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=Change Site Introduction
##

# Change the introduction text for the site. This script is not part
#   of start a site code, they all end in "Next".

result = {}

form = context.REQUEST.form
assert form.has_key('introduction')
assert form.has_key('siteId')

result['form'] = form

for field in form:
    try:
        form[field] = form[field].strip()
    except AttributeError:
        pass

result = container.check_introduction(form['introduction'])
if result['error']:
    return result

return context.Scripts.forms.siteinfo.writeIntroduction(form['introduction'],
                                                        form['siteId'])
