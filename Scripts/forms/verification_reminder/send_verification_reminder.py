## Script (Python) "send_verification_reminder"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=siteId='',groupId='',userId='',adminId=''
##title=Send the Verification Reminder to a User
##
from Products.PythonScripts.standard import html_quote
import DateTime
from Products.GSProfile.utils import send_add_user_notification
from Products.GSContent.groupInfo import GSGroupInfoFactory

assert siteId
assert groupId
assert userId

site_root = context.site_root()
userObj = site_root.acl_users.getUser(userId)
assert userObj, 'No user instance for %s' % userId

adminObj = site_root.acl_users.getUser(adminId)
assert adminObj, 'No admin instance for %s' % adminId

if userObj.hasProperty('reminders_sent'):
    reminders = list(userObj.getProperty('reminders_sent'))
    if len(reminders) >= 5:
        return (False, 'too many reminders sent')
    reminders.append(DateTime.DateTime())
    userObj.manage_changeProperties(reminders_sent=reminders)
else:
    userObj.manage_addProperty('reminders_sent', [DateTime.DateTime()], 
                               'lines')
                               
site = getattr(site_root.Content, siteId)
groupInfo = GSGroupInfoFactory()(site, groupId)
send_add_user_notification(userObj, adminObj, groupInfo, '')

return (True, '')

