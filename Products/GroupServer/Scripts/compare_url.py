## Script (Python) "compare_url"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=caller, url, exact_match=0
##title=
##
request = context.REQUEST

final_path = request.URL0.split(request.BASE0)[1].split('/')[1:]
virt_path = list(getattr(request, 'VirtualRootPhysicalPath', []))

curr_path = filter(None, virt_path+final_path)
nice_url = filter(None, virt_path+str(url).split('/'))

if exact_match:
    return int(curr_path == nice_url)
else:
    for i in range(len(nice_url)):
        if i == 0:
            match = curr_path == nice_url
        else:
            match = curr_path[:-i] == nice_url
        if match:
            return 1
    return 0
