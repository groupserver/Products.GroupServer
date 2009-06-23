<?xml version="1.0" encoding="UTF-8" ?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:metal="http://xml.zope.org/namespaces/metal"
    xmlns:xf="http://www.w3.org/2002/xforms"
    xmlns:tal="http://xml.zope.org/namespaces/tal"
    exclude-result-prefixes="xf">
    
    <xsl:include href="file://layout" />
    
    <xsl:output method="xml" indent="yes" encoding="UTF8"
        omit-xml-declaration="yes"
        doctype-public="-//W3C//DTD HTML 4.01//EN"
        doctype-system="http://www.w3.org/TR/html4/strict.dtd" />
    
    <xsl:template match="root">
        <xsl:apply-templates select="output/content" />
    </xsl:template>
    
</xsl:stylesheet>
