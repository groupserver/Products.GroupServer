## Script (Python) "start_site"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=siteId=None, sitename=None, siteintro='', userId=None, step=0
##title=Start a Site
##

# This script is near omnipotent as it has to create some low-level
#   objects.

# <preconditions>
assert(siteId != None)
assert(siteId != '')
assert(sitename != None)
assert(sitename != '')
assert(userId != None)
assert(userId != '')
# Check to see if the site does not already exist
sitesContainer = context.restrictedTraverse('Content')
siteIds = map(lambda s: s[0],
              filter(lambda s: s[1].getProperty('is_division'),
                     sitesContainer.objectItems('Folder')))
assert(siteId not in siteIds)
# </preconditions>


#------------------------------------------------------------
if step == 0:
    return
#------------------------------------------------------------



# 0. Remove copy of the example division, if it exists
try:
    sitesContainer.manage_delObjects(('copy_of_example_division',))
except:
    pass

# 1. create a virtual site (technically, a division) object
# * make a copy of the example division
copiedExampleSite = \
                  sitesContainer.manage_copyObjects(('example_division',))
sitesContainer.manage_pasteObject(copiedExampleSite)

#------------------------------------------------------------
if step == 1:
    return
#------------------------------------------------------------

# * rename the copy with the id of your virtual site
sitesContainer.manage_renameObject('copy_of_example_division', siteId)

#------------------------------------------------------------
if step == 1.5:
    return
#------------------------------------------------------------

# 2. configure the site object
newSite = context.restrictedTraverse('/Content/%s' % siteId)

# * in the Properties tag of your new division object, edit
# the "Title" to reflect the title of your new virtual site
siteTitle = '%s Online Groups' % sitename
newSite.manage_changeProperties(title=siteTitle)

#------------------------------------------------------------
if step == 2:
    return
#------------------------------------------------------------

# * navigate to the DivisionConfiguration? object
divisionConfiguration = newSite.objectItems('Custom Properties')[1]

# * in the Properties the DivisionConfiguration? object,
# edit the canonicalHost property to the subdomain of your
# new virtual site e.g. newdivision.onlinegroups.net
hostname='%s.onlinegroups.net' % siteId
divisionConfiguration.manage_changeProperties(canonicalHost=hostname)

#------------------------------------------------------------
if step == 2.5:
    return
#------------------------------------------------------------

# * add a Virtual Host Monster, naming it VHM
newSite.manage_addVirtualHostMonster('VHM')

#------------------------------------------------------------
if step == 2.8:
    return
#------------------------------------------------------------

# 3. set up a site news object
# * delete the news object
newSite.manage_delObjects(('news',))

#------------------------------------------------------------
if step == 3:
    return
#------------------------------------------------------------


# * create a new XWF News object, naming it news
newSite.manage_addXWFNews('news')

#------------------------------------------------------------
if step == 3.2:
    return
#------------------------------------------------------------

# * copy the news/index.xml file from example_division and
# paste inside your new news object
exampleDivision = \
                context.restrictedTraverse('/Content/example_division/news')
oldNewsIndex = exampleDivision.manage_copyObjects(('index.xml',))
newNews = context.restrictedTraverse('/Content/%s/news' % siteId)
newNews.manage_pasteObject(oldNewsIndex)

#------------------------------------------------------------
if step == 3.4:
    return
#------------------------------------------------------------


# 4. set up permissions for the site
# * navigate to acl_users
aclUsers = context.restrictedTraverse('acl_users')
# * in the acl_users usergroups tab, create a usergroup
#   called newdivision_member (replace newdivision with the id
#   of your new division)
newUsergroupName = '%s_member' % siteId
aclUsers.manage_addGroup(newUsergroupName)

#------------------------------------------------------------
if step == 4:
    return
#------------------------------------------------------------

# * back in your new division, navigate to the security tab
#   and then local roles
# * give newdivision_member the DivisionMember local role
#   (and revoke the DivisionMember? status for any other
#   usergroups)

#--=mpj17=-- ??
newSite.manage_addLocalRoles(newUsergroupName, 'DivisionMember')

#------------------------------------------------------------
if step == 5:
    return
#------------------------------------------------------------


# 5. appoint a site administrator
# * navigate to the new division (GVS) object, and then to
#   security tab and then to local roles 
# * give DivisionAdmin role to the userid of the person who
#   will be administering the GVS 

#--=mpj17=-- ??
newSite.manage_addLocalRoles(userId, 'DivisionAdmin')

#------------------------------------------------------------
if step == 5.2:
    return
#------------------------------------------------------------

# (add them as a user if necessary)
#--=mpj17=-- ??
user = aclUsers.getUser(userId)
user.manage_addGroup(newUsergroupName)

#------------------------------------------------------------
if step == 5.4:
    return
#------------------------------------------------------------

# 6. configure the site for groups
# * delete groups/example-group
newSite.groups.manage_delObjects(('example-group',))

#------------------------------------------------------------
if step == 6:
    return
#------------------------------------------------------------

# * navigate to
# /sites/site_id/Templates/email/notifications/add_group
agnName = '/sites/onlinegroups/Templates/email/notifications/add_group'
addGroupNotification = \
                     context.restrictedTraverse(agnName)

# go to the the properties tab, add the usergroup of your new
# GroupServer? Virtual Site to the ignore_ids property of
# add_group
ids = addGroupNotification.getProperty('ignore_ids')
ids.append(newUsergroupName)
addGroupNotification.manage_changeProperties(ignore_ids=ids)

#------------------------------------------------------------
if step == 6.5:
    return
#------------------------------------------------------------


# 7. test that your new site is browseable

context.REQUEST.RESPONSE.redirect('http://%s.onlinegroups.net/' % siteId)
