## Script (Python) "groups_object"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##
groups_object = context
while groups_object:
    try:
        groups_object = groups_object.aq_parent
        if getattr(groups_object.aq_inner.aq_explicit, 'is_groups', 0):
            break
    except:
        break

return groups_object.aq_inner.aq_explicit
