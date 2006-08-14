<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:email="http://xwft.net/namespaces/email/0.9/" 
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

  <xsl:output method="html" encoding="UTF-8"/>

  <xsl:template match="email:sendemail">
    <xsl:if test="//metadata/group/@post = 'yes'">
      <xsl:choose>
        <xsl:when test="email:subject/text()">
          <h2 id="add_to_topic">Add to the topic <xsl:value-of select="email:subject/text()"/></h2>
        </xsl:when>
        <xsl:otherwise>
          <h2>Start a New Topic</h2>
        </xsl:otherwise>
      </xsl:choose>
      <xsl:choose>
        <xsl:when test="//output/metadata/group/@posting_blocked = 'yes'">
          <p>You have temporarily been blocked from posting to this forum. 
          You will be able to post again in
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
          <form method="post" 
            enctype="multipart/form-data"
            action="/Scripts/forms/post/addPost">
            <input type="hidden" name="groupId" 
              value="{//output/metadata/group/@id}"/>
            <input type="hidden" name="siteId" 
              value="{//output/metadata/division/@id}"/>
            <input type="hidden" name="replyToId" value="{@id}"/>

            <!-- Topic entry -->
            <div class="formelementtext">
              <xsl:choose>
                <xsl:when test="email:mailSubject/text()">
                  <!--Do not show the topic if we are replying to an -->
                  <!--  existing message.-->
                  <strong>Topic:</strong> 
                  <xsl:value-of select="email:mailSubject/text()"/>
                  <input type="hidden" name="topic" 
                    value="{email:mailSubject/text()}"/>
                </xsl:when>
                <xsl:otherwise>
                  <label for="post-topic" 
                    class="text">Topic</label>
                  <div class="hint">The topic (or subject) of your post.</div>
                  <input type="text" id="post-topic" name="topic" 
                    class="text"
                    title="The topic (or subject) of your post." 
                    value="Enter your new topic here"/>
                </xsl:otherwise>
              </xsl:choose>
            </div>

            <!-- Address Selector -->
            <div class="formelementtext">
              <xsl:choose>
                <xsl:when 
                  test="count(//user[@type='self']/emailaddresses/emailaddress)=1">
                  <!--Do not show the selector if the user has only -->
                  <!--  one address -->
                  <strong>From:</strong>
                  <xsl:value-of 
                    select="//user[@type='self']/emailaddresses/emailaddress/text()"/>
                  <!--Just because there is only one email, it does -->
                  <!--  not mean that we can avoid submitting it to -->
                  <!--  the form processor! -->
                  <input type="hidden" name="email" 
                    value="{//user[@type='self']/emailaddresses/emailaddress/text()}"/>

                </xsl:when>
                <xsl:otherwise>
                  <label for="post-email" class="text">Email From</label>
                  <div class="hint">The email address that you wish to
                    send the post from.</div>
                  <select name="email" id="post-email" 
                    title="The email address to send the post from." 
                    class="text">
                    <xsl:for-each 
                      select="//user[@type='self']/emailaddresses/emailaddress">
                      <option value="{./text()}">
                        <xsl:if test="./@preferred='1'">
                          <xsl:attribute name="selected">1</xsl:attribute>
                        </xsl:if>
                        <xsl:value-of select="./text()"/>
                      </option>
                    </xsl:for-each>
                  </select>
                </xsl:otherwise>
              </xsl:choose>
            </div>

            <!-- Message entry -->
            <div class="formelementtext">
              <label for="post-message" class="text">Message</label>
              <div class="hint">The message you wish to post to the
                group.</div>
              <textarea name="message" class="text"  id="post-message" 
                title="The message you wish to post to the group."></textarea>
            </div>

            <fieldset>
              <legend>Optional Fields</legend>
              <!--Tags entry-->
              <div class="formelementtext">
                <label for="post-tags" class="text">Tags</label>
                <div class="hint">The keywords that summarise your
                  post.</div>
                <input type="text" id="post-tags" name="tags" 
                  class="text" 
                  title="The keywords that summarise your post." value=""/>
              </div>

              <!--File entry-->
              <div class="formelementtext">
                <label for="post-file" class="text">File</label>
                <div class="hint">The file you wish to post to the
                  group.</div>
                <input type="file" name="file" 
                  id="post-file"
                  title="The file you wish to post to the group." 
                  class="text" value=""/>
              </div>
            </fieldset>

            <!-- The Post button-->
            <div class="formelementbutton">
              <div class="hint">
                  <xsl:choose>
                    <xsl:when test="email:subject/text()">
                      Add to the topic 
                      &#8220;<xsl:value-of select="email:subject/text()"/>&#8221;
                    </xsl:when>
                    <xsl:otherwise>
                      Start the new topic                      
                    </xsl:otherwise>
                  </xsl:choose>
                </div>
              <input type="submit" name="submit" class="button">
                <xsl:attribute name="value">
                  <xsl:choose>
                    <xsl:when test="email:subject/text()">Add</xsl:when>
                    <xsl:otherwise>Start</xsl:otherwise>
                  </xsl:choose>
                </xsl:attribute>
                <xsl:attribute name="title">
                  <xsl:choose>
                    <xsl:when
                      test="email:subject/text()">Add to the topic <xsl:value-of select="email:subject/text()"/></xsl:when>
                    <xsl:otherwise>Start the new topic</xsl:otherwise>
                  </xsl:choose>
                </xsl:attribute>
              </input>
            </div>
          </form>
        </xsl:otherwise>
      </xsl:choose>
    </xsl:if>
    <xsl:if test="//metadata/group/@post = 'no'">
      <p>
        If you are a <xsl:value-of select="metadata/division/@name"/> 
      member, you must 
      <a href="/login" title="Log in here">log in</a>
      to post messages.
    </p>
  </xsl:if>
</xsl:template>   

</xsl:stylesheet>

          <!--table border="0" cellspacing="5" class="sendmessage">
            <form action="send_email" method="POST">
              <input type="hidden" name="group_id" value="{//output/metadata/group/@id}"/>
              <input type="hidden" name="email_id" value="{@id}"/>
              <tr><td><strong>Subject:</strong></td>
              <xsl:choose>
                <xsl:when test="email:mailSubject/text()">
                  <td><xsl:value-of select="email:mailSubject/text()"/></td>
                </xsl:when>
                <xsl:otherwise>
                  <td><input type="text" size="40" name="subject" 
                  value="Enter a Title for Your New Topic Here"/></td>
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
        <tr><td colspan="2"><input type="submit" name="submit" 
        value="Send"/></td></tr>
      </form>
    </table-->
