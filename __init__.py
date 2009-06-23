import os
from Products.FileSystemSite.DirectoryView import registerDirectory

import pathutil

import groupserver

# registerDirectory is also in here to get around some serious chicken-egg
# problems with getting the module path
def initialize( context ):
    registerDirectory( 'Products/GroupServer/Scripts', globals() )
    registerDirectory( 'Products/GroupServer/Presentation', globals() )
    registerDirectory( 'Products/GroupServer/help', globals() )
    registerDirectory( 'Products/GroupServer/admindivision', globals() )
    registerDirectory( 'Products/GroupServer/admingroup', globals() )

    context.registerClass( 
        groupserver.GroupserverSite, 
        constructors = ( groupserver.manage_addGroupserverSiteForm, 
                         groupserver.manage_addGroupserverSite ),
        icon='icons/ic-groupserversite.png'

                           )

                           
