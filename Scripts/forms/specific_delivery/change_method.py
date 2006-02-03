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
required = {"delivery_setting": "A choice of delivery method is required, but was not selected",
            "group_id": "A group ID was required, but was not specified"}
            
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

delivery_setting = form.get('delivery_setting')
group_id = form.get('group_id')

user = context.REQUEST.AUTHENTICATED_USER
if delivery_setting == 'disabled':
    user.set_disableDeliveryByKey(group_id)
else:
    user.set_enableDeliveryByKey(group_id)

if delivery_setting == 'topicdigest':
    user.set_enableDigestByKey(group_id)
else:
    user.set_disableDigestByKey(group_id)

result['message'] = "<p>Successfully added address</p>"

return result