# -*- coding: utf-8 -*-
from Products.FileSystemSite.DirectoryView import registerDirectory
from AccessControl import ModuleSecurityInfo
from .creation import manage_addGroupserverSiteForm, manage_addGroupserverSite
from .groupserver import GroupserverSite
from .pathutil import get_groupserver_path  # lint:ok


def initialize(context):
    # registerDirectory is also in here to get around some serious chicken-egg
    # problems with getting the module path
    registerDirectory('Scripts', globals())

    context.registerClass(GroupserverSite,
                            constructors=(manage_addGroupserverSiteForm,
                            manage_addGroupserverSite),
                            icon='icons/ic-groupserversite.png')

pathutil_security = ModuleSecurityInfo('Products.GroupServer.pathutil')
pathutil_security.declarePublic('get_groupserver_path')
