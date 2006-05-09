## Script (Python) "changeIntroduction"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=Change Site Introduction
##

result = {}

form = context.REQUEST.form
assert form.has_key('introduction')
result['form'] = form

for field in form:
    try:
        form[field] = form[field].strip()
    except AttributeError:
        pass

result = container.check_introduction(form['introduction'])
if result['error']:
    return result

# No error, redirect
result['error'] = False
result['message'] = 'Not implemented'
return result
