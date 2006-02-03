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
  xmlns="http://www.w3.org/1999/xhtml"
  xsl:exclude-result-prefixes="xev xhtml2">
  
  <xsl:output
    encoding="UTF-8"
    method="xml"
    doctype-public="-//W3C//DTD XHTML 1.0 Strict//EN"
    doctype-system="http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd"/>
  
  <xsl:include href="file://document-elements"/>
  <xsl:include href="file://block-elements"/>
  <xsl:include href="file://list-elements"/>
  <xsl:include href="file://text-elements"/>
  <xsl:include href="file://section-elements"/>
  <xsl:include href="file://table-elements"/>
  <xsl:include href="file://metadata-elements"/>
  
  <xsl:include href="file://common-attributes"/>
  
  <xsl:include href="file://common-contents"/>
  
</xsl:stylesheet>
