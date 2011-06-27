## Script (Python) "site_users"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=divisionId=''
##title=
##
from Products.XWFCore.XWFUtils import deprecated
deprecated(context, script, "Products.GSGroupMember.")

def sorter(a,b):
   if a ==None or b == None:
      return 0
   nameA = a.getProperty('fn', '')
   nameB = b.getProperty('fn', '')
   if nameA.lower() > nameB.lower():
      return 1
   else:
      return -1

divisionGroup = '%s_member' % divisionId
users = context.Scripts.get.users_from_groups([divisionGroup])

users = filter(lambda u: u != None, users)
users.sort(sorter)
assert users
return users
