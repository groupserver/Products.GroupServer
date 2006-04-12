## Script (Python) "group_memberships_ids_all"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=division_objects, gtype, user_id=None
##title=
##
group_title_ids = []
group_ids = []
for division_object in division_objects:
    groups = getattr(division_object, 'groups', None)
    if not groups:
        continue
    memberships = context.group_memberships(division_object.groups, user_id)
    #if gtype:
    #    memberships = memberships.get(gtype, [])
    #else:
    if 1:
        m = []
        for gtype in memberships:
            m += memberships.get(gtype, [])
        memberships = m
    
    for membership in memberships:
        if not membership.getId() in group_ids:
            groupHost = division_object.Scripts.get.option('canonicalHost')
            #groupUrl = "http://%s/groups/%s" % (groupHost, membership.getId())
            groupUrl = "/%s" % membership.absolute_url(1)
            group_title_ids.append((membership.getProperty('title'),
                                    membership.getId(),
                                    groupUrl,
                                    division_object.title_or_id(),
                                    groupHost)) 
            group_ids.append(membership.getId())
    
return group_title_ids
