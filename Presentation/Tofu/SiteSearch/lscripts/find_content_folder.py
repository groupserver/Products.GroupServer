## Script (Python) "find_content_folder"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=ucid
##title=
##
groups = context.Scripts.get.groups()

def process_folder(folder):
    url = folder.absolute_url()
    if getattr(folder, 'ucid', 0) == ucid:
        url = folder.absolute_url()
        return url
        
    for folder in folder.objectValues('XWF Virtual Folder'):
        url = process_folder(folder)
        if url:
            return url
    return ''
    
for group in groups:
    files = getattr(group, 'files', None)
    if not files: continue
    url = process_folder(files)
    if url: break
    
return url
