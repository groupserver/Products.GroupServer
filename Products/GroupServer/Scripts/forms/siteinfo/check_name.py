## Script (Python) "check_name"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=sitename=""
##title=Check Site Name
##

result = {}

if sitename == '':
    result['error'] = True
    result['message'] = 'The site name must be specified.'
    return result

# Check for swearing
badWord = container.bad_words(sitename)
if badWord:
    result['error'] = True
    result['message'] = '''No profanities (such as %s) are allowed in
      the site name.''' % badWord 
    return result

# Check if the site exists
sites = filter(lambda s: s.getProperty('is_division'),
               map(lambda s: s[1], container.Content.objectItems('Folder')))
siteNames = filter(lambda site: site.title_or_id().lower(), sites)
if sitename.lower() in siteNames:
    result['error'] = True
    result['message'] = '''The site name %s has already
      been taken. Please pick another.''' %  sitename
    return result

result['error'] = False
result['message'] = '''The site name %s is valid.''' % sitename
return result

# --= Unit Tests =--
# >>> check_name('Foo Bar')['error'] == False
# >>> check_name('')['error'] == True
# >>> check_name('Foo Santorum Bar')['error'] == True
# >>> check_name('GroupServer.Org')['error'] == False
