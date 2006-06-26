## Script (Python) "adduser_add_user"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=user=None,groups=[],email=''
##title="Add User: Add a User"
##

assert user!=None

site_root = context.site_root()
retval = {'message': '',
          'error': False,
          'count': 0}
userId = user.getId() # To save multiple function calls
userGroups = user.getGroups()

folders = site_root.Content.objectValues(('Folder',
                                          'Folder (Ordered)'))
sites = filter(lambda s: s.getProperty('is_division'), folders)
siteIds = map(lambda s: s.getId(), sites)

for group in groups:
    groupName = group.split('_member')[0]
    groupIsSite = groupName in siteIds
    siteOrGroup = groupIsSite and 'site' or 'group'
    inGroup = group in userGroups

    if (inGroup and groupIsSite):
        pass
    elif (inGroup and (not groupIsSite)):
        retval['message'] = retval['message'] + '''<listitem>The user
        %s <bold>has not</bold> been added to %s: %s is already a
        member of the %s.</listitem>\n''' % (userId, groupName,
                                             userId, siteOrGroup)
        retval['error'] = True
    elif user.add_groupWithNotification(group):
        if groupIsSite:
            site = filter(lambda s: s.getId() == groupName, sites)[0]
            groupName = site.title_or_id()
        retval['count'] = retval['count'] + 1
        retval['message'] = retval['message'] + '''<listitem>Added %s to
        the %s %s.</listitem>\n''' % (userId, siteOrGroup, groupName)
    else:
        retval['message'] = retval['message'] +'''<listitem>Could not
        add %s to the %s %s; this should not have
        happened.</listitem>\n''' % (userId, siteOrGroup, groupName)
        
return retval
