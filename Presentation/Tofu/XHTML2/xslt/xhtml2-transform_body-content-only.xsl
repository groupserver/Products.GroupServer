<?xml version="1.0" encoding="utf-8"?>

<!--
  - Main XSL Stylesheet for transforming XHTML2 to XHTML1
  -
  - This file sets up the file output paramaters and includes the requisite
  -   modules that are reuired to do the transformation.
  -
  - Michael JasonSmith, 2006
  -->

<xsl:stylesheet version="1.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:xev="http://www.w3.org/2001/xml-events"
  xmlns:xhtml2="http://www.w3.org/2002/06/xhtml2/"
  xmlns:xhtml1="http://www.w3.org/1999/xhtml"
  xsl:exclude-result-prefixes="xev xhtml2 xhtml1">
  
  <xsl:output encoding="UTF-8" method="xml" standalone="no" version="1.0"
    omit-xml-declaration="yes"/>

  <!-- Stolen from document-elements.xsl -->
  <xsl:template name="head" match="xhtml2:head">
  </xsl:template>

  <xsl:include href="file://block-elements.xsl"/>
  <xsl:include href="file://section-elements.xsl"/>
  <xsl:include href="file://list-elements.xsl"/>
  <xsl:include href="file://text-elements.xsl"/>
  <xsl:include href="file://table-elements.xsl"/>
  <xsl:include href="file://depricated-elements.xsl"/>
  
  <xsl:include href="file://attributes.xsl"/>
  
  <xsl:include href="file://common-contents.xsl"/>
  
</xsl:stylesheet>
