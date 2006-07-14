## Script (Python) "entity_exists"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=entityId=""
##title=Check if an Entity Exists
##
import string

assert id != ''

site_root = context.site_root()
assert site_root

# Now to check if we already have a site with the same entityId as the one
#   we have been given
assert hasattr(site_root, 'Content')
sitesContainer = site_root.Content
siteIds = map(lambda s: s[0],
              filter(lambda s: s[1].getProperty('is_division'),
                     sitesContainer.objectItems('Folder')))
if entityId in siteIds:
    return 1

# Check if a group exists with the same entityId
assert hasattr(site_root, 'ListManager')
groupIds = map(lambda s: s[0],
               site_root.ListManager.objectItems('XWF Mailing List'))
if entityId in groupIds:
    return 2

# Check if a user exists with the same entityId
assert hasattr(site_root, 'acl_users')
if site_root.acl_users.getUserById(entityId):
    return 3

# The following two check should *NOT* hold if we have got this far.
# 1. Check in ACL Users
try:
    site_root.acl_users.getGroupById('%s_member' % entityId)
except:
    pass
else:
    return 4
    
# 2. Check in the add_group email template
assert hasattr(site_root, 'Templates')
addGroupNotification = site_root.Templates.email.notifications.add_group
ids = list(addGroupNotification.getProperty('ignore_ids'))
if '%s_member' % entityId in ids:
    return 5

# If we are here, then all is well in the world

return False
