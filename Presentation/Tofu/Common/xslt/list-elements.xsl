<?xml version="1.0" encoding="utf-8"?>

<!--
  - List Elements XSL: Convert XHTML2 list elements to XHTML1
  -
  - Converting lists loses information: di tags cannot be converted, and
  -   none of the lists can have href or src tags. In addition, the
  -   navigation lists are converted to unordered lists.
  -
  - Michael JasonSmith, 2006
  -->

<xsl:stylesheet version="1.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:xev="http://www.w3.org/2001/xml-events"
  xmlns:xhtml2="http://www.w3.org/2002/06/xhtml2/"
  xmlns="http://www.w3.org/1999/xhtml">

  <!-- === Children of the List === -->

  <xsl:template match="xhtml2:li">
    <li>
      <xsl:call-template name="commonAttributes"/>
      <xsl:call-template name="elementLink"/>
    </li>
  </xsl:template>

  <xsl:template match="xhtml2:label">
    <p class="xhtml2-label">
      <xsl:call-template name="commonAttributes"/>
      <xsl:call-template name="elementLink"/>
    </p>
  </xsl:template>
        
  <!-- === Simple Lists === -->
  
  <xsl:template match="xhtml2:ul">
   <div class="xhtml2-ul">
     <xsl:call-template name="commonAttributes"/>
     <xsl:apply-templates select="xhtml2:label"/> 
     <ul>
       <xsl:apply-templates select="xhtml2:li"/>
     </ul>
   </div>
  </xsl:template>
  
  <xsl:template match="xhtml2:ol">
   <div class="xhtml2-ol">
     <xsl:call-template name="commonAttributes"/>
     <xsl:apply-templates select="xhtml2:label"/> 
     <ol>
       <xsl:apply-templates select="xhtml2:li"/>
     </ol>
   </div>
  </xsl:template>
  
  <!-- === Navigation Lists === -->
   <xsl:template match="xhtml2:nl">
   <div class="xhtml2-nl">
     <xsl:call-template name="commonAttributes"/>
     <xsl:apply-templates select="xhtml2:label"/> 
     <ul>
       <xsl:apply-templates select="xhtml2:li"/>
     </ul>
   </div>
  </xsl:template>
  
  <!-- === Description Lists === -->
  <xsl:template match="xhtml2:dl">
   <div class="xhtml2-dl">
     <xsl:call-template name="commonAttributes"/>
     <xsl:apply-templates select="xhtml2:label"/> 
      <dl>
       <xsl:apply-templates select="xhtml2:di"/>
     </dl>
   </div>
  </xsl:template>

  <!-- Ignore description items, as they are not in XHTML1 -->
  <!-- Note: The di is required, even though it is ignored -->
  <xsl:template match="xhtml2:di">
    <xsl:apply-templates />
  </xsl:template>

  <xsl:template match="xhtml2:dt">
    <dt>
      <xsl:call-template name="commonAttributes"/>
      <xsl:call-template name="elementLink"/>
    </dt>
  </xsl:template>

  <xsl:template match="xhtml2:dd">
    <dd>
      <xsl:call-template name="commonAttributes"/>
      <xsl:call-template name="elementLink"/>
    </dd>
  </xsl:template>
  
</xsl:stylesheet>
