<?xml version="1.0" encoding="utf-8"?>

<!--
  - Section Elements XSL: Transform XHTML2 section elements to XHTML1
  -
  - Sectioning is one of the big changes between the two forms of XHTML:
  -   the newer version has effectively deprecated the h1...h6 tags. Instead
  -   there are nested section tags, with h tags defining the names. With
  -   some jiggery pokery, the XHTML2 sections are mapped onto XHTML1 div
  -   and h1...h6 tags.
  -
  - Michael JasonSmith, 2006
  -->

<xsl:stylesheet version="1.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:xev="http://www.w3.org/2001/xml-events"
  xmlns:xhtml2="http://www.w3.org/2002/06/xhtml2/"
  xmlns="http://www.w3.org/1999/xhtml">
  
  <!-- 
    - The main trick is to use count(ancestor::xhtml2:section) 
    -   to calculate the current depth of the section. Then
    -   it is a process of adding the caclulated number to whatever
    -   is being processed at the time.
    -->
  
  <xsl:template match="xhtml2:section">
    <div>
      <xsl:attribute name="class"><!-- Ignore the line-break
        -->xhtml2-section-<xsl:value-of
          select="count(ancestor::xhtml2:section)+1"/>
      </xsl:attribute>
      <xsl:call-template name="commonAttributes"/>
      <xsl:call-template name="elementLink"/>
    </div>
  </xsl:template>
  
  <xsl:template match="xhtml2:h">
    <xsl:variable name="depth">
      <xsl:choose>
        <!-- highest valid HTML H level is H6; so anything nested deeper
             than 5 levels down just becomes H6 -->
        <xsl:when test="count(ancestor::xhtml2:section) &gt; 5">6</xsl:when>
        <xsl:otherwise>
          <xsl:value-of select="count(ancestor::xhtml2:section)"/>
        </xsl:otherwise>
      </xsl:choose>
    </xsl:variable>
    <xsl:element name="h{$depth}" namespace="http://www.w3.org/1999/xhtml">
      <xsl:call-template name="commonAttributes"/>
      <xsl:call-template name="elementLink"/>
    </xsl:element>
  </xsl:template>
</xsl:stylesheet>
