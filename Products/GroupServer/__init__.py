import os
from Products.FileSystemSite.DirectoryView import registerDirectory
from AccessControl import ModuleSecurityInfo

from pathutil import get_groupserver_path

import groupserver

# registerDirectory is also in here to get around some serious chicken-egg
# problems with getting the module path
def initialize( context ):
    registerDirectory( 'Scripts', globals() )
    registerDirectory( 'Presentation', globals() )
    registerDirectory( 'help', globals() )
    registerDirectory( 'admingroup', globals() )

    context.registerClass( 
        groupserver.GroupserverSite, 
        constructors = ( groupserver.manage_addGroupserverSiteForm, 
                         groupserver.manage_addGroupserverSite ),
        icon='icons/ic-groupserversite.png'
                           )
                           
pathutil_security = ModuleSecurityInfo('Products.GroupServer.pathutil')
pathutil_security.declarePublic('get_groupserver_path')

