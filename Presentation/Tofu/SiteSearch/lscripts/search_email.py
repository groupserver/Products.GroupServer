## Script (Python) "search_email"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=groups, search_term
##title=
##
queries = [{'mailSubject': search_term},
           {'mailBody': search_term},
           {'mailFrom': '*%s*' % search_term}]

results = []
for group in groups:
    for query in queries:
        results.append(group.messages.find_email(query))

results = filter(None, results)
fresults = []
if results:
    # we need to do this because reduce isn't available to us
    fresults = results.pop()
    for result in results:
        fresults += result

return fresults
