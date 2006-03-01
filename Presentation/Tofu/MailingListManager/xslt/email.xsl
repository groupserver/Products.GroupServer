<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:email="http://xwft.net/namespaces/email/0.9/" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
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
                                        <h1>Topic</h1>
                                        <h2>"<xsl:value-of select="email:email/email:mailSubject"/>" <a class="email-link" href="/r/topic/{email:email[position()=last()]/@id}">link</a></h2>
					<a name="top"/>
					<p><span class="note"><a href="view_threads">All Topics</a></span>
                                           &#160;&#160;&#160;&#160;
                                          <xsl:if test="//groupmemberships/groupmembership[@id=$groupId]">
                                            <span class="note"><a href="view_email?id={email:email[position()=last()]/@id}&amp;show_thread=1#add_to_topic">Add to Topic</a></span>
                                           &#160;&#160;&#160;&#160;
                                           <span class="note"><a href="view_send_email">Start a new Topic</a></span>
                                          </xsl:if>
                                        </p>
					<p>The "<xsl:value-of select="email:email/email:mailSubject"/>" Topic contains these posts:</p>

					<table id="results">
						<tr>
							<th>Date Posted</th>
							<th>Posted By</th>
						</tr>
							
						<xsl:for-each select="email:email">
							<tr>
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
                                        <h2>"<xsl:value-of select="email:email/email:mailSubject"/>" <a class="email-link" href="/r/post/{email:email[position()=last()]/@id}">link</a></h2>
					<p>
						<span class="note"><a href="view_results">all Posts</a></span> | <a href="{//content/@url}&amp;show_thread=1">"<xsl:value-of select="email:email/email:mailSubject"/>" Topic</a>
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
		
	</xsl:template>
	
	
	<xsl:template name="email-present-email">
		<a name="{@id}" />
		<p class="email-metadata">Posted <strong><xsl:value-of select="email:mailDate"/></strong> by <strong><xsl:choose>
                                                  <xsl:when test="email:mailUserId/text() and email:mailFromName/text()">
                                                      <a href="/contacts/{email:mailUserId/text()}/"><xsl:value-of select="email:mailFromName/text()"/></a>
                                                  </xsl:when>
                                                  <xsl:otherwise>
                                                      <xsl:value-of select="email:from"/>
                                                  </xsl:otherwise>
                                              </xsl:choose></strong></p>

                <xsl:if test="email:mailUserImage/text()">
                    <div class="userimage">
                        <a href="/contacts/{email:mailUserId/text()}"><img src="{email:mailUserImage/text()}" alt="Photo of {email:mailFromName/text()}"/></a>
                    </div>
                </xsl:if>

		<pre class="email-body">
			<xsl:call-template name="mailBody"><xsl:with-param name="email" select="."/><xsl:with-param name="pos" select="position()"/></xsl:call-template>
		</pre>
		
		<p class="email-navlink"><a href="{//content/@url}#top">top</a> <a class="email-link" href="/r/post/{@id}">link</a></p>
<div class="spacer">&#160;</div>

	</xsl:template>

    <xsl:template name="mailBody">
        <xsl:param name="email"/>
        <xsl:param name="pos"/>
        <xsl:choose>
            <xsl:when test="$pos = 1">
	        <span class="emailintro"><xsl:for-each select="$email/email:mailBody"><xsl:apply-templates /></xsl:for-each></span>                
            </xsl:when>
            <xsl:otherwise>
                <xsl:variable name="emailintro">
                    <xsl:for-each select="$email/email:mailIntro"><xsl:apply-templates /></xsl:for-each>
                </xsl:variable>
                <xsl:variable name="emailremainder">
                    <xsl:for-each select="$email/email:mailRemainder"><xsl:apply-templates /></xsl:for-each>
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

</xsl:stylesheet>
