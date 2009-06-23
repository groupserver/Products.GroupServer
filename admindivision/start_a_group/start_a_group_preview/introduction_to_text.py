## Script (Python) "introduction_to_text"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=siteId=None
##title=Convert the Introduction Object to Plain Text
##
introduction = context.restrictedTraverse('Content/%s/division_introduction.xml' % siteId)
#site = getattr(context.Content, siteId)
#introduction = getattr(site.aq_explicit, 'division_introduction.xml')

txt = introduction.document_src()

firstParStartIndex = txt.find('<paragraph>')+len('<paragraph>')
firstParEndIndex = txt.find('</paragraph>')

retval = txt[firstParStartIndex:firstParEndIndex].strip()

return retval
