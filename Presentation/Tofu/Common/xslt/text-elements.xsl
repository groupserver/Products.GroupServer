<?xml version="1.0" encoding="utf-8"?>

<!--
  - Text Elements XSL: Transform XHTML2 text elements to XHTML1 text elements
  -
  - Almost all the templates in this stylesheet are basic "pass through"
  -   rules, which do little other than move the tag from one namespace to
  -   another. The semantics of inline quotes changes between XHTML1 and 2
  -   but this stylesheet does not deal with that as it requires too much
  -   XSL voodo.
  -
  - Michael JasonSmith, 2006
  -->

<xsl:stylesheet version="1.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:xev="http://www.w3.org/2001/xml-events"
  xmlns:xhtml2="http://www.w3.org/2002/06/xhtml2/"
  xmlns="http://www.w3.org/1999/xhtml">


  <xsl:template match="xhtml2:abbr">
    <abbr>
      <xsl:call-template name="commonAttributes"/>
      <xsl:call-template name="elementLink"/>
    </abbr>
  </xsl:template>

  <xsl:template match="xhtml2:cite">
    <cite>
      <xsl:call-template name="commonAttributes"/>
      <xsl:call-template name="elementLink"/>
    </cite>
  </xsl:template>

  <xsl:template match="xhtml2:code">
    <code>
      <xsl:call-template name="commonAttributes"/>
      <xsl:call-template name="elementLink"/>
    </code>
  </xsl:template>

  <xsl:template match="xhtml2:dfn">
    <dfn>
      <xsl:call-template name="commonAttributes"/>
      <xsl:call-template name="elementLink"/>
    </dfn>
  </xsl:template>
  
  <xsl:template match="xhtml2:em">
    <em>
      <xsl:call-template name="commonAttributes"/>
      <xsl:call-template name="elementLink"/>
    </em>
  </xsl:template>
  
  <xsl:template match="xhtml2:kbd">
    <kbd>
      <xsl:call-template name="commonAttributes"/>
      <xsl:call-template name="elementLink"/>
    </kbd>
  </xsl:template>
  
  <xsl:template match="xhtml2:l">
    <span>
      <xsl:call-template name="commonAttributes"/>
      <xsl:call-template name="elementLink"/>
    </span>
    <br/>
  </xsl:template>

  <xsl:template match="xhtml2:quote">
    <q>
      <xsl:call-template name="commonAttributes"/>
      <xsl:call-template name="elementLink"/>
    </q>
  </xsl:template>

  <xsl:template match="xhtml2:samp">
    <samp>
      <xsl:call-template name="commonAttributes"/>
      <xsl:call-template name="elementLink"/>
    </samp>
  </xsl:template>

  <xsl:template match="xhtml2:span">
    <span>
      <xsl:call-template name="commonAttributes"/>
      <xsl:call-template name="elementLink"/>
    </span>
  </xsl:template>

  <xsl:template match="xhtml2:strong">
    <strong>
      <xsl:call-template name="commonAttributes"/>
      <xsl:call-template name="elementLink"/>
    </strong>
  </xsl:template>

  <xsl:template match="xhtml2:sub">
    <sub>
      <xsl:call-template name="commonAttributes"/>
      <xsl:call-template name="elementLink"/>
    </sub>
  </xsl:template>

  <xsl:template match="xhtml2:sup">
    <sup>
      <xsl:call-template name="commonAttributes"/>
      <xsl:call-template name="elementLink"/>
    </sup>
  </xsl:template>

  <xsl:template match="xhtml2:var">
    <var>
      <xsl:call-template name="commonAttributes"/>
      <xsl:call-template name="elementLink"/>
    </var>
  </xsl:template>

</xsl:stylesheet>
