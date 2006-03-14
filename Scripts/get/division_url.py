## Script (Python) "division_url"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=no_division='/'
##title=
##
division_object = context.Scripts.get.division_object()

if division_object:
    absolute_url = division_object.absolute_url(1)
    if absolute_url == '':
        return absolute_url
    else:
        return '/%s' % division_object.absolute_url(1)
return no_division
