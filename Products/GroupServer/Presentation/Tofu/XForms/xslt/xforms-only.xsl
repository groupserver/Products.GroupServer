<?xml version="1.0" encoding="UTF-8" standalone="yes"?>

<xsl:stylesheet version="1.0"
  xmlns:xf="http://www.w3.org/2002/xforms" 
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:xhtml="http://www.w3.org/1999/xhtml"
  exclude-result-prefixes="xf xhtml">
  
  <xsl:output encoding="UTF-8" method="xml" standalone="no" version="1.0"
    omit-xml-declaration="yes" />

  <xsl:preserve-space elements="*"/>
  
  <xsl:include href="file://xforms"/>  
  
  <xsl:template match="xf:model">
    <!--input type="hidden" name="__submit__" value="{@id}" /--> 
    <input type="hidden" name="__models__" value="{@id}" />
    <xsl:apply-templates/>
  </xsl:template>
  
  <xsl:template match="xf:instance">
    <xsl:for-each select="data/*">
      <input type="hidden"
        name="__instance+{ancestor::xf:model/@id}+{name()}"
        value="{text()}" />
    </xsl:for-each>
    <xsl:apply-templates/>
  </xsl:template>
  
  <xsl:template match="xf:submission">
    <input type="hidden"
      name="__submission_action+{../@id}+{@id}" value="{@action}" />
    <input type="hidden"
      name="__submission_method+{../@id}+{@id}" value="{@method}" />
    <xsl:if test="@target">
      <input type="hidden"
        name="__submission_target+{../@id}+{@id}" value="{@target}" />
    </xsl:if>
    <xsl:apply-templates/>
  </xsl:template>
</xsl:stylesheet>
