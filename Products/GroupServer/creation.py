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
SITE_ID = 'initial_site'  # FIX


def mumble_exists_mumble(function, thing):
    '''Warn that a thing still exists'''
    log.warning('%s: "%s" already exists.' % (function, thing))
    log.warning('%s: Carrying on regardless.' % function)


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
    btf = gss.manage_addProduct['BTreeFolder2']
    try:
        btf.manage_addBTreeFolder('contacts', 'Contacts')
    except BadRequest:
        mumble_exists_mumble('init_user_folder', 'contacts')

    # The contacts folder stores the user-data.
    cuf = gss.manage_addProduct['CustomUserFolder']
    try:
        cuf.manage_addCustomUserFolder('contacts')
    except BadRequest:
        mumble_exists_mumble('init_user_folder', 'acl_users')

    contacts = getattr(gss, 'contacts')
    contacts.manage_permission('Manage properties', ('Owner', 'Manager'),
                                acquire=1)

    # Cookie Crumbler logs people in
    cc = gss.manage_addProduct['CookieCrumbler']
    try:
        cc.manage_addCC('cookie_authentication')
    except BadRequest:
        mumble_exists_mumble('init_user_folder', 'cookie_authentication')

    cookies = getattr(gss, 'cookie_authentication')
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


def init_global_configuration(gss, siteName, supportEmail,
                                timezone, canonicalHost):
    '''Initalise the global configuration.'''
    cp = gss.manage_addProduct['CustomProperties']
    try:
        cp.manage_addCustomProperties('GlobalConfiguration',
            'The global configuration for the Site')
    except BadRequest:
        mumble_exists_mumble('init_global_configuration',
                                'GlobalConfiguration')
        m = 'init_global_configuration: Not configuring "GlobalConfiguration"'
        log.warning(m)
    else:
        gc = getattr(gss, 'GlobalConfiguration')
        gc.manage_addProperty('alwaysShowMemberPhotos', True, 'boolean')
        gc.manage_addProperty('showEmailAddressTo', 'request', 'string')
        gc.manage_addProperty('supportEmail', supportEmail, 'string')
        gc.manage_addProperty('timezone', timezone, 'string')
        gc.manage_addProperty('emailDomain', canonicalHost, 'string')


def init_fs_scripts(gss):
    '''Initalise the Scripts that live on the file-system. It uses the old
    FileSystemSite code.'''
    fss = gss.manage_addProduct['FileSystemSite']
    try:
        fss.manage_addDirectoryView(get_groupserver_path('Scripts'), 'Scripts')
    except BadRequest:
        mumble_exists_mumble('init_fs_scripts', 'Scripts')
    try:
        gss.manage_addFolder('LocalScripts', 'Site specific scripts')
    except BadRequest:
        mumble_exists_mumble('init_fs_scripts', 'LocalScripts')


def init_file_library(gss):
    fl = gss.manage_addProduct['XWFFileLibrary2']
    try:
        fl.manage_addXWFFileLibrary2('FileLibrary2')
    except BadRequest:
        mumble_exists_mumble('init_file_library', 'FileLibrary2')

    file_library = getattr(gss, 'FileLibrary2')
    fls = file_library.manage_addProduct['XWFFileLibrary2']
    try:
        fls.manage_addXWFFileStorage2('storage')
    except BadRequest:
        mumble_exists_mumble('init_file_library', 'FileLibrary2/storage')


def init_id_factory(gss):
    '''Initalise the XWF ID Factory, which is used by the Files system.'''
    xif = gss.manage_addProduct['XWFIdFactory']
    try:
        xif.manage_addXWFIdFactory('IdFactory')
    except BadRequest:
        mumble_exists_mumble('init_id_factory', 'IdFactory')


def init_catalog(gss):
    '''Initalise the ZODB catalog.'''
    mAP = gss.manage_addProduct['XWFCore']
    mAP.manage_addXWFCatalog('Catalog')
    catalog = getattr(gss, 'Catalog')

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
    '''Import the content from the ZEXP files.'''
    # --=rrw=-- big ugly hack

    objects_to_import = ['CodeTemplates.zexp', 'Content.zexp',
                         'ListManager.zexp', 'Templates.zexp']
    for object_to_import in objects_to_import:
        try:
            path = get_import_path(object_to_import)
            container._importObjectFromFile(path)
        except BadRequest:
            mumble_exists_mumble('import_content', object_to_import)

    site = getattr(container.Content, SITE_ID)
    assert site, 'No site "%s" found' % SITE_ID
    site.manage_addProduct['FileSystemSite']


def init_group(container, admin_email, emailDomain):
    '''Initialise the first group.'''
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


def manage_addGroupserverSite(container, gsId, title,
        admin_email, admin_password, zope_admin_id, timezone,
        canonicalHost, canonicalPort, smtp_host, smtp_port, smtp_user,
        smtp_password, databaseHost, databasePort, databaseUsername,
        databasePassword, databaseName, REQUEST=None):
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
    init_user_folder(gss, admin_email, admin_password, canonicalHost,
                        canonicalPort)
    init_fs_scripts(gss)

    supportEmail = 'support@{0}'.format(canonicalHost)
    init_global_configuration(gss, title, supportEmail, timezone,
                                canonicalHost)
    init_group(gss, admin_email, canonicalHost)
    init_vhm(canonicalHost, gss)
    transaction.commit()

    if REQUEST is None:
        return

    REQUEST.RESPONSE.redirect(REQUEST['URL1'] + '/manage_main')

manage_addGroupserverSiteForm = PageTemplateFile(
    'management/manage_addGroupserverSiteForm.zpt',
    globals(), __name__='manage_addGroupserverSiteForm')
