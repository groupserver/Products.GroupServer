from zope.interface import implements
from OFS.OrderedFolder import OrderedFolder

from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from Products.XWFCore.XWFUtils import createRequestFromRequest, rfc822_date, assign_ownership

from App.config import getConfiguration

from interfaces import IGroupserverSite

import transaction
import datetime
import urlparse
from urllib import quote
import pathutil
import os.path

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

def init_user_folder( groupserver_site, initial_user, initial_password, 
                        email, canonicalHost, canonicalPort ):
    btf = groupserver_site.manage_addProduct['BTreeFolder2']
    btf.manage_addBTreeFolder( 'contacts', 'Contacts' )
    groupserver_site.manage_addFolder( 'contactsimages', 'People in the Site' )

    cuf = groupserver_site.manage_addProduct['CustomUserFolder']
    cuf.manage_addCustomUserFolder( 'contacts' )
    
    acl = getattr( groupserver_site, 'acl_users' )
    acl.userFolderAddGroup( 'example_site_member', 
                                'Membership of Example Site' )
    
    acl._doAddUser(initial_user, initial_password, [], [], [])
    adminuser = acl.getUser(initial_user)
    assert adminuser, 'Did not create the initial user'
    adminuser.manage_changeProperties(fn='Default Administrator')
    adminuser.add_defaultDeliveryEmailAddress(email)
    try:
        vid = 'AdminVerified%s' % email.replace('@', 'at')
        adminuser.add_emailAddressVerification(vid, email)
        adminuser.verify_emailAddress(vid)
        m = 'init_user_folder: Verified initial user email address %s' % email
        log.info(m)
    except:
        m = 'init_user_folder: Issues verifying initial user email address %s' % email
        log.error(m)
    acl.addGroupsToUser(['example_site_member'], adminuser.getId())
    

    acl._doAddUser('example_user', 'fake', [], [], [])
    exampleuser = acl.getUser('example_user')
    assert exampleuser, 'Did not create the example user'
    example_address = 'example_user@%s' % canonicalHost
    exampleuser.manage_changeProperties(fn='Example User')
    exampleuser.add_defaultDeliveryEmailAddress(example_address)
    try:
        vid = 'AdminVerified%s' % example_address.replace('@', 'at')
        exampleuser.add_emailAddressVerification(vid, example_address)
        exampleuser.verify_emailAddress(vid)
        m = 'init_user_folder: Verified example user email address %s' % example_address
        log.info(m)
    except:
        m = 'init_user_folder: Issues verifying example user email address %s' % example_address
        log.error(m)
    acl.addGroupsToUser(['example_site_member'], exampleuser.getId())
        
    cc = groupserver_site.manage_addProduct['CookieCrumbler']
    cc.manage_addCC('cookie_authentication')
    
    cookies = getattr( groupserver_site, 'cookie_authentication' )
    cookies.manage_changeProperties( auto_login_page='Content/login.html',
                                     unauth_page='Content/login.html',
                                     logout_page='Content/logout.html' )
    
    contacts = getattr( groupserver_site, 'contacts' )
    contacts.manage_permission( 'Manage properties', ('Owner','Manager'), acquire=1 )
    

    # --=mpj17=-- The example_site is created as a side-effect of
    # importing the content of the GroupServer instance (see the
    # ``init_content`` method, and the "big ugly hack" comment below).
    # This is bad in so many ways that it would take an essay to 
    # document them all. However, time is scarce, so rather than fix
    # the problem I am documenting it: configure the example site here.
    # *sigh*.
    example_site = getattr(groupserver_site.Content, 'example_site')
    example_site.manage_addLocalRoles(adminuser.getId(), ['DivisionAdmin'])
    site_config = getattr(groupserver_site.Content.example_site, 'DivisionConfiguration')
    site_config.manage_changeProperties(canonicalHost=canonicalHost)
    if not(hasattr(site_config, 'canonicalPort')):
        site_config.manage_addProperty('canonicalPort', canonicalPort, 
                                        'string')
    else:
        site_config.manage_changeProperties(canonicalPort=canonicalPort)

def init_global_configuration( groupserver_site, siteName, supportEmail,
                                timezone):
    cp = groupserver_site.manage_addProduct['CustomProperties']
    cp.manage_addCustomProperties( 'GlobalConfiguration', 'The global configuration for the Site' )
    gc = getattr(groupserver_site, 'GlobalConfiguration')
    gc.manage_addProperty('alwaysShowMemberPhotos', True, 'boolean')
    gc.manage_addProperty('showEmailAddressTo', 'request', 'string')
    gc.manage_addProperty('supportEmail', supportEmail, 'string')
    gc.manage_addProperty('timezone', timezone, 'string')
    
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

def import_content( container ):
    # --=rrw=-- big ugly hack
    from Products.GroupServer import pathutil
    
    container.manage_addProduct['MailHost'].manage_addMailHost('MailHost',
                                                                smtp_host='localhost')   
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
    getattr(site, 'admindivision').manage_changeProperties(title='Administer Site')
    fss.manage_addDirectoryView( pathutil.get_groupserver_path('help'), 'help' )
    assert hasattr(site.aq_explicit, 'help')
    getattr(site, 'help').manage_changeProperties(title='Help')

def init_group ( container, initial_user ):
    site = getattr(container.Content, 'example_site')
    assert site, 'No example_site found' 
    group = create_group(site, initial_user)
    assert group, 'No example_group found'
    site.acl_users.addGroupsToUser(['example_group_member'], 'example_user')

def create_group( site, initial_user ):
    groups = getattr(site, 'groups')
    group = site.Scripts.forms.start_a_group.create.group_folder(groups, 'example_group', 'Example Group',
                                       'example people', 'standard')
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
    groupList = site.Scripts.forms.start_a_group.create.list_instance(group, mailHost, site.getId(), 'public')
    create_default_administrator(group, initial_user)

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
    #   The group needs to be 'owned' by a top level user, since the Scripts are
    #   above the context of the site, and some of them require Manager level
    #   proxy access. Yes, this is darker magic than we'd like. Any suggestions
    #   welcome.
    assign_ownership(group, 'admin', 1, '/acl_users')
    assign_ownership(groupList, 'admin', 1, '/acl_users')
    return group

def create_default_administrator(group, adminUserId):
    assert group
    user = group.acl_users.getUser(adminUserId)
    assert user
    user.add_groupWithNotification('%s_member' % group.getId())
    group.manage_addLocalRoles(user.getId(), ['GroupAdmin'])
    return

def manage_addGroupserverSite(  container, id, title, 
                                initial_user, initial_password,
                                support_email, timezone, 
                                canonicalHost, canonicalPort,
                                databaseHost, databasePort,
                                databaseUsername, databasePassword,
                                databaseName, REQUEST=None ):
    """ Add a Groupserver Site object to a given container.
    
    """
    id = container._setObject( id, GroupserverSite( id, title ) )
    transaction.commit()
    
    gss = getattr( container, id )

    init_db_connection( gss, databaseHost, databasePort, databaseUsername, databasePassword, databaseName )

    init_catalog( gss )
    transaction.commit()

    init_id_factory( gss )
    transaction.commit()

    init_file_library( gss )
    transaction.commit()
    
    import_content( gss )
    transaction.commit()
    
    init_user_folder( gss, initial_user, initial_password, 
                        support_email, canonicalHost, canonicalPort )
    transaction.commit()

    init_fs_presentation( gss )
    transaction.commit()

    init_fs_scripts( gss )
    transaction.commit()

    init_global_configuration( gss, title, support_email, timezone )
    transaction.commit()

    init_group( gss, initial_user )
    transaction.commit()
                               
    if REQUEST is None:
        return
    
    REQUEST.RESPONSE.redirect( REQUEST['URL1'] + '/manage_main' )

manage_addGroupserverSiteForm = PageTemplateFile( 
    'management/manage_addGroupserverSiteForm.zpt', 
    globals(), __name__='manage_addGroupserverSiteForm' )
