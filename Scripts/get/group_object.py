## Script (Python) "group_object"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##
group_object = context
while group_object:
    try:
        group_object = group_object.aq_parent
        if getattr(group_object.aq_inner.aq_explicit, 'is_group', 0):
            break
    except:
        break

return group_object.aq_inner.aq_explicit
