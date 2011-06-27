## Script (Python) "reminders_sent"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=user_id
##title=Get the List of Reminders sent to the User
##
from Products.XWFCore.XWFUtils import deprecated
deprecated(context, script, "Use gs.group.member.invite instead.")
site_root = context.site_root()

retval = []
try:
    user = site_root.acl_users.getUser(user_id)
except:
    user = None

if user and user.hasProperty('reminders_sent'):
    retval = list(user.getProperty('reminders_sent'))

print retval
return printed    
return retval
