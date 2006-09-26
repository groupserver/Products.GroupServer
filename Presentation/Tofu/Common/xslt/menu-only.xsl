<?xml version="1.0" ?>

<!-- XSL template to transform JoshBook menus into XHTML1, but without the 
  - normal XHTML1 support code (such as DTDs and the XML declaration. This
  - template was designed to be used with the Pragmatic Templates product.
  -
  - Michael JasonSmith, September 2006
  -->

<xsl:stylesheet version="1.0" 
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:metal="http://xml.zope.org/namespaces/metal"
  xmlns:tal="http://xml.zope.org/namespaces/tal">

  <xsl:output encoding="UTF-8" method="xml" standalone="no" version="1.0"
    omit-xml-declaration="yes"/>

  <xsl:include href="file://menu" />

</xsl:stylesheet>
