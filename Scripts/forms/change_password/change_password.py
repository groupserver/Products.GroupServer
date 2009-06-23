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
site_root = context.site_root()

required = {'password1': '<p>You must specify new password</p>',
            'password2': '<p>You must repeat the new password</p>'}
            
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

password1 = form.get('password1','')
password2 = form.get('password2','')

if password1 != password2:
    result['error'] = 1
    result['message'] = '<p>The passwords you have specified did not match</p>'

if result.get('error', False):
    return result

user = context.REQUEST.AUTHENTICATED_USER

roles = user.getRoles()
domains = user.getDomains()
    
site_root.acl_users.userFolderEditUser(user.getId(), password1, roles, domains)
site_root.cookie_authentication.credentialsChanged(user, user.getId(), password1)

result['message'] = "<p>Successfully changed password</p>"

return result
