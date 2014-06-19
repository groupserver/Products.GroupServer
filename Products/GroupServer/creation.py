# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright © 2008, 2009, 2010, 2011, 2012, 2013, 2014 OnlineGroups.net and
# Contributors. All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
from __future__ import absolute_import, unicode_literals
from logging import getLogger
log = getLogger('Products.GroupServer.creation')
import sys
if (sys.version_info < (3, )):
    from urlparse import urlsplit
else:
    from urllib.parse import urlsplit  # lint:ok
import transaction
from zope.component import createObject
from zExceptions import BadRequest
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from gs.core import to_ascii
from gs.group.member.join.joininguser import JoiningUser
from gs.group.start.groupcreator import MoiraeForGroup
from gs.profile.email.verify.emailverificationuser import EmailVerificationUser
from gs.profile.password.passworduser import PasswordUser
from Products.GSProfile.utils import create_user_from_email
from .pathutil import get_groupserver_path, get_import_path
from .groupserver import GroupserverSite
SITE_ID = to_ascii('initial_site')  # FIX


def mumble_exists_mumble(function, thing):
    '''Warn that a thing exists

:param str function: The function that is raising the warning.
:param str thing: The thing that exists.
:returns: ``None``

Installation sometimes dies. When this happens various *things* are left in
the object database. These things should left alone when installation is rerun,
but it is good practice to mention that they are being left alone.
'''
    m = '{0}: "{1}" already exists.\n{0}: Carrying on regardless.'
    msg = m.format(function, thing)
    log.warning(msg)


def create_user(site, email, fn, password):
    'Create a user'
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
        m = 'create_user: Verified the address <{0}> for {1} ({2}).'
        msg = m.format(email, fn, user.getId())
        log.info(to_ascii(msg))
    except Exception as e:
        m = 'create_user: Issues verifying the address <{0}> for {1} ({2}).'
        msg = m.format(email, fn, user.getId())
        log.error(to_ascii(msg))
        raise e
    return user


def init_user_folder(gss, admin_email, admin_password, canonicalHost,
                        canonicalPort):
    '''Initalise the user-folder (contacts)'''
    CONTACTS_NAME = to_ascii('contacts')
    btf = gss.manage_addProduct['BTreeFolder2']
    try:
        btf.manage_addBTreeFolder(CONTACTS_NAME, 'Contacts')
    except BadRequest:
        mumble_exists_mumble('init_user_folder', CONTACTS_NAME)

    # The contacts folder stores the user-data.
    cuf = gss.manage_addProduct['CustomUserFolder']
    try:
        cuf.manage_addCustomUserFolder(CONTACTS_NAME)
    except BadRequest:
        mumble_exists_mumble('init_user_folder', 'acl_users')

    contacts = getattr(gss, CONTACTS_NAME)
    contacts.manage_permission('Manage properties', ('Owner', 'Manager'),
                                acquire=1)

    # Cookie Crumbler logs people in
    CA_NAME = to_ascii('cookie_authentication')
    cc = gss.manage_addProduct['CookieCrumbler']
    try:
        cc.manage_addCC(CA_NAME)
    except BadRequest:
        mumble_exists_mumble('init_user_folder', CA_NAME)

    cookies = getattr(gss, CA_NAME)
    cookies.manage_changeProperties(auto_login_page='Content/login.html',
                                     unauth_page='Content/login.html',
                                     logout_page='Content/logout.html')

    # Create the user-group for the site.
    egSiteMember = '%s_member' % SITE_ID
    acl = getattr(gss, 'acl_users')
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
    example_site = getattr(gss.Content, SITE_ID)
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
    admin = create_user(example_site, admin_email, 'GroupServer Administrator',
                            admin_password)
    example_site.manage_addLocalRoles(admin.getId(), ['DivisionAdmin'])


def init_global_configuration(gss, siteName, supportEmail, canonicalHost):
    '''Initalise the global configuration (``GlobalConfiguration``).'''
    GLOBAL_CONFIG_NAME = to_ascii('GlobalConfiguration')
    cp = gss.manage_addProduct['CustomProperties']
    try:
        cp.manage_addCustomProperties(GLOBAL_CONFIG_NAME,
            'The global configuration for the site')
    except BadRequest:
        mumble_exists_mumble('init_global_configuration',
                                GLOBAL_CONFIG_NAME)
        m = 'init_global_configuration: Not configuring "GlobalConfiguration"'
        log.warning(m)
    else:
        gc = getattr(gss, GLOBAL_CONFIG_NAME)
        gc.manage_addProperty('alwaysShowMemberPhotos', True, 'boolean')
        gc.manage_addProperty('showEmailAddressTo', 'request', 'string')
        gc.manage_addProperty('supportEmail', supportEmail, 'string')
        gc.manage_addProperty('timezone', 'UTC', 'string')
        gc.manage_addProperty('emailDomain', canonicalHost, 'string')


def init_fs_scripts(gss):
    '''Initalise the Scripts that live on the file-system. It uses the old
    FileSystemSite code.'''
    fss = gss.manage_addProduct['FileSystemSite']
    try:
        fss.manage_addDirectoryView(get_groupserver_path('Scripts'),
                                    to_ascii('Scripts'))
    except BadRequest:
        mumble_exists_mumble('init_fs_scripts', 'Scripts')
    try:
        gss.manage_addFolder(to_ascii('LocalScripts'), 'Site specific scripts')
    except BadRequest:
        mumble_exists_mumble('init_fs_scripts', 'LocalScripts')


def init_file_library(gss):
    'Create the XWFFileLibrary2'
    LIBRARY_NAME = to_ascii('FileLibrary2')
    fl = gss.manage_addProduct['XWFFileLibrary2']
    try:
        fl.manage_addXWFFileLibrary2(LIBRARY_NAME)
    except BadRequest:
        mumble_exists_mumble('init_file_library', LIBRARY_NAME)

    file_library = getattr(gss, LIBRARY_NAME)
    fls = file_library.manage_addProduct['XWFFileLibrary2']
    try:
        fls.manage_addXWFFileStorage2(to_ascii('storage'))
    except BadRequest:
        mumble_exists_mumble('init_file_library', LIBRARY_NAME + '/storage')


def init_id_factory(gss):
    '''Initalise the XWF ID Factory, which is used by the Files system.'''
    FACTORY_NAME = to_ascii('IdFactory')
    xif = gss.manage_addProduct['XWFIdFactory']
    try:
        xif.manage_addXWFIdFactory(FACTORY_NAME)
    except BadRequest:
        mumble_exists_mumble('init_id_factory', FACTORY_NAME)


def init_catalog(gss):
    '''Initalise the ZODB catalog.'''
    CATALOG_NAME = to_ascii('Catalog')
    mAP = gss.manage_addProduct['XWFCore']
    mAP.manage_addXWFCatalog(CATALOG_NAME)
    catalog = getattr(gss, CATALOG_NAME)

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

    for key in list(keysToAdd.keys()):
        try:
            catalog.manage_addIndex(to_ascii(key), to_ascii(keysToAdd[key]))
        except:
            # The key is already in the index
            pass

    for catalogEntry in catalogEntries:
        try:
            catalog.manage_addColumn(to_ascii(key))
        except:
            # The key is already in the column
            pass


def import_content(container):
    '''Import the content from the ZEXP files.'''
    # --=rrw=-- big ugly hack

    objects_to_import = ('Content.zexp', 'ListManager.zexp', 'Templates.zexp')
    for object_to_import in objects_to_import:
        try:
            path = to_ascii(get_import_path(object_to_import))
            container._importObjectFromFile(path)
        except BadRequest:
            mumble_exists_mumble('import_content', object_to_import)

    site = getattr(container.Content, SITE_ID, None)
    if not site:
        m = 'No site "{0}" found in "{1}"'.format(SITE_ID, container)
        raise ValueError(m)
    site.manage_addProduct['FileSystemSite']


def init_group(container, admin_email, emailDomain):
    '''Initialise the first group.'''
    acl_users = container.site_root().acl_users
    site = getattr(container.Content, SITE_ID, None)
    if not site:
        m = 'No site "{0}" found in "{1}"'.format(SITE_ID, container)
        raise ValueError(m)
    siteInfo = createObject('groupserver.SiteInfo', site)

    starter = MoiraeForGroup(siteInfo)
    groupId = 'example_group'
    # We want the userInfo in the context of the site
    admin = acl_users.get_userByEmail(admin_email)
    adminInfo = createObject('groupserver.UserFromId', site, admin.getId())
    try:
        groupInfo = starter.create('Example group', groupId, 'public',
                                    emailDomain, adminInfo)
    except BadRequest:
        mumble_exists_mumble('init_group', 'groups/%s' % groupId)
        m = 'init_group: Skipping the rest of the group configuration.'
        log.warning(m)
    else:
        ju = JoiningUser(adminInfo)
        # Silent Join is used so if the SMTP config is borken everything still
        # works.
        ju.silent_join(groupInfo)


def init_vhm(canonicalHost, container):
    '''Initalise the virtual host monster

    The virtual host monster maps between a domain name and a path to a folder
    within the ZMI. This function determines the mapping and sets it up.'''
    vhm = getattr(container, 'virtual_hosting')
    sitePath = '/'.join(container.getPhysicalPath())[1:]
    newMap = '%s/%s/Content/%s' % \
      (canonicalHost, sitePath, SITE_ID)
    lines = list(vhm.lines)
    lines.append(newMap)
    mapText = '\n'.join(lines)
    vhm.set_map(mapText, None)


def manage_addGroupserverSite(container, gsId, title, supportEmail,
        admin_email, admin_password, canonicalHost, canonicalPort,
        smtp_host, smtp_port, smtp_user, smtp_password, REQUEST=None):
    """Add a Groupserver instance to a given container.

:param OFS.Folder container: The folder in the ZMI that holds the new instance.
:param str gsId: The identifier for the new GroupServer instance.
:param str title: The title for the new instance.
:param str supportEmail: The email address of support for the GS instance.
:param str admin_email: The email address for the administrator of the new site.
:param str admin_password: The password for the new site administrator.
:param str canonicalHost: The host-name of the new site.
:param str canonicalPort: The port of the new site.
:param str smtp_host: The host-name of the *outgoing* SMTP server.
:param str smtp_port: The port of the *outgoing* SMTP server.
:param str smtp_user: The user-name of the user for the *outgoing* SMTP server.
:param str smtp_password: The password for the *outgoing* SMTP server.
:param object REQUEST: The request object (may be ``None``).
"""
    try:
        gsId = container._setObject(gsId, GroupserverSite(gsId, title))
    except BadRequest:
        mumble_exists_mumble('manage_addGroupserverSite', gsId)

    gss = getattr(container, gsId, None)
    if not gss:
        raise ValueError('Could not get the site "{0}"'.format(gsId))

    try:
        init_catalog(gss)
    except BadRequest:
        mumble_exists_mumble('manage_addGroupserverSite', 'catalog')

    init_id_factory(gss)
    init_file_library(gss)
    import_content(gss)
    init_user_folder(gss, admin_email, admin_password, canonicalHost,
                        canonicalPort)
    init_fs_scripts(gss)

    init_global_configuration(gss, title, supportEmail, canonicalHost)
    init_group(gss, admin_email, canonicalHost)
    init_vhm(canonicalHost, gss)

    # TODO: SMTP

    transaction.commit()

    if REQUEST is None:
        return

    REQUEST.RESPONSE.redirect(REQUEST['URL1'] + '/manage_main')

manage_addGroupserverSiteForm = PageTemplateFile(
    'management/manage_addGroupserverSiteForm.zpt',
    globals(), __name__='manage_addGroupserverSiteForm')
