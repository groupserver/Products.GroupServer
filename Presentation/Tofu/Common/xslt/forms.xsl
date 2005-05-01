<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:forms="http://xwft.org/namespaces/input/forms/0.9" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method="html" indent="yes" encoding="UTF-8"
            omit-xml-declaration="yes" doctype-public="-//W3C//DTD HTML 4.01 Transitional//EN" doctype-system="http://www.w3.org/TR/html4/loose.dtd"/>

    <xsl:template match="forms:form">
      <form action="{forms:target}" method="POST" enctype="multipart/form-data">
        <table cellpadding="3" cellspacing="3" border="0">
        <xsl:for-each select="forms:element">
          <xsl:choose>
            <xsl:when test="forms:type='textbox'">
              <tr>
                <xsl:call-template name="forms-textbox"/>
              </tr>
            </xsl:when>
            <xsl:when test="forms:type='submit'">
              <tr>
                <xsl:call-template name="forms-submit"/>
              </tr>
            </xsl:when>
            <xsl:when test="forms:type='file'">
              <tr>
                <xsl:call-template name="forms-file"/>
              </tr>
            </xsl:when>
            <xsl:otherwise>
            </xsl:otherwise>
          </xsl:choose>
        </xsl:for-each>
        </table>
      </form>
    </xsl:template>
    
    <xsl:template name="forms-textbox">
      <td><label for="{forms:name}"><xsl:value-of select="forms:label"/></label></td>
      <td><input type="text" name="{forms:name}" id="{forms:name}" size="{forms:length}" maxlength="{forms:maxlength}"/></td>
    </xsl:template>

    <xsl:template name="forms-submit">
      <td>&#160;</td><td align="right"><input type="submit" name="{forms:name}" value="{forms:value}"/></td>
    </xsl:template>

    <xsl:template name="forms-file">
      <td><label for="{forms:name}"><xsl:value-of select="forms:label"/></label></td>
      <td><input type="file" name="{forms:name}" value="{forms:value}"  size="{forms:length}"/></td>
    </xsl:template>

</xsl:stylesheet>