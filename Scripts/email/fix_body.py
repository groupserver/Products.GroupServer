## Script (Python) "fix_body"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=body=''
##title=
##
try:
    ord(body[0])
except:
    return body
    
a = ''

for x in body:
    if ord(x) > 127:
        a += "'"
    elif ord(x) == 38:
        a += '&amp;'
    elif ord(x) == 60:
        a += '&lt;'
    elif ord(x) == 62:
        a += '&gt;'
    else:
        a += x

return a
