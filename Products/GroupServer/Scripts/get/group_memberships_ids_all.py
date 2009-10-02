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
   
    m = []
    for gtype in memberships:
        m += memberships.get(gtype, [])
    memberships = m
    
    canonicalHost = division_object.Scripts.get.option('canonicalHost')
    divisionTitle = division_object.title_or_id()
    for membership in memberships:
        membership_id = membership.getId()
        if not membership_id in group_ids:
            groupUrl = "/%s" % membership.absolute_url(1)
            group_title_ids.append((membership.getProperty('title'),
                                    membership_id,
                                    groupUrl,
                                    divisionTitle,
                                    canonicalHost)) 
            group_ids.append(membership_id)
    
return group_title_ids
