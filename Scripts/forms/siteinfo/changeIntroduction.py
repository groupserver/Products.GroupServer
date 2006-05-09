## Script (Python) "changeIntroduction"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=Change Site Introduction
##

# Change the introduction text for the site. This script is not part
#   of start a site code, they all end in "Next".

result = {}

form = context.REQUEST.form
assert form.has_key('introduction')
result['form'] = form

for field in form:
    try:
        form[field] = form[field].strip()
    except AttributeError:
        pass

result = container.check_introduction(form['introduction'])
if result['error']:
    return result

# --=mppj17=--
# We really should check if division_intro.xml exisits, rather than
#  assuming it does!

introXML = '''<?xml version="1.0" encoding="utf-8"?>
<div
  xmlns:tal="http://xml.zope.org/namespaces/tal"
  xmlns:metal="http://xml.zope.org/namespaces/metal" 
  metal:define-macro="division_introduction" 
  class="introduction">

  <paragraph>
    %s
	</paragraph> 
</div>''' % form['introduction']

divIntro = context.restrictedTraverse('Content/%s/division_introduction.xml' %\
  form['siteId'])

divIntro.write(introXML)

# No error, redirect
result['error'] = False
result['message'] = 'Not implemented'
return result
