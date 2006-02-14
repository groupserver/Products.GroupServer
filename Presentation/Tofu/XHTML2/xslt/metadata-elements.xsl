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
      <xsl:apply-templates select="@href | @hreflang | @hreftype" 
        mode="hypertext"/>
      <xsl:apply-templates select="@*"/>
    </link>
  </xsl:template>
  
  
  <xsl:template match="xhtml2:handler">
    <script>
      <xsl:apply-templates select="@src" mode="embed"/>
      <xsl:apply-templates select="@*"/>
    </script>
  </xsl:template>
  
</xsl:stylesheet>
