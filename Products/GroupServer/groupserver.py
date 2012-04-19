# coding=utf-8
from traceback import format_exc
import transaction, datetime, urlparse, pathutil, os.path
from urllib import quote
from zope.interface import implements
from zope.component import createObject
from zExceptions import BadRequest
from OFS.OrderedFolder import OrderedFolder
from App.config import getConfiguration
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from Products.XWFCore.XWFUtils import createRequestFromRequest, \
    rfc822_date
from Products.GSProfile.utils import create_user_from_email
from gs.profile.email.verify.emailverificationuser import EmailVerificationUser
from gs.profile.password.passworduser import PasswordUser
from gs.group.member.join.joininguser import JoiningUser
from gs.group.start.groupcreator import MoiraeForGroup
from interfaces import IGroupserverSite

import logging
log = logging.getLogger('GroupServer Site')

def mumble_exists_mumble(function, thing):
    log.warning('%s: "%s" already exists.' % (function, thing))
    log.warning('%s: Carrying on regardless.' % function)

SITE_ID = 'initial_site' # FIX

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
            URL = request.get('URL','')
            q = quote(URL)
            formatedError = format_exc()
            eggs = 'eggs/'
            e = ''
            for line in formatedError.split('\n'):
                if eggs in line:
                    e += '  %s' % line.split(eggs)[1]
                else:
                    e += line
                e += '\n'
            t = ((len(e) > 1536) and (e[:256] +'\nsnip...\n'+e[-1024:])) or e
            m = quote(t)
            uri = '/new_unexpected_error.html?q=%s&m=%s' % (q, m)
            request.RESPONSE.redirect(uri, lock=1)
        raise # Propogate the error up.

def create_user(site, email, fn, password):
    user = create_user_from_email(site, email)
    user.manage_changeProperties(fn=fn)
    # We want the userInfo in the context of the site
    ui = createObject('groupserver.UserFromId', site, user.getId())
    pu = PasswordUser(ui)
    pu.set_password(password)
    try:
        vid = 'AssumedTrue%s' % email.replace('@', 'at')
        evu = EmailVerificationUser(site, ui, email)
        evu.add_verification_id(vid)
        evu.verify_email(vid)
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
    try:
        btf.manage_addBTreeFolder( 'contacts', 'Contacts' )
    except BadRequest, br:
        mumble_exists_mumble('init_user_folder', 'contacts')
    
    # The contacts folder stores the user-data.
    cuf = groupserver_site.manage_addProduct['CustomUserFolder']
    try:
        cuf.manage_addCustomUserFolder( 'contacts' )
    except BadRequest, br:
        mumble_exists_mumble('init_user_folder', 'acl_users')
        
    contacts = getattr( groupserver_site, 'contacts' )
    contacts.manage_permission( 'Manage properties', ('Owner','Manager'), acquire=1 )

    # Cookie Crumbler logs people in
    cc = groupserver_site.manage_addProduct['CookieCrumbler']
    try:
        cc.manage_addCC('cookie_authentication')
    except BadRequest, br:
        mumble_exists_mumble('init_user_folder', 'cookie_authentication')
        
    cookies = getattr( groupserver_site, 'cookie_authentication' )
    cookies.manage_changeProperties( auto_login_page='Content/login.html',
                                     unauth_page='Content/login.html',
                                     logout_page='Content/logout.html' )
    
    # Create the user-group for the site.
    egSiteMember = '%s_member' % SITE_ID
    acl = getattr( groupserver_site, 'acl_users' )
    try:
        acl.userFolderAddGroup( egSiteMember, 'Membership of Example Site' )
    except ValueError, ve:
        u = 'User group %s' % egSiteMember
        mumble_exists_mumble('init_user_folder',  u)

    # --=mpj17=-- The initial site is created as a side-effect of
    # importing the content of the GroupServer instance (see the
    # ``init_content`` method, and the "big ugly hack" comment below).
    # This is bad in so many ways that it would take an essay to 
    # document them all. However, time is scarce, so rather than fix
    # the problem I am documenting it: configure the example site here.
    # *sigh*.
    example_site = getattr(groupserver_site.Content, SITE_ID)
    example_site.manage_addLocalGroupRoles(egSiteMember, ('DivisionMember',))
    # Ok, now we are configuring the site. *sigh*
    site_config = getattr(example_site, 'DivisionConfiguration')
    site_config.manage_changeProperties(canonicalHost=canonicalHost)
    if not(hasattr(site_config, 'canonicalPort')):
        site_config.manage_addProperty('canonicalPort', canonicalPort, 
                                        'string')
    else:
        site_config.manage_changeProperties(canonicalPort=canonicalPort)

    # The admin.
    admin = create_user(example_site, admin_email, 
                u'GroupServer Administrator', admin_password)
    example_site.manage_addLocalRoles(admin.getId(), ['DivisionAdmin'])
    # The normal user
    user = create_user(example_site, user_email, u'GroupServer User',
                    user_password)

def init_global_configuration( groupserver_site, siteName, supportEmail,
                                timezone, canonicalHost):
    cp = groupserver_site.manage_addProduct['CustomProperties']
    try:
        cp.manage_addCustomProperties( 'GlobalConfiguration', 
            'The global configuration for the Site' )
    except BadRequest, br:
        mumble_exists_mumble('init_global_configuration', 'GlobalConfiguration')
        log.warning('init_global_configuration: Not configuring "GlobalConfiguration"')
    else:
        gc = getattr(groupserver_site, 'GlobalConfiguration')
        gc.manage_addProperty('alwaysShowMemberPhotos', True, 'boolean')
        gc.manage_addProperty('showEmailAddressTo', 'request', 'string')
        gc.manage_addProperty('supportEmail', supportEmail, 'string')
        gc.manage_addProperty('timezone', timezone, 'string')
        gc.manage_addProperty('emailDomain', canonicalHost, 'string')
    
def init_fs_presentation( groupserver_site ):
    # TODO: --mpj17=-- Drop Presentation
    fss = groupserver_site.manage_addProduct['FileSystemSite']
    try:
        fss.manage_addDirectoryView( pathutil.get_groupserver_path('Presentation'), 'Presentation' )
    except BadRequest, br:
        mumble_exists_mumble('init_fs_presentation', 'Presentation')
        
    try:
        groupserver_site.manage_addFolder('PresentationCustom', 'Site specific presentation customisation')
    except BadRequest, br:
        mumble_exists_mumble('init_fs_presentation', 'PresentationCustom')
    pc = getattr(groupserver_site, 'PresentationCustom')
    try:
        pc.manage_addFolder('Tofu', 'Choose Your Own Flavor')
    except BadRequest, br:
        mumble_exists_mumble('init_fs_presentation', 'Tofu')
    tofu = getattr(pc, 'Tofu')
    try:
        tofu.manage_addFolder('Common', 'Common Style')
    except BadRequest, br:
        mumble_exists_mumble('init_fs_presentation', 'Common')
    common = getattr(tofu, 'Common')
    try:
        common.manage_addFolder('css', 'Cascading Style Sheets')
    except BadRequest, br:
        mumble_exists_mumble('init_fs_presentation', 'css')
    css = getattr(common, 'css')
    try:
        css.manage_addDTMLMethod('globalstyle.css', 'Custom Stylesheet')
    except BadRequest, br:
        mumble_exists_mumble('init_fs_presentation', 'globalstyle.css')
    
def init_fs_scripts( groupserver_site ):
    fss = groupserver_site.manage_addProduct['FileSystemSite']
    try:
        fss.manage_addDirectoryView( pathutil.get_groupserver_path('Scripts'), 'Scripts' )
    except BadRequest, br:
        mumble_exists_mumble('init_fs_scripts', 'Scripts')
    try:
        groupserver_site.manage_addFolder('LocalScripts', 'Site specific scripts')
    except BadRequest, br:
        mumble_exists_mumble('init_fs_scripts', 'LocalScripts')

def init_file_library( groupserver_site ):
    fl = groupserver_site.manage_addProduct['XWFFileLibrary2']
    try:
        fl.manage_addXWFFileLibrary2( 'FileLibrary2' )
    except BadRequest, br:
        mumble_exists_mumble('init_file_library', 'FileLibrary2')
    
    file_library = getattr( groupserver_site, 'FileLibrary2' )
    fls = file_library.manage_addProduct['XWFFileLibrary2']
    try:
        fls.manage_addXWFFileStorage2( 'storage' )
    except BadRequest, br:
        mumble_exists_mumble('init_file_library', 'FileLibrary2/storage')
    
def init_id_factory( groupserver_site ):
    xif = groupserver_site.manage_addProduct['XWFIdFactory']
    try:
        xif.manage_addXWFIdFactory( 'IdFactory' )
    except BadRequest, br:
        mumble_exists_mumble('init_id_factory', 'IdFactory')
    
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

    try:
        container.manage_addProduct['ZSQLAlchemy'].manage_addZSQLAlchemy('zsqlalchemy')
    except BadRequest, br:
        mumble_exists_mumble('init_db_connection', 'zsqlalchemy')

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
    
    try:    
        container.manage_addProduct['MailHost'].manage_addMailHost(mailHostId)
    except BadRequest, br:
        mumble_exists_mumble('init_smtp_host', mailHostId)
    notificationsMailHost = getattr(container, mailHostId)
    notificationsMailHost.manage_makeChanges(
        title='Notifications SMTP Settings',
        smtp_host=smtp_host, smtp_port=smtp_port, smtp_uid=smtp_user,
        smtp_pwd=smtp_password, REQUEST=None)
    
    listManager = getattr(container.site_root(), 'ListManager')
    try:    
        listManager.manage_addProduct['MailHost'].manage_addMailHost(mailHostId)
    except BadRequest, br:
        i = 'ListManager/%s' % mailHostId
        mumble_exists_mumble('init_smtp_host', i)
    listMailHost = getattr(listManager, mailHostId)
    listMailHost.manage_makeChanges(
        title='Mail List SMTP Settings',
        smtp_host=smtp_host, smtp_port=smtp_port, smtp_uid=smtp_user,
        smtp_pwd=smtp_password, REQUEST=None)
    
def import_content( container ):
    # --=rrw=-- big ugly hack
    from Products.GroupServer import pathutil
        
    objects_to_import = ['CodeTemplates.zexp', 'Content.zexp',
                         'ListManager.zexp', 'Templates.zexp']
    for object_to_import in objects_to_import:
        try:
            container._importObjectFromFile( pathutil.get_import_path(
                                                 object_to_import) )
        except BadRequest, br:
            mumble_exists_mumble('import_content', object_to_import)

    site = getattr(container.Content, SITE_ID)
    assert site, 'No site "%s" found' % SITE_ID
    fss = site.manage_addProduct['FileSystemSite']

    try:
        fss.manage_addDirectoryView( pathutil.get_groupserver_path('help'), 'help' )
    except BadRequest, br:
            mumble_exists_mumble('import_content', 'help')
    
    assert hasattr(site.aq_explicit, 'help')
    getattr(site, 'help').manage_changeProperties(title='Help')

def init_group ( container, admin_email, user_email, emailDomain ):
    acl_users = container.site_root().acl_users
    assert acl_users
    site = getattr(container.Content, SITE_ID)
    assert site, 'No %s found' % SITE_ID
    siteInfo = createObject('groupserver.SiteInfo', site)
    
    starter = MoiraeForGroup(siteInfo)
    groupId = 'example_group'
    # We want the userInfo in the context of the site
    admin = acl_users.get_userByEmail(admin_email)
    adminInfo = createObject('groupserver.UserFromId', site, admin.getId())
    try:
        groupInfo = starter.create('Example Group', groupId, 'public', 
                                    emailDomain, adminInfo)
    except BadRequest, br:
        mumble_exists_mumble('init_group', 'groups/%s' % groupId)
        log.warning('init_group: Skipping the rest of the group configuration.')
    else:
        ju = JoiningUser(adminInfo)
        ju.join(groupInfo)

        # Join the normal user to the group.
        user = acl_users.get_userByEmail(user_email)
        # We want the userInfo in the context of the site
        ui = createObject('groupserver.UserFromId', site, user.getId())
        ju = JoiningUser(ui)
        ju.join(groupInfo)

def init_vhm( canonicalHost, container ):
    vhm = getattr(container, 'virtual_hosting')
    sitePath = '/'.join(container.getPhysicalPath())[1:]
    newMap = '%s/%s/Content/%s' % \
      (canonicalHost, sitePath, SITE_ID)
    lines = list(vhm.lines)
    lines.append(newMap)
    mapText = '\n'.join(lines)
    vhm.set_map(mapText, None)

def manage_addGroupserverSite( container, id, title,
        admin_email, admin_password, user_email, user_password,
        zope_admin_id, support_email, timezone, canonicalHost,
        canonicalPort, smtp_host, smtp_port, smtp_user, smtp_password,
        databaseHost, databasePort, databaseUsername, databasePassword,
        databaseName, REQUEST=None ):
    """ Add a Groupserver Site object to a given container.
    
    """
    try:
        id = container._setObject( id, GroupserverSite( id, title ) )
        transaction.commit()
    except BadRequest, br:
        mumble_exists_mumble('manage_addGroupserverSite', id)
        
    gss = getattr( container, id )
    assert gss, 'Could not get the site "%s"' % id

    init_db_connection( gss, databaseHost, databasePort, 
        databaseUsername, databasePassword, databaseName )

    try:
        init_catalog( gss )
        transaction.commit()
    except BadRequest, br:
        mumble_exists_mumble('manage_addGroupserverSite', 'catalog')

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

    init_group( gss, admin_email, user_email, canonicalHost )
    transaction.commit()

    init_vhm( canonicalHost, gss )
    transaction.commit()
    
    if REQUEST is None:
        return
    
    REQUEST.RESPONSE.redirect( REQUEST['URL1'] + '/manage_main' )

manage_addGroupserverSiteForm = PageTemplateFile( 
    'management/manage_addGroupserverSiteForm.zpt', 
    globals(), __name__='manage_addGroupserverSiteForm' )

