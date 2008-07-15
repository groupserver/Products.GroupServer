import os
from Products.FileSystemSite.DirectoryView import registerDirectory

import pathutil

import groupserver

# registerDirectory is also in here to get around some serious chicken-egg
# problems with getting the module path
def initialize( context ):
    registerDirectory( 'Scripts', globals() )
    registerDirectory( 'Presentation', globals() )
    registerDirectory( 'help', globals() )
    registerDirectory( 'admindivision', globals() )
    registerDirectory( 'admingroup', globals() )

    context.registerClass( 
        groupserver.GroupserverSite, 
        constructors = ( groupserver.manage_addGroupserverSiteForm, 
                         groupserver.manage_addGroupserverSite ),
        icon='icons/ic-groupserversite.png'

                           )

                           
