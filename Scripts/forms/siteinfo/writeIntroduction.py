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

result= {}

introXML = '''<?xml version="1.0" encoding="utf-8"?>
<div
  xmlns:tal="http://xml.zope.org/namespaces/tal"
  xmlns:metal="http://xml.zope.org/namespaces/metal" 
  metal:define-macro="division_introduction" 
  class="introduction">

  <paragraph>
    %s
	</paragraph> 
</div>''' % introduction

introFile = 'Content/%s/division_introduction.xml' % siteId
divIntro = context.restrictedTraverse(introFile)

divIntro.write(introXML)

# No error
result['error'] = False
result['message'] = 'The site introduction has been changed.'
return result
