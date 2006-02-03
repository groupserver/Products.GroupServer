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
  <xsl:template name="commonAttributes">
    <xsl:call-template name="coreAttributes"/>
    <xsl:call-template name="eventAttributes"/>
    <xsl:call-template name="roleAttributes"/>
    <xsl:call-template name="styleAttributes"/>
    <!-- Deliberately skipped attributes hypertext and embedding -->
  </xsl:template>

  <!-- === Core === -->
  <xsl:template name="coreAttributes">
    <!-- Class -->
    <xsl:if test="@xhtml2:class">
      <xsl:attribute name="class" select="@xhtml2:class">
        <xsl:value-of select="@xhtml2:class"/>
      </xsl:attribute>
    </xsl:if>
    <!-- ID -->
    <xsl:if test="@xhtml2:id">
      <xsl:attribute name="id" select="@xhtml2:id">
        <xsl:value-of select="@xhtml2:id"/>
      </xsl:attribute>
    </xsl:if>
    <!-- Missing: Layout -->
    <!-- Title -->
    <xsl:if test="@xhtml2:title">
      <xsl:attribute name="title">
        <xsl:value-of select="@xhtml2:title"/>
      </xsl:attribute>
    </xsl:if>
  </xsl:template>

  <!-- === Events === -->
  <!-- JavaScript event handler: XEvent to XHTML1.0 -->
  <xsl:template name="eventAttributes">
    <xsl:if test="@xev:event">
      <xsl:attribute name="{@xev:event}">
         <xsl:value-of select="@xev:handler"/>
      </xsl:attribute>
    </xsl:if>
  </xsl:template>
  
  <!-- === Hypertext === -->
  <xsl:template name="hypertextAttributes">
    <!-- cite -->
    <xsl:if test="@xhtml2:cite">
      <xsl:attribute name="cite">
         <xsl:value-of select="@xhtml2:cite"/>
      </xsl:attribute>
    </xsl:if>
    <!-- href -->
    <xsl:if test="@xhtml2:href">
      <xsl:attribute name="href">
         <xsl:value-of select="@xhtml2:href"/>
      </xsl:attribute>
    </xsl:if>
    <!-- hreflang -->
    <xsl:if test="@xhtml2:hreflang">
      <xsl:attribute name="hreflang">
         <xsl:value-of select="@xhtml2:hreflang"/>
      </xsl:attribute>
    </xsl:if>
    <!-- hreftype -->
    <xsl:if test="@xhtml2:hreftype">
      <xsl:attribute name="type">
         <xsl:value-of select="@xhtml2:hreftype"/>
      </xsl:attribute>
    </xsl:if>
  </xsl:template>
  
  <!-- === Role === -->
  <xsl:template name="roleAttributes">
    <!-- The "role" is folded into the class. -->
    <xsl:if test="@xhtml2:role">
      <xsl:attribute name="class">
        <xsl:value-of select="@xhtml2:role"/>
      </xsl:attribute>
    </xsl:if>
  </xsl:template>
  
  <!-- === Style === -->
  <xsl:template name="styleAttributes">
    <xsl:if test="@xhtml2:style">
      <xsl:attribute name="style">
        <xsl:value-of select="@xhtml2:style"/>
      </xsl:attribute>
    </xsl:if>
  </xsl:template>

  <!-- === Version === -->
  <xsl:template name="versionAttributes">
      <!-- Versions cannot be mapped -->
    <xsl:if test="@xhtml2:version">
    </xsl:if>
  </xsl:template>
  
  <!-- === Embedding === -->
  <xsl:template name="embeddingAttributes">
    <xsl:if test="@xhtml2:src">
    <xsl:attribute name="src">
        <xsl:value-of select="@xhtml2:src"/>
      </xsl:attribute>
    </xsl:if>
  </xsl:template>
  
  <!-- === Tables === -->
  <xsl:template name="spanAttributes">
    <xsl:if test="@xhtml2:span">
    <xsl:attribute name="span">
        <xsl:value-of select="@xhtml2:span"/>
      </xsl:attribute>
    </xsl:if>
    <xsl:if test="@xhtml2:colspan">
    <xsl:attribute name="colspan">
        <xsl:value-of select="@xhtml2:colspan"/>
      </xsl:attribute>
    </xsl:if>
    <xsl:if test="@xhtml2:rowspan">
    <xsl:attribute name="rowspan">
        <xsl:value-of select="@xhtml2:rowspan"/>
      </xsl:attribute>
    </xsl:if>
  </xsl:template>

  <!-- === Metadata === -->
  <xsl:template name="metadataAttributes">
    <xsl:if test="@xhtml2:rel">
      <xsl:attribute name="rel">
        <xsl:value-of select="@xhtml2:rel"/>
      </xsl:attribute>
    </xsl:if>
  </xsl:template>
  <xsl:template name="handlerAttributes">
    <xsl:if test="@xhtml2:type">
      <xsl:attribute name="type">
         <xsl:value-of select="@xhtml2:type"/>
      </xsl:attribute>
    </xsl:if>
  </xsl:template>
</xsl:stylesheet>
