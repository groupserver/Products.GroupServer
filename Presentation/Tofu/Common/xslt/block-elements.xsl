<?xml version="1.0" encoding="utf-8"?>

<!--
  - Block Elements XSL: Transform block elements from XHTML2 to XHTML1
  -
  - This particular transform handles paragraphs, which may or may
  -   not be images, and hypertext links.
  -
  - The text that the coe handles is similar to the following.
  -
  - <xhtml2:p 
  -   xhtml2:role="context-help"
  -   xhtml2:src=".../help.png"
  -   xhtml2:href="help-document"
  -   xev:event="onclick"
  -   xev:handler="doContextHelp">Help</xhtml2:p>
  -
  - It is transformed into something akin to the following.
  -
  -     <p class="context-help">
  -       <a href="help-document"
  -         onclick="doContextHelp('help-document')">
  -         <img src="help.png" alt="Help"/>
  -       </a>
  -     </p>
  -
  -  Michael JasonSmith, 2006
-->
  
<xsl:stylesheet version="1.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:xev="http://www.w3.org/2001/xml-events"
  xmlns:xhtml2="http://www.w3.org/2002/06/xhtml2/"
  xmlns="http://www.w3.org/1999/xhtml">

  <!-- Paragraph template -->
  <xsl:template match="xhtml2:p">
    <p>
      <xsl:call-template name="commonAttributes"/>
      <xsl:call-template name="elementLink"/>
    </p>
  </xsl:template>

  <!-- Generic div template -->
  <xsl:template match="xhtml2:div">
    <div>
      <xsl:call-template name="commonAttributes"/>
      <xsl:call-template name="elementLink"/>
    </div>
  </xsl:template>
  
  <!-- Block quote template -->
  <xsl:template match="xhtml2:blockquote">
    <blockquote>
      <xsl:call-template name="commonAttributes"/>
      <xsl:call-template name="elementLink"/>
    </blockquote>
  </xsl:template>
  
  <!-- Block code template -->
  <xsl:template match="xhtml2:blockcode">
    <pre>
      <xsl:attribute name="style">font-family: monospace;</xsl:attribute>
      <xsl:call-template name="commonAttributes"/>
      <xsl:call-template name="elementLink"/>
    </pre>
  </xsl:template>
 
  <!-- Preformatted text template -->
  <xsl:template match="xhtml2:pre">
    <pre>
      <xsl:call-template name="commonAttributes"/>
      <xsl:call-template name="elementLink"/>
    </pre>
  </xsl:template>

  <!-- Address template -->
  <xsl:template match="xhtml2:address">
    <div>
      <xsl:call-template name="commonAttributes"/>
      <xsl:call-template name="elementLink"/>
    </div>
  </xsl:template>

  <!-- Seperator template -->
  <xsl:template match="xhtml2:seperator">
    <hr/>
    <xsl:call-template name="commonAttributes"/>
  </xsl:template>
  
</xsl:stylesheet>
