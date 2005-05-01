<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:file="http://xwft.org/ns/filelibrary/0.9/" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method="html" indent="yes" encoding="UTF-8" omit-xml-declaration="yes" doctype-public="-//W3C//DTD HTML 4.01 Transitional//EN" doctype-system="http://www.w3.org/TR/html4/loose.dtd"/>
    <xsl:include href="file://results"/>
    <xsl:template match="file:collection">
             <xsl:call-template name="file-present-results"/>
    </xsl:template>
</xsl:stylesheet>
