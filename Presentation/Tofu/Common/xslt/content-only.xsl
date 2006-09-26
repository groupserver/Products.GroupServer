<?xml version="1.0" ?>

<!-- XSL template to transform JoshBook content into XHTML1, but without the 
  - normal XHTML1 support code (such as DTDs and the XML declaration). This
  - template was designed to be used with the Pragmatic Templates product.
  -
  - Michael JasonSmith, September 2006
  -->

<xsl:stylesheet version="1.0" 
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:metal="http://xml.zope.org/namespaces/metal"
  xmlns:tal="http://xml.zope.org/namespaces/tal">

  <xsl:output encoding="UTF-8" method="xml" standalone="no" version="1.0"
    omit-xml-declaration="no"/>

  <xsl:template match="root">
      <xsl:apply-templates />
  </xsl:template>
  <xsl:template match="output">
      <xsl:apply-templates />
  </xsl:template>
  <xsl:template match="content">
    <div class="joshbook-content">
      <xsl:apply-templates />
    </div>
  </xsl:template>
  
  <xsl:include href="file://layout"/>
  
</xsl:stylesheet>
