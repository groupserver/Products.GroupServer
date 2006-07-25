<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" 
  xmlns:email="http://xwft.net/namespaces/email/0.9/" 
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  
  <xsl:output method="html" encoding="UTF-8"/>
  
  <xsl:template name="email-present-results">
    <h1>Summart of Posts to 
    <span class="group"><xsl:value-of select="//metadata/group/text()"/></span></h1>
    <xsl:choose>
      <xsl:when test="number(@size)=0">
        <p>No posts</p>
      </xsl:when>
      <xsl:otherwise>
        <p>
          <span class="note"><a href="view_threads">Summary of topics</a>
          |
          <a href="view_results?summary=0">Full-text of posts</a>
        </span>
      </p>
        
        <p>Posts <strong><xsl:value-of select="@start"/></strong> to <strong><xsl:value-of select="number(@end)"/></strong> of the most recent posts are shown. There have been <strong><xsl:value-of select="@size"/></strong> posts in total. <xsl:value-of select="number(@end)-number(@start)+1"/> shown.</p>

        <table id="results">
          <tr>
            <th><a href="{@reversedate}" title="Sort by Date">Date Posted</a></th>
            <th>Subject</th>
            <th>Posted By</th>
          </tr>
          
          <xsl:for-each select="email:email">
            <tr>
              <xsl:if test="position() mod 2 != 0">
                <xsl:attribute name="class">alternate</xsl:attribute>
              </xsl:if>
              <td><xsl:value-of select="email:mailDate"/></td>
              <td><a href="view_email?id={@id}"><xsl:value-of select="email:mailSubject/text()"/></a></td>
              <td><xsl:choose>
              <xsl:when test="email:mailUserId/text() and email:mailFromName/text()">
                <a href="/contacts/{email:mailUserId/text()}/"><xsl:value-of select="email:mailFromName/text()"/></a>
              </xsl:when>
              <xsl:when test="email:mailUserId/text() and email:mailFromName/text() and email:mailUserId/@exists != '1'">
                <xsl:value-of select="email:mailFromName/text()"/>
              </xsl:when>
              <xsl:otherwise>
                Account Removed
              </xsl:otherwise>
            </xsl:choose></td>
          </tr>
        </xsl:for-each>
      </table>
      
      <div class="resultsnav">
        <xsl:if test="@prev">
          <a href="{@prev}">prev <xsl:value-of select="@prevbsize"/>
        </a>
      </xsl:if>
      <xsl:if test="@next">
        <a href="{@next}">next <xsl:value-of select="@nextbsize"/>
      </a>
    </xsl:if>
  </div>
</xsl:otherwise>
</xsl:choose>
</xsl:template>
</xsl:stylesheet>