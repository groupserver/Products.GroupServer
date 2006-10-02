<?xml version="1.0" encoding="utf-8"?>

<!--
  - Deprecated elements transform: XHTML2 to XHTML1
  -  
  - This stylesheet contains the transforms for the elements in XHTML1
  -   that are either deprecated or unnecessary, such as the anchor tag.
  -  
  -  Michael JasonSmith, 2006
-->
  
<xsl:stylesheet version="1.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:xev="http://www.w3.org/2001/xml-events"
  xmlns:xhtml2="http://www.w3.org/2002/06/xhtml2/"
  xmlns="http://www.w3.org/1999/xhtml">

  <!-- Anchor template -->
  <xsl:template match="xhtml2:a">
    <a>
      <xsl:apply-templates 
        select="@href | @hreflang | @hreftype" 
        mode="hypertext"/>
      <xsl:apply-templates select="@*"/>
      <xsl:apply-templates />
    </a>
  </xsl:template>
  
</xsl:stylesheet>
