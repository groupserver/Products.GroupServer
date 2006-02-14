<?xml version="1.0" encoding="utf-8"?>

<!--
  - Common Attributes XSL: Transform attributes from XHTML2 to XHTML1
  -
  - Much like DocBook, attributes in XHTML2 are broken into groups.
  -   This set of named transforms handles the conversion of attributes.
  -   The most common entry-point for this code should be the
  -   "commonAttributes" template, as that is the most common set of
  -   attributes in XHTML2.
  -
  - Michael JasonSmith, 2006
  -->

<xsl:stylesheet version="1.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:xev="http://www.w3.org/2001/xml-events"
  xmlns:xhtml2="http://www.w3.org/2002/06/xhtml2/"
  xmlns="http://www.w3.org/1999/xhtml">

  <!-- Handle the attributes that are common to all sorts of elements -->

  <!-- === Core === -->
  <!-- Class -->
  <xsl:template match="@class">
    <xsl:attribute name="class">
      <xsl:if test="../@role">
        <xsl:value-of select="../@role"/>
      </xsl:if>
      <xsl:value-of select="."/>
    </xsl:attribute>
  </xsl:template>
  <!-- ID -->
  <xsl:template match="@id">
    <xsl:attribute name="id">
      <xsl:value-of select="."/>
    </xsl:attribute>
  </xsl:template>
  <!-- Missing: Layout -->
  <!-- Title -->
  <xsl:template match="@title">
    <xsl:attribute name="title">
      <xsl:value-of select="."/>
    </xsl:attribute>
  </xsl:template>

  <!-- === Events === -->
  <!-- JavaScript event handler: XEvent to XHTML1.0 -->
  <xsl:template match="@xev:event">
    <xsl:attribute name="{.}">
      <xsl:value-of select="../@xev:handler"/>
    </xsl:attribute>
  </xsl:template>
  <xsl:template match="@xev:handler">
  </xsl:template>
  
  <!-- === Hypertext === -->
  <!-- cite -->
  <xsl:template match="@cite" mode="hypertext">
    <xsl:attribute name="cite">
      <xsl:value-of select="."/>
    </xsl:attribute>
  </xsl:template>
  <xsl:template match="@cite">
  </xsl:template>
  <!-- href -->
  <xsl:template match="@href" mode="hypertext">
    <xsl:attribute name="href">
      <xsl:value-of select="."/>
    </xsl:attribute>
  </xsl:template>
  <xsl:template match="@href">
  </xsl:template>
  <!-- hreflang -->
  <xsl:template match="@hreflang" mode="hypertext">
    <xsl:attribute name="hreflang">
      <xsl:value-of select="."/>
    </xsl:attribute>
  </xsl:template>
  <xsl:template match="@hreflang">
  </xsl:template>
  <!-- hreftype -->
  <xsl:template match="@hreftype" mode="hypertext">
    <xsl:attribute name="type">
      <xsl:value-of select="."/>
    </xsl:attribute>
  </xsl:template>
  <xsl:template match="@hreftype">
  </xsl:template>
  
  <!-- === Role === -->
  <!-- The "role" is folded into the class. -->
  <xsl:template match="@role">
  </xsl:template>
  
  
  <!-- === Style === -->
  <xsl:template match="@style">
    <xsl:attribute name="style">
      <xsl:value-of select="."/>
    </xsl:attribute>
  </xsl:template>

  <!-- === Version === -->
  <!-- Versions cannot be mapped -->
  <xsl:template match="@version">
  </xsl:template> 
  <!-- === Embedding === -->
  <!-- src -->
  <xsl:template match="@src" mode="image">
    <xsl:element name="img">
      <xsl:attribute name="alt">
        <xsl:choose>
          <xsl:when test="self::text()">
            <xsl:value-of select="self::text()"/>
          </xsl:when>
          <xsl:when test="../text()">
            <xsl:value-of select="../text()"/>
          </xsl:when>
          <xsl:when test="child::text()">
            <xsl:value-of select="child::text()"/>
          </xsl:when>
          <xsl:otherwise>No Description</xsl:otherwise>
        </xsl:choose>
      </xsl:attribute>
      <xsl:attribute name="src">
        <xsl:value-of select="."/>
      </xsl:attribute>
    </xsl:element>
  </xsl:template>
  <xsl:template match="@src" mode="embed">
    <xsl:attribute name="src">
      <xsl:value-of select="."/>
    </xsl:attribute>
  </xsl:template>
  <xsl:template match="@src">
  </xsl:template>
    
  <!-- === Tables === -->
  <xsl:template match="@span">
    <xsl:attribute name="span">
      <xsl:value-of select="."/>
    </xsl:attribute>
  </xsl:template>
  <xsl:template match="@colspan">
    <xsl:attribute name="colspan">
      <xsl:value-of select="."/>
    </xsl:attribute>
  </xsl:template>
  <xsl:template match="@rowspan">
    <xsl:attribute name="rowspan">
      <xsl:value-of select="."/>
    </xsl:attribute>
  </xsl:template>

  <!-- === Metadata === -->
  <xsl:template match="@rel">
    <xsl:attribute name="rel">
      <xsl:value-of select="."/>
    </xsl:attribute>
  </xsl:template>

  <!-- === Handler === -->
  <xsl:template match="@type">
    <xsl:attribute name="type">
      <xsl:value-of select="."/>
    </xsl:attribute>
  </xsl:template>
</xsl:stylesheet>
