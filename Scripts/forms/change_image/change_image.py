## Script (Python) "process_form"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=Change User's Image
##
if not form.get('submitted', False):
    return result

site_root = context.site_root
result = {}
user = context.REQUEST.AUTHENTICATED_USER
origimage = getattr(context.contactsimages, '%s.jpg' % user.getId(), None)
form = context.REQUEST.form
result['form'] = form
result['message'] = ""
fileData = form.get('fileData','')

# Try and delete the old tempory image, but don't worry if it is not there.
try:
  context.contactsimages.manage_delObjects(['%s.jpg_temp' % user.getId()])
except:
  pass

# Add the fileData to the "contactsimages" folder, as a tempory file
context.contactsimages.manage_addImage('%s.jpg_temp' % user.getId(), 
  fileData, '%s %s' % (user.getProperty('preferredName', ''), 
  user.getProperty('lastName', '')))
image = getattr(context.contactsimages, '%s.jpg_temp' % user.getId())

if (image.content_type != 'image/jpeg'):
  # The image is not a JPEG
  result['error'] = True
  result['message'] = '<p>Only JPEG images are allowed.</p>'

elif (image.width > 150 or image.height > 200):
  # The image is too big
  result['error'] = True
  msg = '''<p>Image size (%d&#215;%d) is too large: 150&#215;200 pixels is
    the argest allowed size</p>''' % (image.width, image.height)
  result['message'] = msg

else:
  # The image is ok

  if origimage: # Delete the old image, if it exists
    context.contactsimages.manage_delObjects([origimage.getId()])

  # Add the image for real this time.
  context.contactsimages.manage_addImage('%s.jpg' % user.getId(), 
  fileData, '%s %s' % (user.getProperty('preferredName', ''),
  user.getProperty('lastName', '')))
  context.contactsimages.manage_delObjects([image.getId()])
  # Try and delete the old tempory image, but don't worry if it is not there.
  try:
    context.contactsimages.manage_delObjects(['%s.jpg_temp' % user.getId()])
  except:
    pass

  result['message'] = '<p>The image has been successfully changed.</p>'

return result

