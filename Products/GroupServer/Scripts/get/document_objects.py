## Script (Python) "document_objects"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##
from Products.XWFCore.XWFUtils import deprecated
deprecated(context, script, "Remove all traces of 'Documents'.")

REQUEST = context.REQUEST
user = REQUEST.AUTHENTICATED_USER

documents_object = getattr(user, 'Documents', None) or getattr(user, 'documents', None)
if not documents_object:
    return []

document_objects = documents_object.objectValues()
if not document_objects:
    return []

now = DateTime()

documents = []
for result in document_objects:
    #if getattr(result, 'is_result', 1):
    #    release_date = getattr(result, 'release_date', 0)
    #    if release_date and int(DateTime(release_date)) <= int(now):
    documents.append(result)

def sort_documents(a,b):
    if a.title > b.title:
        return 1
    elif a.title < b.title:
        return -1
    else:
        return 0

documents.sort(sort_documents)

return documents
