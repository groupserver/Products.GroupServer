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

introXML = """<div 
  xmlns:tal="http://xml.zope.org/namespaces/tal"
  class="introduction">
  %s
</div>""" % introduction
division = getattr(site_root.Content, siteId)

if hasattr(division, 'introduction'):
    division.manage_changeProperties({'introduction': introXML})
else:
    division.manage_addProperty('introduction', introXML, 'text')

assert hasattr(division, 'introduction')
# No error
result['error'] = False
result['message'] = 'The site introduction has been changed.'
return result
