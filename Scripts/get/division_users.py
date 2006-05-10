## Script (Python) "site_users"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=divisionId=''
##title=
##

divisionGroup = '%s_member' % divisionId
users = context.Scripts.get.users_from_groups([divisionGroup])

return users
