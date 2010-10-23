# coding=utf-8
import transaction, datetime, urlparse, pathutil, os.path
from urllib import quote
from zope.interface import implements
from zope.component import createObject
from OFS.OrderedFolder import OrderedFolder
from App.config import getConfiguration
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from Products.XWFCore.XWFUtils import createRequestFromRequest, \
    rfc822_date, assign_ownership
from Products.GSProfile.utils import create_user_from_email
from Products.GSGroupMember.groupmembership import join_group
from interfaces import IGroupserverSite

import logging
log = logging.getLogger('GroupServer Site')

class GroupserverSite( OrderedFolder ):
    implements( IGroupserverSite )
    
    meta_type = 'Groupserver Site'
    
    def __init__( self, id, title='' ):
        OrderedFolder.__init__( self, id )
        self.title = title
    
    def get_site( self ):
        """ Return ourself.
        
        """
        return self
    
    site_root = get_site
    
    def setAuthCookie(self, resp, cookie_name, cookie_value):
        """ Persistent authentication cookie support.
        
        """
        if self.REQUEST.form.get('__ac_persistent', 0):
            expires = rfc822_date(datetime.datetime.utcnow() +
                                  datetime.timedelta(365))
            resp.setCookie(cookie_name, cookie_value, path=self.cookie_authentication.getCookiePath(), expires=expires)
        else:
            resp.setCookie(cookie_name, cookie_value, path=self.cookie_authentication.getCookiePath())

    def getRealContext(self):
        request = self.REQUEST
        path = tuple(filter(None, urlparse.urlsplit(request.URL1)[2].split('/')))
        virtual_path = request.get('VirtualRootPhysicalPath', ())
        
        path = virtual_path + path
        
        context = self.unrestrictedTraverse(path)
        
        return context
        
    def index_html( self ):
        """ Return the default view
        
        """
        redirect = self.REQUEST.RESPONSE.redirect
                
        redirectFile = ''
        # ---=mpj17=---
        # If there is a content_en.xml file, then we are working with a
        #   Five GSContent folder, so call index.html. Otherwise call
        #   the ol' Zope 2 index.xml page template
        context = self.getRealContext()

        if (hasattr(context.aq_explicit, 'content_en.xml') 
            or hasattr(context.aq_explicit, 'content_en')):
            redirectFile = 'index.html'
        else:
            redirectFile = 'index.xml'

        # ---=mpj17=--- Now construct the URL
        url = '/'.join((self.REQUEST.URL1, redirectFile))
        request =  createRequestFromRequest(self.REQUEST)
        if len(request) > 0:
            url = '?'.join((url, request))
        
        return redirect(url, lock=1)
    
    def standard_error_message( self, **kw ):
        """ Override the default standard_error_message.
        
        """
        request = self.REQUEST
        context = self.getRealContext()
        if kw['error_type'] == 'NotFound':
            URL = request.get('URL','')
            HTTP_REFERRER = request.get('HTTP_REFERER','')
            m = '404: Link from <%s> to <%s> is broken.' % (HTTP_REFERRER, URL)
            q = quote(URL)
            r = quote(HTTP_REFERRER)
            log.warn(m)
            uri = '/new_not_found.html?q=%s&r=%s'  %(q, r)
            request.RESPONSE.redirect(uri, lock=1)
        # ignore these types
        elif kw['error_type'] in ('Forbidden',):
            pass
        else:
            request.RESPONSE.redirect('unknown_error.html', lock=1)
        
        raise

def create_user(groupserver_site, email, fn, password):
    user = create_user_from_email(groupserver_site, email)
    user.manage_changeProperties(fn=fn)
    user.set_password(password, updateCookies=False)
    try:
        vid = 'AssumedTrue%s' % email.replace('@', 'at')
        user.add_emailAddressVerification(vid, email)
        user.verify_emailAddress(vid)
        m = 'init_user_folder: Verified the address <%s> for %s (%s).' %\
            (email, fn, user.getId())
        log.info(m)
    except:
        m = 'init_user_folder: Issues verifying the address <%s> for '\
            '%s (%s).' % (email, fn, user.getId())
        log.error(m)
    return user

def init_user_folder( groupserver_site, admin_email, admin_password,
        user_email, user_password, support_email, canonicalHost, 
        canonicalPort ):
    btf = groupserver_site.manage_addProduct['BTreeFolder2']
    btf.manage_addBTreeFolder( 'contacts', 'Contacts' )
    # --=mpj17=-- Do we need contactsimages? 
    #       groupserver_site.manage_addFolder( 'contactsimages', 'People in the Site' )
    # The contacts folder stores the user-data.
    cuf = groupserver_site.manage_addProduct['CustomUserFolder']
    cuf.manage_addCustomUserFolder( 'contacts' )
    contacts = getattr( groupserver_site, 'contacts' )
    contacts.manage_permission( 'Manage properties', ('Owner','Manager'), acquire=1 )
    # Cookie Crumbler logs people in
    cc = groupserver_site.manage_addProduct['CookieCrumbler']
    cc.manage_addCC('cookie_authentication')
    cookies = getattr( groupserver_site, 'cookie_authentication' )
    cookies.manage_changeProperties( auto_login_page='Content/login.html',
                                     unauth_page='Content/login.html',
                                     logout_page='Content/logout.html' )
    
    # Create the default members of the site.    
    egSiteMember = 'example_site_member'
    acl = getattr( groupserver_site, 'acl_users' )
    acl.userFolderAddGroup( egSiteMember, 'Membership of Example Site' )
    # The admin.
    admin = create_user(groupserver_site, admin_email, 
                u'GroupServer Administrator', admin_password)
    acl.addGroupsToUser([egSiteMember], admin.getId())
    # The normal user
    user = create_user(groupserver_site, user_email, u'GroupServer User',
                    user_password)
    acl.addGroupsToUser([egSiteMember], user.getId())

    # --=mpj17=-- The example_site is created as a side-effect of
    # importing the content of the GroupServer instance (see the
    # ``init_content`` method, and the "big ugly hack" comment below).
    # This is bad in so many ways that it would take an essay to 
    # document them all. However, time is scarce, so rather than fix
    # the problem I am documenting it: configure the example site here.
    # *sigh*.
    example_site = getattr(groupserver_site.Content, 'example_site')
    example_site.manage_addLocalRoles(admin.getId(), ['DivisionAdmin'])
    example_site.manage_addLocalGroupRoles(egSiteMember, ('DivisionMember',))
    site_config = getattr(groupserver_site.Content.example_site,
                    'DivisionConfiguration')
    site_config.manage_changeProperties(canonicalHost=canonicalHost)
    if not(hasattr(site_config, 'canonicalPort')):
        site_config.manage_addProperty('canonicalPort', canonicalPort, 
                                        'string')
    else:
        site_config.manage_changeProperties(canonicalPort=canonicalPort)

def init_global_configuration( groupserver_site, siteName, supportEmail,
                                timezone, canonicalHost):
    cp = groupserver_site.manage_addProduct['CustomProperties']
    cp.manage_addCustomProperties( 'GlobalConfiguration', 'The global configuration for the Site' )
    gc = getattr(groupserver_site, 'GlobalConfiguration')
    gc.manage_addProperty('alwaysShowMemberPhotos', True, 'boolean')
    gc.manage_addProperty('showEmailAddressTo', 'request', 'string')
    gc.manage_addProperty('supportEmail', supportEmail, 'string')
    gc.manage_addProperty('timezone', timezone, 'string')
    gc.manage_addProperty('emailDomain', canonicalHost, 'string')
    
def init_fs_presentation( groupserver_site ):
    fss = groupserver_site.manage_addProduct['FileSystemSite']
    fss.manage_addDirectoryView( pathutil.get_groupserver_path('Presentation'), 'Presentation' )
    groupserver_site.manage_addFolder('PresentationCustom', 'Site specific presentation customisation')
    pc = getattr(groupserver_site, 'PresentationCustom')
    pc.manage_addFolder('Tofu', 'Choose Your Own Flavor')
    tofu = getattr(pc, 'Tofu')
    tofu.manage_addFolder('Common', 'Common Style')
    common = getattr(tofu, 'Common')
    common.manage_addFolder('css', 'Cascading Style Sheets')
    css = getattr(common, 'css')
    css.manage_addDTMLMethod('globalstyle.css', 'Custom Stylesheet')
    
def init_fs_scripts( groupserver_site ):
    fss = groupserver_site.manage_addProduct['FileSystemSite']
    fss.manage_addDirectoryView( pathutil.get_groupserver_path('Scripts'), 'Scripts' )
    groupserver_site.manage_addFolder('LocalScripts', 'Site specific scripts')

def init_file_library( groupserver_site ):
    fl = groupserver_site.manage_addProduct['XWFFileLibrary2']
    fl.manage_addXWFFileLibrary2( 'FileLibrary2' )
    
    file_library = getattr( groupserver_site, 'FileLibrary2' )
    fls = file_library.manage_addProduct['XWFFileLibrary2']
    fls.manage_addXWFFileStorage2( 'storage' )
    
def init_id_factory( groupserver_site ):
    xif = groupserver_site.manage_addProduct['XWFIdFactory']
    xif.manage_addXWFIdFactory( 'IdFactory' )
    
def init_catalog( groupserver_site ):
    groupserver_site.manage_addProduct['XWFCore'].manage_addXWFCatalog( 'Catalog' )
    catalog = getattr( groupserver_site, 'Catalog' )
    
    catalogEntries = ( 'content_type', 'dc_creator', 'group_ids', 'id', 
      'indexable_summary', 'meta_type', 'modification_time', 'size', 'tags', 
      'title', 'topic' )
    
    keysToAdd = {
      'allowedRolesAndUsers'  : 'KeywordIndex', 
      'content_type'          : 'FieldIndex', 
      'dc_creator'            : 'FieldIndex', 
      'group_ids'             : 'KeywordIndex', 
      'id'                    : 'FieldIndex', 
      'indexable_content'     : 'ZCTextIndex', 
      'meta_type'             : 'FieldIndex', 
      'modification_time'     : 'DateIndex', 
      'tags'                  : 'KeywordIndex', 
      'title'                 : 'FieldIndex', 
      'topic'                 : 'FieldIndex', 
      'dc_description'        : 'ZCTextIndex', 
      'dc_title'              : 'KeywordIndex', 
      'dc_valid'              : 'DateIndex', 
      'linked_resources'      : 'KeywordIndex', 
      'path'                  : 'PathIndex', 
      'resource_locator'      : 'KeywordIndex', 
    }
    
    for key in keysToAdd.keys():
        try:
            catalog.manage_addIndex( key, keysToAdd[key] )
        except:
            # The key is already in the index
            pass
    
    for catalogEntry in catalogEntries:
        try:
            catalog.manage_addColumn( key )
        except:
            # The key is already in the column
            pass

def init_db_connection( container, databaseHost, databasePort, databaseUsername, databasePassword, databaseName ):
    databasePort = int(databasePort)
    assert databasePort != 0

    container.manage_addProduct['ZSQLAlchemy'].manage_addZSQLAlchemy('zsqlalchemy')
    container.zsqlalchemy.manage_changeProperties(dbtype='postgres',
                                                  hostname=databaseHost,
                                                  port=databasePort,
                                                  username=databaseUsername,
                                                  password=databasePassword,
                                                  database=databaseName)

def init_smtp_host( container, smtp_host, smtp_port, smtp_user, smtp_password):
    '''Initalise SMTP Hosts
    
    Create the MailHost instance that will communicate to the SMTP host
    in order to send the GroupServer notifications, and configure the
    MailHost used to send posts from groups.'''
    mailHostId = 'MailHost'
    
    container.manage_addProduct['MailHost'].manage_addMailHost(mailHostId)
    notificationsMailHost = getattr(container, mailHostId)
    notificationsMailHost.manage_makeChanges(
        title='Notifications SMTP Settings',
        smtp_host=smtp_host, smtp_port=smtp_port, smtp_uid=smtp_user,
        smtp_pwd=smtp_password, REQUEST=None)
    
    listManager = getattr(container.site_root(), 'ListManager')
    listManager.manage_addProduct['MailHost'].manage_addMailHost(mailHostId)
    listMailHost = getattr(listManager, mailHostId)
    listMailHost.manage_makeChanges(
        title='Mail List SMTP Settings',
        smtp_host=smtp_host, smtp_port=smtp_port, smtp_uid=smtp_user,
        smtp_pwd=smtp_password, REQUEST=None)
    
def import_content( container ):
    # --=rrw=-- big ugly hack
    from Products.GroupServer import pathutil
        
    objects_to_import = ['CodeTemplates.zexp', 'Content.zexp', 'GroupProperties.zexp',
                         'ListManager.zexp', 'Templates.zexp']
    for object_to_import in objects_to_import:
        container._importObjectFromFile( pathutil.get_import_path(
                                             object_to_import) )

    site = getattr(container.Content, 'example_site')
    assert site, 'No example_site found'
    fss = site.manage_addProduct['FileSystemSite']
    
    fss.manage_addDirectoryView( pathutil.get_groupserver_path('admindivision'), 'admindivision' )
    assert hasattr(site.aq_explicit, 'admindivision')
    adminDivision = getattr(site, 'admindivision')
    adminDivision.manage_changeProperties(title='Administer Site')
    adminSitePerms = ['DivisionAdmin', 'Manager', 'Owner']
    adminDivision.manage_permission('View',
        adminSitePerms, acquire=0)
    adminDivision.manage_permission('Access contents information',
        adminSitePerms, acquire=0)
    
    fss.manage_addDirectoryView( pathutil.get_groupserver_path('help'), 'help' )
    assert hasattr(site.aq_explicit, 'help')
    getattr(site, 'help').manage_changeProperties(title='Help')

def init_group ( container, admin_email, user_email, zope_admin_id ):
    site = getattr(container.Content, 'example_site')
    assert site, 'No example_site found' 
    groupInfo = create_group(site, zope_admin_id)

    acl_users = container.site_root().acl_users
    
    admin = acl_users.get_userByEmail(admin_email)
    join_group(admin, groupInfo)
    groupInfo.groupObj.manage_addLocalRoles(admin.getId(), ['GroupAdmin'])

    user = acl_users.get_userByEmail(user_email)
    join_group(user, groupInfo)

def init_vhm( canonicalHost, container ):
    vhm = getattr(container, 'virtual_hosting')
    sitePath = '/'.join(container.getPhysicalPath())[1:]
    newMap = '%s/%s/Content/example_site' % \
      (canonicalHost, sitePath)
    lines = list(vhm.lines)
    lines.append(newMap)
    mapText = '\n'.join(lines)
    vhm.set_map(mapText, None)

def create_group( site, zope_admin_id ):
    groups = getattr(site, 'groups')
    group = site.Scripts.forms.start_a_group.create.group_folder(groups,
                'example_group', 'Example Group', 'example people', 
                'standard')
    assert group, 'No group found'
    site.Scripts.forms.start_a_group.create.group_index(group)
    site.Scripts.forms.start_a_group.create.javascript(group)
    site.Scripts.forms.start_a_group.create.files_area(group)
    site.Scripts.forms.start_a_group.create.messages_area(group)
    site.Scripts.forms.start_a_group.create.charter(group, 'standard')
    site.Scripts.forms.start_a_group.create.email_settings(group)
    site.Scripts.forms.start_a_group.create.administration(group)
    site.Scripts.forms.start_a_group.create.members_area(group)
    site.Scripts.forms.start_a_group.create.chat(group)

    canonicalHost = site.DivisionConfiguration.getProperty('canonicalHost')
    mailHost = canonicalHost
    groupList = site.Scripts.forms.start_a_group.create.list_instance(group, 
                    mailHost, site.getId(), 'public')
    assert groupList, 'No groupList found'

    # Set the permissions for the group.
    joinCondition = 'anyone'
    userGroups = ['Anonymous', 'Authenticated', 'DivisionMember',
                  'DivisionAdmin', 'GroupAdmin','GroupMember','Manager',
                  'Owner']
    group.manage_changeProperties(join_condition=joinCondition)
    group.manage_permission('View', userGroups)
    group.manage_permission('Access contents information', userGroups)

    # Set the messages and files to default, following the group.
    group.files.manage_permission('View', [], 1)
    group.files.manage_permission('Access contents information', [], 1)
    group.messages.manage_permission('View', [], 1)
    group.messages.manage_permission('Access contents information', [], 1)

    # Set the administration interface to site and group admins only
    adminGroups = ['DivisionAdmin', 'GroupAdmin', 'Manager', 'Owner']
    group.admingroup.manage_permission('View', adminGroups)
    group.admingroup.manage_permission('Access contents information', adminGroups)

    # Add the start date to the group
    curr_time = datetime.datetime.now()
    group.manage_addProperty('date_open', curr_time.strftime('%d %B %Y'), 'string')

    # --=rrw=--
    #   The group needs to be 'owned' by a top level user, since the
    #   Scripts are above the context of the site, and some of them
    #   require Manager level proxy access. Yes, this is darker magic
    #   than we'd like. Any suggestions welcome.
    assign_ownership(group, zope_admin_id, 1, '/acl_users')
    assign_ownership(groupList, zope_admin_id, 1, '/acl_users')

    groupInfo = createObject('groupserver.GroupInfo', group)
    return groupInfo

def manage_addGroupserverSite( container, id, title,
        admin_email, admin_password, user_email, user_password,
        zope_admin_id, support_email, timezone, canonicalHost,
        canonicalPort, smtp_host, smtp_port, smtp_user, smtp_password,
        databaseHost, databasePort, databaseUsername, databasePassword,
        databaseName, REQUEST=None ):
    """ Add a Groupserver Site object to a given container.
    
    """
    id = container._setObject( id, GroupserverSite( id, title ) )
    transaction.commit()
    
    gss = getattr( container, id )

    init_db_connection( gss, databaseHost, databasePort, 
        databaseUsername, databasePassword, databaseName )

    init_catalog( gss )
    transaction.commit()

    init_id_factory( gss )
    transaction.commit()

    init_file_library( gss )
    transaction.commit()
    
    import_content( gss )
    transaction.commit()
    
    init_smtp_host( gss, smtp_host, smtp_port, smtp_user, smtp_password )
    transaction.commit()
    
    init_user_folder( gss, admin_email, admin_password, 
        user_email, user_password, support_email, canonicalHost, 
        canonicalPort )
    transaction.commit()

    init_fs_presentation( gss )
    transaction.commit()

    init_fs_scripts( gss )
    transaction.commit()

    init_global_configuration( gss, title, support_email, 
                               timezone, canonicalHost )
    transaction.commit()

    init_group( gss, admin_email, user_email, zope_admin_id )
    transaction.commit()

    init_vhm( canonicalHost, gss )
    transaction.commit()
    
    if REQUEST is None:
        return
    
    REQUEST.RESPONSE.redirect( REQUEST['URL1'] + '/manage_main' )

manage_addGroupserverSiteForm = PageTemplateFile( 
    'management/manage_addGroupserverSiteForm.zpt', 
    globals(), __name__='manage_addGroupserverSiteForm' )
