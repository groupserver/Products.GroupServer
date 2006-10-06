## Script (Python) "addPost"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=Add a Post to the Group
##

from Products.PythonScripts.standard import html_quote
#from zLOG import LOG, WARNING, PROBLEM, INFO

def tagProcess(tagsString):
    # --=mpj17=-- Not the most elegant function, but I did not want to
    #   use the regular-expression library.
    retval = []
    
    tagsString = tagsString.replace('\n', ' ')
    if len(tagsString) == 0:
        return retval

    if ',' in tagsString:
        retval = tagsString.split(',')
    else:
        tags = tagsString
        if (('"' in tags) and (tags.count('"') % 2 == 0)):
            newTags = ''
            inQuote = False
            for c in tags:
                if (c == '"') and (not inQuote):
                    inQuote = True
                elif (c == '"') and (inQuote):
                    inQuote = False
                elif (c == ' ') and inQuote:
                    newTags += '_'
                else:
                    newTags += c
                    tags = newTags

        tagsList = tags.split(' ')
        for tag in tagsList:
            retval.append(tag.replace('_', ' '))
    
    return map(lambda t: t.strip(), filter(lambda t: t!='', retval))

result = {}

form = context.REQUEST.form
assert form.has_key('groupId')
assert form.has_key('siteId')
assert form.has_key('replyToId')
assert form.has_key('topic')
assert form.has_key('message')
assert form.has_key('tags')
assert form.has_key('email')
assert form.has_key('file')
result['form'] = form

# --=mpj17=-- Do not, under *A*N*Y* circumstances, strip the file.
for field in ['replyToId', 'topic', 'message', 'tags', 'email']:
    # No really: do not strip the file.
    try:
        form[field] = form[field].strip()
    except AttributeError:
        pass

groupId = form.get('groupId')
siteId = form.get('siteId')
replyToId = form.get('replyToId', '')
topic = form.get('topic', '')
message = form.get('message', '').replace('\r', '')
tags = tagProcess(form.get('tags', ''))
tagsString = ', '.join(tags)
email = form.get('email', '').replace('\r', '')
uploadedFile = form.get('file', '')

site_root = context.site_root()
assert site_root
user = context.REQUEST.AUTHENTICATED_USER
assert user

siteObj = getattr(site_root.Content, siteId)
groupObj = getattr(siteObj.groups, groupId)
ptnCoachId = groupObj.getProperty('ptn_coach_id', '')
canonicalHost = context.Scripts.get.option('canonicalHost',
                                             'onlinegroups.net')
host = context.Scripts.get.option('canonicalHost', 'onlinegroups.net')
messages = getattr(groupObj, 'messages')
assert messages
files = getattr(groupObj, 'files')
assert files
listManager = messages.get_xwfMailingListManager()
assert listManager
groupList = getattr(listManager, groupObj.getId())
assert groupList

if replyToId:
    origEmail = messages.get_email(replyToId)
    topic = origEmail.getProperty('mailSubject')
    subject = 'Re: %s'  % topic
    emailMessageReplyToId = origEmail.getProperty('message-id', '')
    # --=mpj17=-- I should really handle the References header here.
else:
    subject = topic
    emailMessageReplyToId = ''

# Step 1, check if the user is blocked
blocked_members = groupList.getProperty('blocked_members')
if blocked_members and user.getId() in blocked_members:
    message = 'Blocked user: %s from posting via web' % user.getId()
    LOG('XWFVirtualMailingListArchive', PROBLEM, message)
    m = 'You are currently blocked from posting. Please contact the group administrator'
    raise 'Forbidden', m

# Step 2, check the moderation
moderatedlist = groupList.getValueFor('moderatedlist')
moderated = groupList.getValueFor('moderated')
via_mailserver = False
# --=rrw=--if we are moderated _and_ we have a moderatedlist, only
# users in the moderated list are moderated
if moderated and moderatedlist:
    for address in user.get_emailAddresses():
        if address in moderatedlist:
            #LOG('XWFVirtualMailingListArchive', INFO,
            #    'User "%s" posted from web while moderated' % user.getId())
            via_mailserver = True
            break
# --=rrw=-- otherwise if we are moderated, everyone is moderated
elif moderated:
    #LOG('XWFVirtualMailingListArchive', INFO,
    #    'User "%s" posted from web while moderated' % user.getId())
    via_mailserver = True

# Step 3, Create the file object, if necessary
fileObj = None
if uploadedFile:
    fileProperties = {'topic': topic,
                      'tags': tags,
                      'dc_creator': user.getId(),
                      'description': message[:200]}
    fileObj = files.add_file(uploadedFile, fileProperties)

# Step 3, Get the templates
templateDir = site_root.Templates.email.notifications.new_file
messageTemplate = templateDir.message

for list_id in messages.getProperty('xwf_mailing_list_ids', []):
    curr_list = listManager.get_list(list_id)
    m = messageTemplate(context.REQUEST, list_object=curr_list,
                        user=user, from_addr=email,
                        subject=subject, tags=tagsString,
                        canonicalHost=canonicalHost,
                        group=groupObj, ptn_coach_id=ptnCoachId,
                        message=message,
                        reply_to_id=emailMessageReplyToId,
                        n_type='new_file', n_id=groupObj.getId(),
                        file=fileObj)
    if via_mailserver:
        listManager.MailHost.send(m)
    else:
        groupList.manage_listboxer({'Mail': m})

if groupObj.Scripts.get.option('virtualSitesOnly', False):
    h = '/groups/%s/messages/' % groupObj.getId()
else:
    h = '/%s/groups/%s/messages/' % (siteObj.getId(), groupObj.getId())
context.REQUEST.RESPONSE.redirect(h)

