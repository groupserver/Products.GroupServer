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
blarg = []
while group_object:
    try:
        group_object = group_object.aq_parent
        blarg = group_object.getProperty('is_group')
        if blarg == True:
            break
    except:
        break

return group_object
