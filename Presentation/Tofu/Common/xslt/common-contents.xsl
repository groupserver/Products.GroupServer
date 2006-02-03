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
  
  <!-- 
    - Almost all elements can contain an href attribute
    -   which is handled here.
    -->
  <xsl:template name="elementLink">
    <xsl:choose>
      <!-- The element contains an href -->
      <xsl:when test="@xhtml2:href">
        <a>
          <xsl:call-template name="hypertextAttributes"/>
          <xsl:call-template name="elementContents"/>
        </a>
      </xsl:when>
      <!-- No href -->
      <xsl:otherwise>
        <xsl:call-template name="elementContents"/>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>

  <!-- Handle the contents of the element -->
  <xsl:template name="elementContents">
    <xsl:choose>
      <!-- When is a element not a element? When it is an image. -->
      <xsl:when test="@xhtml2:src">
        <xsl:call-template name="img"/>
      </xsl:when>
      <!-- If the element is a, well, element. -->
      <xsl:otherwise>
        <xsl:apply-templates />
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>
  
  <!-- Create an image tag, this is *not* a match for an image tag -->
  <xsl:template name="img">
    <img>
      <xsl:attribute name="alt" select="parent::text()"/><!--?-->
      <xsl:call-template name="embeddingAttributes"/>
    </img>
  </xsl:template>
</xsl:stylesheet>
