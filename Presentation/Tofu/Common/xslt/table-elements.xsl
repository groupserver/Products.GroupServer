<?xml version="1.0" encoding="utf-8"?>

<!--
  - Table Elements Transform: XHTML2 to XHTML1
  -
  - Tables have changed very little between the two versions of XHTML,
  -   compared to other elements. Except for the summary tag, which is
  -   ignored because there is no XHTML1 equivilent.
  -
  - Michael JasonSmith, 2006
  -->

<xsl:stylesheet version="1.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:xev="http://www.w3.org/2001/xml-events"
  xmlns:xhtml2="http://www.w3.org/2002/06/xhtml2/"
  xmlns="http://www.w3.org/1999/xhtml">
  
  
  <xsl:template match="xhtml2:caption">
    <caption>
      <xsl:call-template name="commonAttributes"/>
      <xsl:call-template name="elementLink"/>
    </caption>
  </xsl:template>
  
  <xsl:template match="xhtml2:col">
    <col>
      <xsl:call-template name="commonAttributes"/>
      <xsl:call-template name="spanAttributes"/>
      <xsl:call-template name="elementLink"/>
    </col>
  </xsl:template>
  
  <xsl:template match="xhtml2:colgroup">
    <colgroup>
      <xsl:call-template name="commonAttributes"/>
      <xsl:call-template name="spanAttributes"/>
      <xsl:call-template name="elementLink"/>
    </colgroup>
  </xsl:template>

  <xsl:template match="xhtml2:summary">
    <!-- Summaries are not supported in XHTML1 -->
  </xsl:template>
  
  <xsl:template match="xhtml2:table">
    <table>
      <xsl:call-template name="commonAttributes"/>
      <xsl:call-template name="elementLink"/>
    </table>
  </xsl:template>
  
  <xsl:template match="xhtml2:tbody">
    <tbody>
      <xsl:call-template name="commonAttributes"/>
      <xsl:call-template name="elementLink"/>
    </tbody>
  </xsl:template>
  
  <xsl:template match="xhtml2:td">
    <td>
      <xsl:call-template name="commonAttributes"/>
      <xsl:call-template name="spanAttributes"/>
      <xsl:call-template name="elementLink"/>
    </td>
  </xsl:template>
  
  <xsl:template match="xhtml2:th">
    <th>
      <xsl:call-template name="commonAttributes"/>
      <xsl:call-template name="spanAttributes"/>
      <xsl:call-template name="elementLink"/>
    </th>
  </xsl:template>
  
  <xsl:template match="xhtml2:thead">
    <thead>
      <xsl:call-template name="commonAttributes"/>
      <xsl:call-template name="elementLink"/>
    </thead>
  </xsl:template>
  
   <xsl:template match="xhtml2:tfoot">
    <tfoot>
      <xsl:call-template name="commonAttributes"/>
      <xsl:call-template name="elementLink"/>
    </tfoot>
  </xsl:template>
  
  <xsl:template match="xhtml2:tr">
    <tr>
      <xsl:call-template name="commonAttributes"/>
      <xsl:call-template name="elementLink"/>
    </tr>
  </xsl:template>
</xsl:stylesheet>
