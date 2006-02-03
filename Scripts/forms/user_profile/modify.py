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
required = {}
            
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

user = context.REQUEST.AUTHENTICATED_USER
for key in form.keys():
    if key[0] == '_':
        continue
    prop = getattr(context.UserProperties.aq_explicit, key, None)
    if prop and user.hasProperty(prop.getId()):
        user.manage_changeProperties({key:form[key]})
    elif prop:
        user.manage_addProperty(prop.getId(), form[key], prop.getProperty('property_type'))

result['message'] = "<p>Successfully modified profile</p>"

return result