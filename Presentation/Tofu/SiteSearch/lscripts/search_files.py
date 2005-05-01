## Script (Python) "search_files"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=groups, query
##title=
##
queries = [{'title': query}, {'dc+Description': query}, {'dc+Creator': query}]

results = []
for group in groups:
    for query in queries:
        try:
            results.append(group.files.find_files(query, -1))
        except:
            pass

results = filter(None, results)
fresults = []
if results:
    # we need to do this because reduce isn't available to us
    fresults = results.pop()
    for result in results:
        fresults += result

nfresults = []
for result in fresults:
    try:
        context.restrictedTraverse(result.getObject().getProperty('virtual_path')[0])
        nfresults.append(result)
    except:
        pass

return nfresults
