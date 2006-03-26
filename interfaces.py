from zope.interface import Interface

class IGroupserverSite(Interface):
    def get_site(self):
        """ Return ourselves.
        
        """
