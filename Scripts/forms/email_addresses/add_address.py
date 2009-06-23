## Script (Python) "process_form"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##
from Products.XWFCore import validators as v
required = {"email": "An email address is required, but was not given"}
            
validators = {}

result = {}

form = context.REQUEST.form
result['form'] = form

if not form.get('submitted', False):
    return result

result['message'] = ""
for field in form:
    try:
        form[field] = form[field].strip()
    except AttributeError:
        pass
   
    if not form[field] and required.has_key(field):
        result['message'] = result['message']+"<dw:para>%s</dw:para>" % required[field]
        result['error'] = True
    else:
        try:
            form[field] = validators.get(field, lambda x: x)(form[field])
        except v.ValidationError, x:
            result['message'] = result['message']+"<dw:para>%s</dw:para>" % x
            result['error'] = True
            
if result.get('error', False):
    return result

email = form.get('email')

try:
    # crude, really crude, way of telling if we're a list
    email.append
except:
    email = [email]

user = context.REQUEST.AUTHENTICATED_USER
for e in email:
    if e:
        try:
            v.validate_email(e)
            user.add_emailAddress(e)
        except v.ValidationError, x:
            result['message'] = result['message']+"<dw:para>%s</dw:para>" % x
            result['error'] = True

if not result.get('error', False):
    result['message'] = "<p>Successfully added address</p>"

return result