## Script (Python) "writeIntroduction"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=introduction='',siteId=''
##title=Change Site Introduction
##

# We do not care if the introduction is empty
assert siteId != ''

site_root = context.site_root()
assert site_root
assert hasattr(site_root, 'Content')

result= {}

division = getattr(site_root.Content, siteId)

if hasattr(division, 'introduction'):
    division.manage_changeProperties({'introduction': introduction})
else:
    division.manage_addProperty('introduction', introduction, 'text')

assert hasattr(division, 'introduction')
# No error
result['error'] = False
result['message'] = 'The site introduction has been changed.'
return result
