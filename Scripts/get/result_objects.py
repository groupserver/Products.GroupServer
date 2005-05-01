## Script (Python) "result_objects"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##
REQUEST = context.REQUEST

user = REQUEST.AUTHENTICATED_USER

results_object = getattr(user, 'Results', None)
if not results_object:
    return []

result_objects = results_object.objectValues()

if not result_objects:
    return []

now = DateTime()

results = []
for result in result_objects:
    if getattr(result, 'is_result', 1):
        release_date = getattr(result, 'release_date', 0)
        if release_date and int(DateTime(release_date)) <= int(now):
            results.append(result)

return results

print map(lambda x: x.absolute_url(), results)
return printed
