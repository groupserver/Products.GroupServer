<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:file="http://xwft.org/ns/filelibrary/0.9/" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:adl="http://iopen.net/ns/adl"
    xmlns:files="http://iopen.net/ns/files"
    xmlns:tal="http://xml.zope.org/namespaces/tal">
    
    <xsl:template match="//adl:slot">
        <div id="slot_{@name}">
            <xsl:value-of select="self::text()"/>
            <xsl:apply-templates />
        </div>
    </xsl:template>

    <xsl:template match="files:selector">
        <script>
            loadURLs.push('pane_files?modification_time=<xsl:value-of select="@modificationtime"/>&amp;b_size=<xsl:value-of select="@batchsize"/>&amp;b_start=<xsl:value-of select="@batchstart"/>&amp;topic=<xsl:value-of select="@topic"/>');
            loadSlots.push('slot_<xsl:value-of select="@slotname"/>');
        </script>
    </xsl:template>

</xsl:stylesheet>

