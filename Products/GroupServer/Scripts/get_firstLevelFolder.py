## Script (Python) "get_firstLevelFolder"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=object
##title=
##
try:
    while object:
        if getattr(object.aq_explicit, 'menu_root', 0) or getattr(object.aq_parent.aq_explicit, 'is_division', 0):
            return object
        object = object.aq_parent.aq_explicit
except:
    return None
