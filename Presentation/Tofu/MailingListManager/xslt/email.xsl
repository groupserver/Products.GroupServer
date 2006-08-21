<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
  xmlns:email="http://xwft.net/namespaces/email/0.9/"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  exclude-result-prefixes="email">
  
  <xsl:output method="html" encoding="UTF-8"/>
  
  <xsl:include href="file://MailingListManager/xslt/results"/>
  <xsl:include href="file://MailingListManager/xslt/sitesearchresults"/>
  <xsl:include href="file://MailingListManager/xslt/threaded"/>
  <xsl:include href="file://MailingListManager/xslt/sendemail"/>

  <xsl:template match="email:collection">
    <xsl:variable name="groupId" select="//metadata/group/@id"/>
    <xsl:variable name="userid" select="//user[@type='self']/id/text()"/>
    <xsl:choose>
      <xsl:when test="email:threadsummary">
        <xsl:for-each select="email:threadsummary">
          <xsl:call-template name="email-present-threadsummary"/>
        </xsl:for-each>
      </xsl:when>
      <xsl:when test="@sitesearch='1'">
        <xsl:call-template name="email-present-sitesearch-results"/>
      </xsl:when>
      <xsl:when test="@resultsummary='1'">
        <xsl:call-template name="email-present-results"/>
      </xsl:when>
      <xsl:otherwise>
        
        <xsl:if test="@fullthread='1'">
          <h1>
            Topic: 
            <span class="topicName">
              <xsl:value-of select="email:email/email:mailSubject"/>
            </span>
          </h1>
          
          <a name="top"/>
          <p>
            <xsl:if test="//groupmemberships/groupmembership[@id=$groupId]">
              <xsl:if test="//metadata/group/@post = 'yes'">
                <span class="note">
                  <a href="view_email?id={email:email[position()=last()]/@id}&amp;show_thread=1#add_to_topic">Add to this topic</a>
                </span>
                &#160;&#160;&#160;&#160;
                <span class="note">
                  <a href="view_send_email">Start a new topic</a>
                </span>
              </xsl:if>
            &#160;&#160;&#160;&#160;
            </xsl:if>
            <span class="note">
              <a href="view_threads"><xsl:value-of select="//metadata/group"/>
                Topics</a>
            </span>
            &#160;&#160;&#160;&#160;
            <span class="note">
              <a class="email-link" 
                href="/r/topic/{email:email[position()=last()]/@id}">Short
                link</a>
            </span>
          </p>
          
          <xsl:apply-templates select="bulletlist[@class='topicNavigation']"/>
          <p>The topic 
            <q><xsl:value-of select="email:email/email:mailSubject"/></q>
            contains the following posts.</p>

          <table id="results">
            <tr>
              <th/>
              <th>Date Posted</th>
              <th>Posted By</th>
            </tr>
            
            <xsl:for-each select="email:email">
              <tr>
               <td>
                  <xsl:apply-templates select="email:fileNotification" mode="summary"/>
                </td>
                <td><a href="{//content/@url}#{@id}"><xsl:value-of select="email:mailDate"/></a></td>
                <td><xsl:choose>
                    <xsl:when test="email:mailUserId/text() and email:mailFromName/text()">
                      <xsl:choose>
                        <xsl:when test="$userid = email:mailUserId/text()">
                          <span class="emailname-self"><xsl:value-of select="email:mailFromName/text()"/></span>
                        </xsl:when>
                        <xsl:otherwise>
                          <xsl:value-of select="email:mailFromName/text()"/>
                        </xsl:otherwise>
                      </xsl:choose>
                    </xsl:when>
                    <xsl:otherwise>
                      <xsl:value-of select="email:from"/>
                    </xsl:otherwise>
                  </xsl:choose></td>
              </tr>
            </xsl:for-each>
          </table>
        </xsl:if>
        <xsl:if test="@fullthread!='1'">
          <h1>Post</h1>
          <h2>Topic: <xsl:value-of select="email:email/email:mailSubject"/> <a class="email-link" href="/r/post/{email:email[position()=last()]/@id}">(link)</a></h2>
          <p>
            <span class="note">
              <a href="{//content/@url}&amp;show_thread=1">The topic
              <xsl:value-of select="email:email/email:mailSubject"/></a>
              | 
              <a href="view_results">Summary of posts</a>
            </span>
          </p>
        </xsl:if>
        
        <!--Showing the full-text of all the posts-->
        <xsl:if test="not(@fullthread) and @resultsummary='0'">
          <h1>Posts to 
          <span class="group"><xsl:value-of select="//metadata/group/text()"/></span></h1>
          <p>
            <span class="note">
              <a href="view_threads">Summary of topics</a>
              | 
              <a href="view_results">Summary of posts</a>
            </span>
          </p>

        </xsl:if>


        <br/>
        
        <script language="Javascript">
          function showHideInline(showelementids, hideelementids) {
          for (var i = 0; i &lt; showelementids.length; i++) {
          var n = document.getElementById(showelementids[i]);
          n.style['display'] = 'inline';
          }
          for (var i = 0; i &lt; hideelementids.length; i++) {
          var n = document.getElementById(hideelementids[i]);
          n.style['display'] = 'none';
          }
          }
        </script>
        <div class="emailwrap">
          <xsl:for-each select="email:email">
            <div class="emaildetails">
              <xsl:choose>
                <xsl:when test="$userid = email:mailUserId/text()">
                  <xsl:choose>
                    <xsl:when test="position() mod 2 = 0"><xsl:attribute name="class">emaildetails-self-even</xsl:attribute></xsl:when>
                    <xsl:otherwise>
                      <xsl:attribute name="class">emaildetails-self-odd</xsl:attribute>
                    </xsl:otherwise>
                  </xsl:choose>
                </xsl:when>
                <xsl:when test="position() mod 2 = 0">
                  <xsl:attribute name="class">emaildetails-even</xsl:attribute>
                </xsl:when> 
                <xsl:otherwise>
                  <xsl:attribute name="class">emaildetails-odd</xsl:attribute>
                </xsl:otherwise>
              </xsl:choose>
              <xsl:call-template name="email-present-email"/>
            </div>
          </xsl:for-each>
        </div>
      </xsl:otherwise>
    </xsl:choose>
    <xsl:apply-templates select="bulletlist[@class='topicNavigation']"/>
  </xsl:template>


  <xsl:template name="email-present-email">
    <p id="{@id}" class="email-metadata">
      <xsl:if test="//@resultsummary='0'">
        <h2><xsl:value-of select="email:mailSubject"/></h2>
      </xsl:if>
      Posted <strong><xsl:value-of select="email:mailDate"/></strong> by <strong><xsl:choose>
          <xsl:when test="email:mailUserId/text() and email:mailFromName/text()">
            <a href="/contacts/{email:mailUserId/text()}/"><xsl:value-of select="email:mailFromName/text()"/></a>
          </xsl:when>
          <xsl:otherwise>
            <xsl:value-of select="email:from"/>
          </xsl:otherwise>
        </xsl:choose></strong> (<a class="email-link" href="/r/post/{@id}">short link</a>)
    </p>

    <xsl:if test="email:mailUserImage/text()">
      <div class="userimage">
        <a href="/contacts/{email:mailUserId/text()}"><img src="{email:mailUserImage/text()}" alt="Photo of {email:mailFromName/text()}"/></a>
      </div>
      <div class="propimage"></div>
    </xsl:if>

    <pre class="email-body">
      <xsl:call-template name="mailBody">
        <xsl:with-param name="email" select="."/>
        <xsl:with-param name="pos" select="position()"/>
      </xsl:call-template>
    </pre>
    
    <xsl:apply-templates select="email:fileNotification" mode="full"/>
    
    <p class="email-navlink"><a href="{//content/@url}#top">top</a></p>
    <div class="clear"></div>                
  </xsl:template>

  <xsl:template name="mailBody">
    <xsl:param name="email"/>
    <xsl:param name="pos"/>
    <xsl:choose>
      <xsl:when test="($pos = 1)">
        <span class="emailintro">
          <xsl:for-each select="$email/email:mailBody">
            <xsl:apply-templates />
          </xsl:for-each>
        </span>                
      </xsl:when>
      <xsl:when test="//@resultsummary='0'">
        <span class="emailintro">
          <xsl:for-each select="$email/email:mailBody">
            <xsl:apply-templates />
          </xsl:for-each>
        </span>
      </xsl:when>
      <xsl:otherwise>
        <xsl:variable name="emailintro">
          <xsl:for-each select="$email/email:mailIntro">
            <xsl:apply-templates />
          </xsl:for-each>
        </xsl:variable>
        <xsl:variable name="emailremainder">
          <xsl:for-each select="$email/email:mailRemainder">
            <xsl:apply-templates />
          </xsl:for-each>
        </xsl:variable>
        <span class="emailintro"><xsl:copy-of select="$emailintro"/></span>
        
        <xsl:if test="$emailremainder and normalize-space($emailremainder) != '' and normalize-space($emailremainder) != ' '">
          <span class="emailremainder" id="emailrem{$email/@id}"><xsl:copy-of select="$emailremainder" /></span>
          <div class="emailshowremainder" id="emailshowrem{$email/@id}">
            <a href="javascript:showHideInline(['emailrem{$email/@id}'],['emailshowrem{$email/@id}'])">show remainder of email</a>
          </div>
        </xsl:if>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>

  <!-- We deliberately have our own link processing here, seperate from the rest, because we want to
  be especially careful about processing email -->
  <xsl:template match="email:link"><a href="{@url}"><xsl:value-of select="text()"/></a></xsl:template>

  <xsl:template match="email:fileNotification" mode="summary">
    <xsl:call-template name="fileIcon">
      <xsl:with-param name="type" select="type"/>
    </xsl:call-template>
  </xsl:template>
  
  <xsl:template name="fileIcon">
    <xsl:param name="type"/>
    <img alt="{type}"
      src="/Presentation/Tofu/FileLibrary2/images/16x16/mimetypes/{translate(type, '/', '-')}.png"/>    
  </xsl:template>
  
  <xsl:template match="email:fileNotification" mode="full">
    <div class="fileNotification"> 
      <p>The following file was added to this topic.</p>
      <ul>
        <li>Name: <xsl:call-template name="fileIcon">
            <xsl:with-param name="type" select="type"/>
          </xsl:call-template>
          <a href="/r/file/{@fileId}">
            <xsl:value-of select="name"/></a></li>
        <li>Type: <xsl:value-of select="type"/></li>
        <li>Size: <xsl:value-of select="size"/></li>
      </ul>
    </div>
  </xsl:template>
</xsl:stylesheet>
