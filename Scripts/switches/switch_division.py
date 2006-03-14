## Script (Python) "switch_division"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=id=None, set_password=None
##title=
##
# If we know the id of the division we should switch to, then try to switch to that division
# otherwise:
#            If we have one division only, switch to that one
#            If we have more than one division, switch to a page explaining how to switch division
#
# For additional security, we still iterate through the division objects
site_root = context.site_root()
user = context.REQUEST.AUTHENTICATED_USER
groups = user.getGroups()

virtualSitesOnly = context.Scripts.get.option('virtualSitesOnly')
if virtualSitesOnly and context.Scripts.get.division_object():
    return 

division_objects = context.Scripts.get_division_objects()
division_ids = map(lambda x: x.getId(), division_objects)

division = ''
if not id:
    tid = user.getProperty('currentDivision', '')
    # check we actually have access to the division still
    if tid in division_ids:
        id = tid

# if we don't have an id, look to see if we're in a system group that corresponds to
# a particular division
if not id:
    for group in groups:
        group_parts = group.split('_member')
        if len(group_parts) == 2:
            gid = group_parts[0]
            if gid in division_ids:
                id = gid

if id:
    for division_object in division_objects:
        if division_object.getId() == id:
            absolute_url = division_object.absolute_url(1)
                        
            if absolute_url == '':
                division = '%s/' % absolute_url
            else:
                division = '/%s/' % absolute_url
            
            #division = '/'+absolute_url+'/'

#if not division and len(division_objects) == 1:
# just choose the first division object
if not division and len(division_objects) >= 1:
    division_object = division_objects[0]
    id = division_object.getId()
    division = '/'+division_object.absolute_url(1)+'/'

if division and set_password:
    return context.REQUEST.RESPONSE.redirect('%s/set_password.xml' % division, lock=1)

if id and id != 'unverified' and user.getProperty('currentDivision', '') != id:
    # adjust the user object so that it points to the current division
    try:
        user.manage_changeProperties(currentDivision=id)
    except:
        pass

if not division:
    division = '/nodivision_message'
    try:
        user.manage_changeProperties(currentDivision='')
    except:
        pass

return context.REQUEST.RESPONSE.redirect(division, lock=1)
