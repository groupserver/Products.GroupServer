# coding=utf-8
import transaction
import datetime
import urlparse
import pathutil
from zope.interface import implements
from zope.component import createObject, getMultiAdapter
from zExceptions import BadRequest
from OFS.OrderedFolder import OrderedFolder
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from Products.XWFCore.XWFUtils import createRequestFromRequest, rfc822_date
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

SITE_ID = 'initial_site'  # FIX


class GroupserverSite(OrderedFolder):
    implements(IGroupserverSite)

    meta_type = 'Groupserver Site'

    def __init__(self, id, title=''):
        OrderedFolder.__init__(self, id)
        self.title = title

    def get_site(self):
        """ Return ourself.

        """
        return self

    site_root = get_site

    def setAuthCookie(self, resp, cookie_name, cookie_value):
        """ Persistent authentication cookie support.

        """
        path = self.cookie_authentication.getCookiePath()
        if self.REQUEST.form.get('__ac_persistent', 0):
            expires = rfc822_date(datetime.datetime.utcnow() +
                                  datetime.timedelta(365))
            resp.setCookie(cookie_name, cookie_value, path=path,
                            expires=expires)
        else:
            resp.setCookie(cookie_name, cookie_value, path=path)

    def getRealContext(self):
        request = self.REQUEST
        p = urlparse.urlsplit(request.URL1)[2].split('/')
        path = tuple(filter(None, p))
        virtual_path = request.get('VirtualRootPhysicalPath', ())

        path = virtual_path + path

        context = self.unrestrictedTraverse(path)

        return context

    def index_html(self):
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
        request = createRequestFromRequest(self.REQUEST)
        if len(request) > 0:
            url = '?'.join((url, request))

        return redirect(url, lock=1)

    def standard_error_message(self, **kw):
        """ Override the default standard_error_message.

        """
        request = self.REQUEST
        context = self.getRealContext()
        if kw['error_type'] == 'NotFound':
            URL = request.get('URL', '')
            HTTP_REFERRER = request.get('HTTP_REFERER', '')
            m = '404: Link from <{referrer}> to <{url}> is broken.'
            log.warn(m.format(referrer=HTTP_REFERRER, url=URL))
            page = getMultiAdapter((context, request), name='not_found.html')
            retval = page()
        # ignore these types
        elif kw['error_type'] in ('Forbidden',):
            raise  # Propogate the error up.
        else:
            request = self.REQUEST
            context = self.getRealContext()
            page = getMultiAdapter((context, request),
                                   name='unexpected_error.html')
            retval = page()
        return retval

    def fail(self):
        """A test for the error-handling system.
        """
        assert False, 'This is a test of the error-handling system.'


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


def init_user_folder(groupserver_site, admin_email, admin_password,
        user_email, user_password, support_email, canonicalHost,
        canonicalPort):
    btf = groupserver_site.manage_addProduct['BTreeFolder2']
    try:
        btf.manage_addBTreeFolder('contacts', 'Contacts')
    except BadRequest:
        mumble_exists_mumble('init_user_folder', 'contacts')

    # The contacts folder stores the user-data.
    cuf = groupserver_site.manage_addProduct['CustomUserFolder']
    try:
        cuf.manage_addCustomUserFolder('contacts')
    except BadRequest:
        mumble_exists_mumble('init_user_folder', 'acl_users')

    contacts = getattr(groupserver_site, 'contacts')
    contacts.manage_permission('Manage properties', ('Owner', 'Manager'),
                                acquire=1)

    # Cookie Crumbler logs people in
    cc = groupserver_site.manage_addProduct['CookieCrumbler']
    try:
        cc.manage_addCC('cookie_authentication')
    except BadRequest:
        mumble_exists_mumble('init_user_folder', 'cookie_authentication')

    cookies = getattr(groupserver_site, 'cookie_authentication')
    cookies.manage_changeProperties(auto_login_page='Content/login.html',
                                     unauth_page='Content/login.html',
                                     logout_page='Content/logout.html')

    # Create the user-group for the site.
    egSiteMember = '%s_member' % SITE_ID
    acl = getattr(groupserver_site, 'acl_users')
    try:
        acl.userFolderAddGroup(egSiteMember, 'Membership of Example Site')
    except ValueError:
        u = 'User group %s' % egSiteMember
        mumble_exists_mumble('init_user_folder', u)

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
    create_user(example_site, user_email, u'GroupServer User', user_password)


def init_global_configuration(groupserver_site, siteName, supportEmail,
                                timezone, canonicalHost):
    cp = groupserver_site.manage_addProduct['CustomProperties']
    try:
        cp.manage_addCustomProperties('GlobalConfiguration',
            'The global configuration for the Site')
    except BadRequest:
        mumble_exists_mumble('init_global_configuration',
                                'GlobalConfiguration')
        m = 'init_global_configuration: Not configuring "GlobalConfiguration"'
        log.warning(m)
    else:
        gc = getattr(groupserver_site, 'GlobalConfiguration')
        gc.manage_addProperty('alwaysShowMemberPhotos', True, 'boolean')
        gc.manage_addProperty('showEmailAddressTo', 'request', 'string')
        gc.manage_addProperty('supportEmail', supportEmail, 'string')
        gc.manage_addProperty('timezone', timezone, 'string')
        gc.manage_addProperty('emailDomain', canonicalHost, 'string')


def init_fs_scripts(groupserver_site):
    fss = groupserver_site.manage_addProduct['FileSystemSite']
    try:
        fss.manage_addDirectoryView(pathutil.get_groupserver_path('Scripts'),
                                    'Scripts')
    except BadRequest:
        mumble_exists_mumble('init_fs_scripts', 'Scripts')
    try:
        groupserver_site.manage_addFolder('LocalScripts',
                                            'Site specific scripts')
    except BadRequest:
        mumble_exists_mumble('init_fs_scripts', 'LocalScripts')


def init_file_library(groupserver_site):
    fl = groupserver_site.manage_addProduct['XWFFileLibrary2']
    try:
        fl.manage_addXWFFileLibrary2('FileLibrary2')
    except BadRequest:
        mumble_exists_mumble('init_file_library', 'FileLibrary2')

    file_library = getattr(groupserver_site, 'FileLibrary2')
    fls = file_library.manage_addProduct['XWFFileLibrary2']
    try:
        fls.manage_addXWFFileStorage2('storage')
    except BadRequest:
        mumble_exists_mumble('init_file_library', 'FileLibrary2/storage')


def init_id_factory(groupserver_site):
    xif = groupserver_site.manage_addProduct['XWFIdFactory']
    try:
        xif.manage_addXWFIdFactory('IdFactory')
    except BadRequest:
        mumble_exists_mumble('init_id_factory', 'IdFactory')


def init_catalog(groupserver_site):
    mAP = groupserver_site.manage_addProduct['XWFCore']
    mAP.manage_addXWFCatalog('Catalog')
    catalog = getattr(groupserver_site, 'Catalog')

    catalogEntries = ('content_type', 'dc_creator', 'group_ids', 'id',
      'indexable_summary', 'meta_type', 'modification_time', 'size', 'tags',
      'title', 'topic')

    keysToAdd = {
      'allowedRolesAndUsers': 'KeywordIndex',
      'content_type': 'FieldIndex',
      'dc_creator': 'FieldIndex',
      'group_ids': 'KeywordIndex',
      'id': 'FieldIndex',
      'indexable_content': 'ZCTextIndex',
      'meta_type': 'FieldIndex',
      'modification_time': 'DateIndex',
      'tags': 'KeywordIndex',
      'title': 'FieldIndex',
      'topic': 'FieldIndex',
      'dc_description': 'ZCTextIndex',
      'dc_title': 'KeywordIndex',
      'dc_valid': 'DateIndex',
      'linked_resources': 'KeywordIndex',
      'path': 'PathIndex',
      'resource_locator': 'KeywordIndex',
    }

    for key in keysToAdd.keys():
        try:
            catalog.manage_addIndex(key, keysToAdd[key])
        except:
            # The key is already in the index
            pass

    for catalogEntry in catalogEntries:
        try:
            catalog.manage_addColumn(key)
        except:
            # The key is already in the column
            pass


def import_content(container):
    # --=rrw=-- big ugly hack
    from Products.GroupServer import pathutil

    objects_to_import = ['CodeTemplates.zexp', 'Content.zexp',
                         'ListManager.zexp', 'Templates.zexp']
    for object_to_import in objects_to_import:
        try:
            container._importObjectFromFile(pathutil.get_import_path(
                                                 object_to_import))
        except BadRequest:
            mumble_exists_mumble('import_content', object_to_import)

    site = getattr(container.Content, SITE_ID)
    assert site, 'No site "%s" found' % SITE_ID
    site.manage_addProduct['FileSystemSite']


def init_group(container, admin_email, user_email, emailDomain):
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
    except BadRequest:
        mumble_exists_mumble('init_group', 'groups/%s' % groupId)
        m = 'init_group: Skipping the rest of the group configuration.'
        log.warning(m)
    else:
        ju = JoiningUser(adminInfo)
        ju.join(groupInfo)

        # Join the normal user to the group.
        user = acl_users.get_userByEmail(user_email)
        # We want the userInfo in the context of the site
        ui = createObject('groupserver.UserFromId', site, user.getId())
        ju = JoiningUser(ui)
        ju.join(groupInfo)


def init_vhm(canonicalHost, container):
    vhm = getattr(container, 'virtual_hosting')
    sitePath = '/'.join(container.getPhysicalPath())[1:]
    newMap = '%s/%s/Content/%s' % \
      (canonicalHost, sitePath, SITE_ID)
    lines = list(vhm.lines)
    lines.append(newMap)
    mapText = '\n'.join(lines)
    vhm.set_map(mapText, None)


def manage_addGroupserverSite(container, gsId, title,
        admin_email, admin_password, user_email, user_password,
        zope_admin_id, support_email, timezone, canonicalHost,
        canonicalPort, smtp_host, smtp_port, smtp_user, smtp_password,
        databaseHost, databasePort, databaseUsername, databasePassword,
        databaseName, REQUEST=None):
    """ Add a Groupserver Site object to a given container.

    """
    try:
        gsId = container._setObject(gsId, GroupserverSite(gsId, title))
    except BadRequest:
        mumble_exists_mumble('manage_addGroupserverSite', gsId)

    gss = getattr(container, gsId)
    assert gss, 'Could not get the site "%s"' % gsId

    try:
        init_catalog(gss)
    except BadRequest:
        mumble_exists_mumble('manage_addGroupserverSite', 'catalog')

    init_id_factory(gss)
    init_file_library(gss)
    import_content(gss)
    init_user_folder(gss, admin_email, admin_password,
        user_email, user_password, support_email, canonicalHost,
        canonicalPort)
    init_fs_scripts(gss)
    init_global_configuration(gss, title, support_email, timezone,
                                canonicalHost)
    init_group(gss, admin_email, user_email, canonicalHost)
    init_vhm(canonicalHost, gss)
    transaction.commit()

    if REQUEST is None:
        return

    REQUEST.RESPONSE.redirect(REQUEST['URL1'] + '/manage_main')

manage_addGroupserverSiteForm = PageTemplateFile(
    'management/manage_addGroupserverSiteForm.zpt',
    globals(), __name__='manage_addGroupserverSiteForm')
