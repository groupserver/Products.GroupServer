## Script (Python) "send_verification_reminder"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=siteId='',groupId='',userId=''
##title=Send the Verification Reminder to a User
##
from Products.PythonScripts.standard import html_quote
import DateTime
from Products.GSProfile.utils import send_verification_message

assert siteId
assert groupId
assert userId

site_root = context.site_root()
userObj = site_root.acl_users.getUser(userId)
assert userObj

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
verified = userObj.get_verifiedEmailAddresses()
allAddr = userObj.get_emailAddresses()
unverified = [e for e in allAddr if e not in verified]

for email in unverified:
    send_verification_message(site, userObj, email)
return (True, '')

