<?xml version="1.0" encoding="utf-8"?>

<!--
  - Metadata Elements XSL: Convert XHTML2 Metadata elements to XHTML1
  -
  - Some strait converstions, with nothing spectacular happening.
  -
  - Michael JasonSmith, 2006
  -->

<xsl:stylesheet version="1.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:xev="http://www.w3.org/2001/xml-events"
  xmlns:xhtml2="http://www.w3.org/2002/06/xhtml2/"
  xmlns="http://www.w3.org/1999/xhtml">
  
  <xsl:template match="xhtml2:link">
    <link>
      <xsl:call-template name="commonAttributes"/>
      <xsl:call-template name="hypertextAttributes"/>
      <xsl:call-template name="metadataAttributes"/>
    </link>
  </xsl:template>
  
  
  <xsl:template match="xhtml2:handler">
    <script>
      <xsl:call-template name="commonAttributes"/>
      <xsl:call-template name="hypertextAttributes"/>
      <xsl:call-template name="handlerAttributes"/>
      <xsl:call-template name="embeddingAttributes"/>
    </script>
  </xsl:template>
  
</xsl:stylesheet>
