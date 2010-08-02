<?xml version="1.0" encoding="utf-8"?>

<!--
  - Common Contents XSL: Transform XHTML2 element-contents to XHTML1
  -
  - One of the biggest changes in XHTML2 is that it has deprecated the
  -   <a/> tag: instead almost all elements can contain an href, which
  -   creates a link to the target. This transform adds the <a/> tag
  -   when it is need. In addition, it adds an <img/> when the src
  -   attribute is specified (XHTML2 has deprecated the <img/> tag, too).
  -
  - The only valid entry point for this code is the "elementLink" named
  -   template.
  -
  - Michael JasonSmith, 2006
  -->

<xsl:stylesheet version="1.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:xev="http://www.w3.org/2001/xml-events"
  xmlns:xhtml2="http://www.w3.org/2002/06/xhtml2/"
  xmlns="http://www.w3.org/1999/xhtml">

  <xsl:template match="xhtml2:html">
    <html>
      <xsl:apply-templates select="node()"/>
      <!-- 
        - No, I do not know what the hell is meant to happen if an
        -   html element has a src or href either -->
    </html>
  </xsl:template>
  
  <xsl:template name="head" match="xhtml2:head">
    <head>
      <xsl:apply-templates select="node()"/>
    </head>
  </xsl:template>

  <xsl:template name="title" match="xhtml2:title">
    <title>
      <xsl:apply-templates select="@* | node()"/>
    </title>
  </xsl:template>

  <xsl:template name="body" match="xhtml2:body">
    <body>
      <xsl:apply-templates select="@* | node()"/>
    </body>
  </xsl:template>
</xsl:stylesheet>
