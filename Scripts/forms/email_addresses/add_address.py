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
            
validators = {"email": v.validate_email}

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
    pass
except:
    result['message'] = ("<p>Some problem.</p>")
    result['error'] = True
    return result

user = context.REQUEST.AUTHENTICATED_USER
user.add_emailAddress(email)

result['message'] = "<p>Successfully added address</p>"

return result