<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:email="http://xwft.net/namespaces/email/0.9/" 
                              xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

   <xsl:output method="html" encoding="UTF-8"/>
   
   <xsl:template match="email:sendemail">
       <xsl:choose>
         <xsl:when test="email:subject/text()">
           <h2 id="add_to_topic">Add to the "<xsl:value-of select="email:subject/text()"/>" topic</h2>
         </xsl:when>
         <xsl:otherwise>
           <h2>Start a new Topic</h2>
         </xsl:otherwise>
       </xsl:choose>
       <xsl:variable name="groupId" select="//metadata/group/@id"/>
       <xsl:choose>
         <xsl:when test="//groupmemberships/groupmembership[@id=$groupId]">
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
                      <td><input type="text" size="40" onfocus="javascript:this.value = ''" name="subject" value="Enter a Title for Your New Topic Here"/></td>
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
          <tr><td colspan="2"><input type="submit" name="submit" value="Send Email"/></td></tr>
          </form>
          </table>
       </xsl:when>
       <xsl:when test="//user/id/text()='Anonymous User'">
         You must be <a href="/login">logged in</a>, and a member of this group in order to post.
       </xsl:when>
       <xsl:otherwise>
         You must be a member of this group in order to post.
       </xsl:otherwise>
     </xsl:choose>
   </xsl:template>

</xsl:stylesheet>

