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
        in_division = division_object.getProperty('is_division')
        if in_division:
            break
    except AttributeError:
        pass
    division_object = division_object.aq_parent
        
return division_object.aq_explicit

