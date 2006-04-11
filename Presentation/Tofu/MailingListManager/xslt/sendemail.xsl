<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:email="http://xwft.net/namespaces/email/0.9/" 
                              xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

   <xsl:output method="html" encoding="UTF-8"/>

   <xsl:template match="email:sendemail">
       <xsl:if test="//metadata/group/@post = 'yes'">
          <xsl:choose>
              <xsl:when test="email:subject/text()">
                  <h2 id="add_to_topic">Add to the "<xsl:value-of select="email:subject/text()"/>" topic</h2>
              </xsl:when>
              <xsl:otherwise>
                  <h2>Start a new Topic</h2>
              </xsl:otherwise>
          </xsl:choose>
          <xsl:choose>
              <xsl:when test="//output/metadata/group/@posting_blocked = 'yes'">
                 <p>You have temporarily been blocked from posting to this forum. You will be able to post again in
                  <xsl:choose>
                      <xsl:when test="number(//output/metadata/group/@posting_allow_seconds) &gt; 60 and number(//output/metadata/group/@posting_allow_seconds) &lt; 3600">
                          <xsl:value-of select="number(//output/metadata/group/@posting_allow_seconds) div 60"/> minutes
                      </xsl:when>
                      <xsl:when test="number(//output/metadata/group/@posting_allow_seconds) &gt;= 3600">
                          <xsl:value-of select="number(//output/metadata/group/@posting_allow_seconds) div 3600"/> hours
                      </xsl:when>
                      <xsl:otherwise>
                          <xsl:value-of select="number(//output/metadata/group/@posting_allow_seconds)"/> seconds
                      </xsl:otherwise>
                  </xsl:choose>.</p>
              </xsl:when>
              <xsl:otherwise>
          <table border="0" cellspacing="5">
          <form action="send_email" method="POST">
          <input type="hidden" name="group_id" value="{//output/metadata/group/@id}"/>
          <input type="hidden" name="email_id" value="{@id}"/>
          <tr><td><strong>Subject:</strong></td>
              <xsl:choose>
                  <xsl:when test="email:mailSubject/text()">
                      <td><xsl:value-of select="email:mailSubject/text()"/></td>
                  </xsl:when>
                  <xsl:otherwise>
                      <td><input type="text" size="40" name="subject" value="Enter a Title for Your New Topic Here"/></td>
                  </xsl:otherwise>
              </xsl:choose>
          </tr>
          <tr><td><strong>Email From:</strong></td>
              <td><select name="email_address">
              <xsl:for-each select="//user[@type='self']/emailaddresses/emailaddress">
                  <option value="{./text()}">
                      <xsl:if test="./@preferred='1'">
                          <xsl:attribute name="selected">1</xsl:attribute>
                      </xsl:if>
                      <xsl:value-of select="./text()"/>
                  </option>
              </xsl:for-each>
          </select>
          </td></tr>
          <tr><td valign="top"><strong>Message:</strong></td>
              <td><textarea cols="72" rows="20" name="message"></textarea></td></tr>
          <tr><td colspan="2"><input type="submit" name="submit" value="Send"/></td></tr>
          </form>
          </table>
          </xsl:otherwise>
          </xsl:choose>
       </xsl:if>
   </xsl:template>   

</xsl:stylesheet>

