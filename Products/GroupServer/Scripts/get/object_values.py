## Script (Python) "object_values"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=ocontainer, otypes=()
##title=
##
# Basically a wrapped version of OFS.objectValues -- only
# return objects we are actually allowed to see
from Products.XWFCore.XWFUtils import deprecated
deprecated(context, script, "Use OFS.objectValues instead.")
objects = []
if not ocontainer:
    return objects

for object_id in ocontainer.objectIds(otypes):
    try:
        object = getattr(ocontainer, object_id)
        objects.append(object)
    except:
        pass

return objects
