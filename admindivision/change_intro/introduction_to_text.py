## Script (Python) "introduction_to_text"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=siteId=None
##title=Convert the Introduction Object to Plain Text
##

site_root = context.site_root()
assert site_root
assert hasattr(site_root, 'Content')
division = getattr(site_root.Content, siteId)

retval = getattr(division, 'introduction', '').strip()
return retval

