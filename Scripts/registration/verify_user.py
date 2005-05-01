## Script (Python) "verify_user"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=verification_code, verify=False, remove=False
##title=
##
if not verification_code:
    return
site_root = context.site_root()
user = context.REQUEST.AUTHENTICATED_USER

if remove:
    if user.get_verificationCode() == verification_code:
        site_root.acl_users.userFolderDelUsers([user.getId()])
    return context.REQUEST.RESPONSE.redirect('/cookie_authentication/logout')
elif verify:
    if user:
        user.verify_user(verification_code)
    
    # redirect to take us to our new division
    return context.REQUEST.RESPONSE.redirect('/Scripts/switches/switch_login')
