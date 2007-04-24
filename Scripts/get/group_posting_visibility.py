## Script (Python) "group_posting_visibility"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##
site_root = context.site_root()
group_object = context.Scripts.get.group_object()

listManager = site_root.objectValues('XWF Mailing List Manager')[0]
group = listManager.get_list(group_object.getId())

try:
    memberlist = filter(lambda a: a.lower(), group.getValueFor('mailinlist'))
except:
    return 'no'

user = context.REQUEST.AUTHENTICATED_USER
if user.getId():
    for address in user.get_emailAddresses():
        if address.lower() in memberlist:
            return 'yes'
return 'no'
