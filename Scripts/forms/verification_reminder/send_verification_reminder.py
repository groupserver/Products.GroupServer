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
siteName = context.Scripts.get.option('canonicalHost') or site.title_or_id()
group = getattr(site.groups, groupId)
canonicalHost = context.Scripts.get.option('canonicalHost',
                                           'onlinegroups.net')
email_addresses  = userObj.get_defaultDeliveryEmailAddresses()
n_dict = {'first_name': userObj.firstName,
          'last_name':  userObj.lastName,
          'to_addr':    email_addresses[0],
          'site_name':  siteName,
          'group_name': group.title_or_id(),
          'cannonical_host': canonicalHost}
userObj.send_notification('confirm_registration',
                          'verification_reminder',
                          n_dict=n_dict)
return (True, '')

