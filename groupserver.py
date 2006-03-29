from zope.interface import implements
from OFS.OrderedFolder import OrderedFolder

from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from App.config import getConfiguration

from interfaces import IGroupserverSite

import transaction
import DateTime

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
            expires = (DateTime.DateTime() + 365).toZone('GMT').rfc822()
            resp.setCookie(cookie_name, cookie_value, path=self.cookie_authentication.getCookiePath(), expires=expires)
        else:
            resp.setCookie(cookie_name, cookie_value, path=self.cookie_authentication.getCookiePath())
        
    def index_html( self ):
        """ Return the default view
        
        """
        request = self.REQUEST
        redirect = request.RESPONSE.redirect
        
        return redirect(request.URL1+'/index.xml', lock=1)
    
    def standard_error_message( self, **kw ):
        """ Override the default standard_error_message.
        
        """
        if kw['error_type'] == 'NotFound':
            if hasattr(self, 'notfound_message.xml'):
                self.REQUEST.RESPONSE.redirect('/notfound_message.xml', lock=1)
            else:
                raise
        # ignore these types
        elif kw['error_type'] in ('Forbidden',):
            pass
        else:
            if hasattr(self, 'notfound_message.xml'):
                self.REQUEST.RESPONSE.redirect('/unexpected_message.xml', lock=1)
            else:
                raise
        
        return 1

def init_user_folder( groupserver_site, initial_user, initial_password, email ):
    cuf = groupserver_site.manage_addProduct['CustomUserFolder']
    cuf.manage_addCustomUserFolder( 'contacts' )
    btf = groupserver_site.manage_addProduct['BTreeFolder2']
    btf.manage_addBTreeFolder( 'contactsimages', 'People in the Site' )
    
    acl = getattr( groupserver_site, 'acl_users' )
    
    #acl.userFolderDelUsers( ('test_user',) )
    
    acl.userFolderAddGroup( 'example_division_member', 
                                'Membership of Example Division' )
    acl.userFolderAddGroup( 'example_division_admin', 
                                'Administration of Example Division' )
    acl.userFolderAddGroup( 'example_group_member', 
                                'Member of Example Group' )
    acl.userFolderAddGroup( 'example_group_admin', 
                                'Administration of Example Group' )
    
    acl._doAddUser( initial_user, initial_password, 
                              (), (), ('example_division_member', 
                                       'example_division_admin', 
                                       'example_group_member', 
                                       'example_group_admin' ) )
    
    user = acl.getUser(initial_user)
    user.manage_changeProperties(firstName='Default', lastName='Administrator',
                                 preferredName='Default')
    user.add_defaultDeliveryEmailAddress(email)
    
    cc = groupserver_site.manage_addProduct['CookieCrumbler']
    cc.manage_addCC('cookie_authentication')
    
    cookies = getattr( groupserver_site, 'cookie_authentication' )
    cookies.manage_changeProperties( auto_login_page='Content/login',
                                     unauth_page='Content/login',
                                     logout_page='Content/login/logout.xml' )
    
    contacts = getattr( groupserver_site, 'contacts' )
    contacts.manage_permission( 'Manage properties', ('Owner','Manager'), acquire=1 )
    
def init_global_configuration( groupserver_site, siteName, supportEmail, timezone, canonicalHost,
                               userVerificationEmail, registrationEmail ):
    cp = groupserver_site.manage_addProduct['CustomProperties']
    cp.manage_addCustomProperties( 'GlobalConfiguration', 'The global configuration for the Site' )
    gc = getattr(groupserver_site, 'GlobalConfiguration')
    gc.manage_addProperty('alwaysShowMemberPhotos', False, 'boolean')
    gc.manage_addProperty('siteName', siteName, 'string')
    gc.manage_addProperty('supportEmail', supportEmail, 'string')
    gc.manage_addProperty('timezone', timezone, 'string')
    gc.manage_addProperty('canonicalHost', canonicalHost, 'string')
    gc.manage_addProperty('userVerificationEmail', userVerificationEmail, 'string')
    gc.manage_addProperty('registrationEmail', registrationEmail, 'string')
    
def init_fs_presentation( groupserver_site ):
    fss = groupserver_site.manage_addProduct['FileSystemSite']
    fss.manage_addDirectoryView( 'GroupServer/Presentation', 'Presentation' )
    groupserver_site.manage_addFolder('PresentationCustom', 'Site specific presentation customisation')
    
def init_fs_scripts( groupserver_site ):
    fss = groupserver_site.manage_addProduct['FileSystemSite']
    fss.manage_addDirectoryView( 'GroupServer/Scripts', 'Scripts' )
    groupserver_site.manage_addFolder('LocalScripts', 'Site specific scripts')

def init_file_library( groupserver_site ):
    fl = groupserver_site.manage_addProduct['XWFFileLibrary2']
    fl.manage_addXWFFileLibrary2( 'FileLibrary2' )
    
    file_library = getattr( groupserver_site, 'FileLibrary2' )
    fls = file_library.manage_addProduct['XWFFileLibrary2']
    fls.manage_addXWFFileStorage2( 'storage' )
    
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

def import_content( container ):
    container.manage_addProduct['MailHost'].manage_addMailHost('MailHost',
                                                                smtp_host='localhost')   
    instance_home = getConfiguration().instancehome
    
    objects_to_import = ['CodeTemplates.zexp', 'Content.zexp', 'GroupProperties.zexp',
                         'ListManager.zexp', 'Templates.zexp', 'UserProperties.zexp',
                         'contacts.zexp']
    
    for object_to_import in objects_to_import:
        container._importObjectFromFile( '%s/Products/GroupServer/imports/%s' % 
                                         (instance_home, object_to_import) )

def manage_addGroupserverSite( container, id, title, initial_user, initial_password,
                               support_email, timezone,
                               canonicalHost, userVerificationEmail, registrationEmail,
                               REQUEST=None ):
    """ Add a Groupserver Site object to a given container.
    
    """
    id = container._setObject( id, GroupserverSite( id, title ) )
    get_transaction().commit()
    
    gss = getattr( container, id )

    init_catalog( gss )
    get_transaction().commit()

    init_file_library( gss )
    get_transaction().commit()
    
    import_content( gss )
    get_transaction().commit()
    
    init_user_folder( gss, initial_user, initial_password, support_email )
    get_transaction().commit()

    init_fs_presentation( gss )
    get_transaction().commit()

    init_fs_scripts( gss )
    get_transaction().commit()

    init_global_configuration( gss, title, support_email, timezone,
                               canonicalHost, userVerificationEmail, registrationEmail )
    get_transaction().commit()
                               
    if REQUEST is None:
        return
    
    REQUEST.RESPONSE.redirect( REQUEST['URL1'] + '/manage_main' )

manage_addGroupserverSiteForm = PageTemplateFile( 
    'management/manage_addGroupserverSiteForm.zpt', 
    globals(), __name__='manage_addGroupserverSiteForm' )
