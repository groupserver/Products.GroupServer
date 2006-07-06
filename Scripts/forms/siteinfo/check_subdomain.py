## Script (Python) "check_subdomain"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=subdomain=""
##title=Check Subdomain
##
import string

result = {}
site_root = context.site_root()

# Check to see if the domain name is valid. Dijkstra will hate me for
#   this.

if subdomain == '':
    result['error'] = True
    result['message'] = 'The subdomain must be specified.'
    return result

# Reference: http://www.ietf.org/rfc/rfc2396.txt section 3.2.2
#      domainlabel   = alphanum | alphanum *( alphanum | "-" ) alphanum
alphanum = string.digits + string.lowercase
validDomainChars = alphanum  + '-'
for c in subdomain:
    if c not in validDomainChars:
        result['error'] = True
        result['message'] = '''The character &#8220;%c&#8221; is not
          allowed in the subdomain. Please rewrite the subdomain.''' % c
        return result
if subdomain[0] not in alphanum:
    result['error'] = True
    result['message'] = '''The subdomain <em>must</em> start with a
      number or a letter. Please rewrite the subdomain.'''
    return result
if subdomain[-1] not in alphanum:
    result['error'] = True
    result['message'] = '''The subdomain must end with a number or a
      letter. Please rewrite the subdomain.'''
    return result

# Now to check if we already have a site with the same id as the one
#   we have been given
sitesContainer = site_root.Content
siteIds = map(lambda s: s[0],
              filter(lambda s: s[1].getProperty('is_division'),
                     sitesContainer.objectItems('Folder')))
if subdomain in siteIds:
    result['error'] = True
    result['message'] = '''There is already an OnlineGroups.Net site
      with the subdomain &#8220;%s&#8221;. Please choose another
      subdomain.''' % subdomain
    return result
# Check if a group exists with the same id
groupIds = map(lambda s: s[0],
               sitesContainer.objectItems('XWF Mailing List'))
if subdomain in groupIds:
    result['error'] = True
    result['message'] = '''There is an online group with the ID
      &#8220;%s&#8221;. Please choose another subdomain, as sites
      cannot have the same name as an existing group.'''
    return result
# Check if a user exists with the same id
userIds = site_root.acl_users.getUserNames()
if subdomain in userIds:
    result['error'] = True
    result['message'] = '''There is a user with the ID
      &#8220;%s&#8221;. Please choose another subdomain, as sites
      cannot have the same name as an existing user.'''
    return result
# The following two check should *NOT* hold if we have got this far.
# 1. Check in ACL Users
userGroups = site_root.acl_users.getGroupNames()
newUsergroupName = '%s_member' % subdomain
if newUsergroupName in userGroups:
    result['error'] = True
    result['message'] = '''There is already a user-group called
      &#8220;%s&#8221;. As there is no site or group called %s, this
      should not have happened. Please contact OnlineGroups.Net
      support.''' % (subdomain, subdomain)
    return result
# 2. Check in the add_group email template
addGroupNotification = site_root.Templates.email.notifications.add_group
ids = list(addGroupNotification.getProperty('ignore_ids'))
if newUsergroupName in ids:
    result['error'] = True
    result['message'] = '''We are handling email notifications to a
      group called &#8220;%s&#8221;. As there is no site or group called
      %s, this should not have happened. Please contact OnlineGroups.Net
      support.''' % (subdomain, subdomain)
    return result

# If we are here, then all is well in the world
result['error'] = False
result['message'] = '''The subdomain %s is valid.''' % subdomain
return result

# --= Unit Tests =--
# >>> check_subdomain('foobar')['error'] == False
# >>> check_subdomain('foo-bar')['error'] == False
# >>> check_subdomain('foo=bar')['error'] == True
# >>> check_subdomain('-foobar')['error'] == True
# >>> check_subdomain('foobar-')['error'] == True
