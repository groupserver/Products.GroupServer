from Products.FileSystemSite.DirectoryView import registerDirectory

registerDirectory( 'Products/GroupServer/Scripts', globals() )
registerDirectory( 'Products/GroupServer/Presentation', globals() )
registerDirectory( 'Products/GroupServer/help', globals() )
registerDirectory( 'Products/GroupServer/admindivision', globals() )
registerDirectory( 'Products/GroupServer/admingroup', globals() )

import groupserver

def initialize( context ):
    context.registerClass( 
        groupserver.GroupserverSite, 
        constructors = ( groupserver.manage_addGroupserverSiteForm, 
                         groupserver.manage_addGroupserverSite ),
        icon='icons/ic-groupserversite.png'

                           )

                           
