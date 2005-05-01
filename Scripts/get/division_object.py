## Script (Python) "division_object"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##
division_object = context
while division_object:
    try:
        division_object = division_object.aq_parent
        if getattr(division_object.aq_inner.aq_explicit, 'is_division', 0):
            break
    except:
        return None

return division_object.aq_inner.aq_explicit
