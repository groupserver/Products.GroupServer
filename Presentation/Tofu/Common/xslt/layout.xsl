<?xml version="1.0" ?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:template match="paragraph | p">
    <p><xsl:apply-templates /></p>
</xsl:template>

<xsl:template match="div">
    <div class="{@class}"><xsl:apply-templates /></div>
</xsl:template>

<xsl:template match="heading1 | h1">
<h1>
<xsl:if test="@id">
<xsl:attribute name="id"><xsl:value-of select="@id"/></xsl:attribute>
</xsl:if>
<xsl:value-of select="." /></h1>
</xsl:template>

<xsl:template match="pparagraph">
&#160;
</xsl:template>

<xsl:template match="pheading1">
&#160;
</xsl:template>

<xsl:template match="heading2 | h2">
<h2>
<xsl:if test="@id">
<xsl:attribute name="id"><xsl:value-of select="@id"/></xsl:attribute>
</xsl:if>
<xsl:value-of select="." /></h2>
</xsl:template>

<xsl:template match="heading3 | h3">
<h3>
<xsl:if test="@id">
<xsl:attribute name="id"><xsl:value-of select="@id"/></xsl:attribute>
</xsl:if>
<xsl:value-of select="." /></h3>
</xsl:template>

<xsl:template match="heading4 | h4">
<h4>
<xsl:if test="@id">
<xsl:attribute name="id"><xsl:value-of select="@id"/></xsl:attribute>
</xsl:if>
<xsl:value-of select="." /></h4>
</xsl:template>

<xsl:template match="bold">
<strong><xsl:value-of select="." /></strong>
</xsl:template>

<xsl:template match="em">
<em><xsl:value-of select="." /></em>
</xsl:template>

<xsl:template match="br">
<xsl:value-of select="." /><br/>
</xsl:template>

<xsl:template match="bulletlist | ul">
<ul class="{@class}">
<xsl:for-each select="listitem | li">
<li class="{@class}"><xsl:apply-templates /></li>
</xsl:for-each>
</ul>
</xsl:template>

<xsl:template match="numberedlist">
<ol>
<xsl:for-each select="listitem">
<li><xsl:apply-templates /></li>
</xsl:for-each>
</ol>
</xsl:template>

<xsl:template match="link">
	<a href="{@url}">
		<xsl:apply-templates/>
	</a>
</xsl:template>
  
<xsl:template match="span">
    <span class="{@class}">
      <xsl:apply-templates />
    </span>
</xsl:template>
  
<xsl:template match="a">
    <a href="{@href}">
      <xsl:if test="@class"><xsl:attribute name="class"><xsl:value-of select="@class"/></xsl:attribute></xsl:if>
      <xsl:apply-templates />
    </a>
</xsl:template>

<xsl:template match="anchor">
<a><xsl:attribute name="name"><xsl:value-of select="@name"/></xsl:attribute></a>
</xsl:template> 

<xsl:template match="registration_box">
        <xsl:apply-templates select="//input[@id='registration']"/>
</xsl:template>

<xsl:template match="//input[@id='registration']">
        <form action="{@target}" method="POST">
		<table class="FormLayout">

                        <tr><td>Fields marked <img src="/Presentation/Tofu/XForms/images/required.gif"/> are required</td></tr>
                        <tr><td>&#160;</td></tr>
			<xsl:for-each select="object">
                           <xsl:choose>
                              <xsl:when test="@type='string'">
				<tr>
					<td align="left" valign="top"><strong><span class="help" title="{description}"><xsl:value-of select="label"/>:</span>
                                                                      </strong></td>
					<td align="left" valign="top">
                                            <input type="text" name="{@id}" value="{element}" size="50" /><xsl:if test="@required"><img src="/Presentation/Tofu/XForms/images/required.gif"/></xsl:if>
					</td>
				</tr>
                              </xsl:when>
                              <xsl:when test="@type='text'">
				<tr>
					<td align="left" valign="top"><strong><span class="help" title="{description}"><xsl:value-of select="label"/>:</span></strong></td>
					<td align="left" valign="top">
					    <textarea type="text" name="{@id}" cols="50"><xsl:value-of select="element"/><xsl:text>
</xsl:text></textarea><xsl:if test="@required"><img src="/Presentation/Tofu/XForms/images/required.gif"/></xsl:if>
					</td>
				</tr>
                              </xsl:when>
                              <xsl:when test="@type='choice'">
				<tr>
					<td align="left" valign="top"><strong><span class="help" title="{description}"><xsl:value-of select="label"/>:</span></strong></td>
					<td align="left" valign="top">
					    <select name="{@id}">
                                              <option value="">----select----</option>
                                              <xsl:for-each select="element">
                                                <option value="{./text()}"><xsl:value-of select="./text()"/></option>
                                              </xsl:for-each>
                                            </select><xsl:if test="@required"><img src="/Presentation/Tofu/XForms/images/required.gif"/></xsl:if>
					</td>
				</tr>
                              </xsl:when>
                              <xsl:when test="@type='hidden'">
                                  <input type="hidden" name="{@id}" value="{element}" />
                              </xsl:when>
                           </xsl:choose>
			</xsl:for-each>
			<tr>
  				<td align="left" valign="top"></td>
  				<td align="right" valign="top">
  					<input type="submit" name="{@id}" value=" Register "/>
  				</td>
			</tr>
	        </table>
        </form>
</xsl:template>

<xsl:template match="userverification">
        <xsl:apply-templates select="//input[@id='userverification']"/>
</xsl:template>

<xsl:template match="//input[@id='userverification']">
        <form action="{@target}" method="POST">
		<table class="FormLayout">
			<xsl:for-each select="object">
                           <xsl:choose>
                              <xsl:when test="@type='string'">
				<tr>
					<td align="left" valign="top"><strong><span class="help" title="{description}"><xsl:value-of select="label"/>:</span></strong></td>
					<td align="left" valign="top">
					    <input type="text" name="{@id}" size="20" />
					</td>
				</tr>
                              </xsl:when>
                              <xsl:when test="@type='hidden'">
                                  <input type="hidden" name="{@id}" value="{element}" />
                              </xsl:when>
                           </xsl:choose>
			</xsl:for-each>

			<tr>
  				<td align="left" valign="top">
  					<input type="submit" name="remove" value=" Remove this account "/>
                                </td>
  				<td align="right" valign="top">
  					<input type="submit" name="verify" value=" Accept Conditions "/>
  				</td>
			</tr>
	        </table>
        </form>
</xsl:template>



<xsl:template match="image">
<xsl:choose>
    <xsl:when test="@align='center'">
       <center>
        <img src="images/{@src}" alt="{@alt}" title="{@title}" border="0"/>
       </center>
    </xsl:when>
    <xsl:otherwise>
       <img src="images/{@src}" alt="{@alt}" align="{@align}" title="{@title}" border="0"/>
    </xsl:otherwise>
</xsl:choose>
</xsl:template>


<!-- News Feeds Start -->

<xsl:template match="channel">
<h1><xsl:value-of select="title"/></h1>
<xsl:apply-templates select="description"/>
<xsl:apply-templates select="item" />
</xsl:template>

<xsl:template match="description">
<xsl:apply-templates />
</xsl:template>

<xsl:template match="item">
	<h3><xsl:value-of select="title"/></h3>
	<h4><xsl:value-of select="pubDate"/></h4>
	<xsl:apply-templates select="description"/>
</xsl:template>

<!-- News Feeds Ends -->

<!-- FAQs Start -->
<xsl:template match="faqs">
	<xsl:apply-templates select="faq"/>
</xsl:template>

<xsl:template match="faq">
	<xsl:apply-templates select="question" mode="faq"/>
	<xsl:apply-templates select="answer" mode="faq"/>
</xsl:template>

<xsl:template match="question" mode="faq">
	<em><xsl:apply-templates /></em>
</xsl:template>

<xsl:template match="answer" mode="faq">
	<p><xsl:apply-templates /></p>
</xsl:template>
<!-- FAQs End -->

<!-- Groups Files Starts -->
<xsl:template match="collection">
	<xsl:choose>
		<xsl:when test="@id='files'">
			<xsl:apply-templates select="batch" mode="files"/>
		</xsl:when>
		<xsl:when test="@id='messages'">
			<xsl:apply-templates select="batch" mode="messages"/>
		</xsl:when>
	</xsl:choose>
	
</xsl:template>


<!-- Files Start -->
<xsl:template match="batch" mode="files">
<table class="files" border="0" cellspacing="0" cellpadding="0">
		<tr> 
                <td colspan="5"><img src="/images/layout/spacer.gif" width="1" height="15"/></td>
              </tr>
              <tr> 
                <th>File Name:</th>
                <th><img src="/images/layout/spacer.gif" width="15" height="1"/></th>
                <th>Date:</th>
                <th><img src="/images/layout/spacer.gif" width="15" height="1"/></th>
                <th>Size:</th>
                <th><img src="/images/layout/spacer.gif" width="15" height="1"/></th>
                <th>Contributor:</th>
                <th><img src="/images/layout/spacer.gif" width="15" height="1"/></th>
                <th>&#160;</th>
              </tr>
              <tr> 
                <td colspan="7"><img src="/images/layout/spacer.gif" width="1" height="8"/></td>
              </tr>
			<xsl:apply-templates select="batchitems" mode="files"/>
	</table>
	<xsl:apply-templates select="navigation"/>
	<xsl:apply-templates select="//input[@id='add_file']"/>
</xsl:template>

<xsl:template match="batchitems" mode="files">
	<xsl:for-each select="file">
              <tr> 
                <td><a href="{@url}"><xsl:apply-templates/></a></td>
                <td>&#160;</td>
                <td><xsl:value-of select="@lastmodified"/></td>
                <td>&#160;</td>
                <td><xsl:value-of select="@size"/></td>
                <td>&#160;</td>
                <td>
                    <table border="0" cellspacing="0" cellpadding="0">
                       <tr>
                          <td><a href="{@ownerurl}"><xsl:value-of select="@ownerpreferredname"/></a></td>
                          <td><img src="/images/layout/spacer.gif" width="5" height="1"/></td>
                          <td><a href="{@ownerurl}"><xsl:value-of select="@ownerlastname"/></a></td>
                       </tr>
                    </table>


                </td>
                <td>&#160;</td>
                <td><xsl:choose>
                     <xsl:when test="@allowremoval=1"><a href="removeFile?file_id={@id}">remove</a></xsl:when>
                     <xsl:otherwise>&#160;</xsl:otherwise>
                    </xsl:choose></td>
              </tr>
		<tr> 
                <td colspan="7"><img src="/images/layout/spacer.gif" width="1" height="6"/></td>
              </tr>
  </xsl:for-each>
</xsl:template>

<xsl:template match="navigation">
<table border="0" cellspacing="0" cellpadding="0">
		<tr>
			<td colspan="3"><img src="/images/layout/spacer.gif" width="1" height="15"/></td>
		</tr>
              <tr> 
                <td>
				<xsl:choose>
					<xsl:when test="count(previous)!=0">
						<a href="{previous/@url}">&lt;&lt;&#160;Previous</a>
					</xsl:when>
					<xsl:otherwise>
						<img src="/images/layout/spacer.gif" width="1" height="1"/>
					</xsl:otherwise>
				</xsl:choose>
		</td>
                <td><img src="/images/layout/spacer.gif" width="25" height="1"/></td>
                <td>
				<xsl:choose>
					<xsl:when test="count(next)!=0">
						<a href="{next/@url}">Next&#160;&gt;&gt;</a>
					</xsl:when>
					<xsl:otherwise>
						<img src="/images/layout/spacer.gif" width="1" height="1"/>
					</xsl:otherwise>
				</xsl:choose>
			</td>
              </tr>
	</table>
</xsl:template>

<xsl:template match="//input[@id='add_file']">
<form action="{@target}" method="post" enctype="multipart/form-data">
	<table border="0" cellspacing="0" cellpadding="0">
		<tr>
			<td><img src="/images/layout/spacer.gif" width="1" height="15"/></td>
		</tr>
		<tr>
			<td><h3>Add a File</h3></td>
		</tr>
		<tr>
			<td><input type="file" name="{object/@id}"/></td>
		</tr>
		<tr>
			<td><img src="/images/layout/spacer.gif" width="1" height="10"/></td>
		</tr>
		<tr>
			<td align="right"><input type="submit" name="add" value="Add File"/></td>
		</tr>
	</table>
</form>
</xsl:template>

<!-- Files End -->


<!-- Messages Start -->

<xsl:template match="collection[@id='recentmail']">
	<h3>Recent Posts (last 3 days)</h3>
<table border="0" cellspacing="0" cellpadding="0" class="messages">
        <tr> 
          <th>Subject:</th>
          <th><img src="/images/layout/spacer.gif" width="10" height="1"/></th>
          <th>Sent By:</th>
          <th><img src="/images/layout/spacer.gif" width="10" height="1"/></th>
          <th>Date:</th>
        </tr>
        <tr> 
          <td colspan="5"><img src="/images/layout/spacer.gif" width="1" height="10"/></td>
        </tr>
		<xsl:apply-templates select="batch/batchitems" mode="messages"/>
      </table>
</xsl:template>

<xsl:template match="batch/batchitems" mode="messages">
<xsl:for-each select="message">
		<tr> 
			<td><a href="{@url}" title="View this post"><xsl:value-of select="@subject"/></a></td>
			<td>&#160;</td>
			 <td><a href="mailto:{@fromemail}" title="Email {@from}"><xsl:value-of select="@from"/></a></td>
		         <td>&#160;</td>
		        <td><xsl:value-of select="@date"/></td>    
		</tr>
		<tr> 
                <td colspan="5"><img src="/images/layout/spacer.gif" width="1" height="5"/></td>
              </tr>
  </xsl:for-each>
</xsl:template>

<xsl:template match="collection[@id='archive']">
<h3>Archive</h3>
	<xsl:apply-templates select="batch/batchitems" mode="archive"/>
</xsl:template>

<xsl:template match="batch/batchitems" mode="archive">
	<ul class="archive">
		<xsl:apply-templates select="archive"/>
	</ul>
</xsl:template>

<xsl:template match="archive">
	<li>
		<a href="{@url}"><xsl:value-of select="."/></a>
	</li>
</xsl:template>


<xsl:template match="collection[@id='email']">
	<h3>Archived Posts: <xsl:value-of select="batch/batchitems/message[@current='1']/@subject"/></h3>
		<xsl:apply-templates select="batch/batchitems/message" mode="email"/>
</xsl:template>

<xsl:template match="batch/batchitems/message" mode="email">
<table border="0" cellspacing="0" cellpadding="0" class="email">
       <tr> 
       	<td>
			<table border="0" cellspacing="0" cellpadding="0">
				<tr>
					<td><strong><xsl:value-of select="@subject"/></strong></td>
					<td><img src="/images/layout/spacer.gif" width="15" height="1"/></td>
					<td><xsl:value-of select="@date"/></td>
				</tr>
			</table>
		</td>
        </tr>
	<tr>
		<td><a href="{@fromemail}" title="Email {@from}"><xsl:value-of select="@from"/></a></td>
	</tr>
	<tr>
		<td><img src="/images/layout/spacer.gif" width="1" height="15"/></td>
	</tr>
	<tr>
		<td><pre><xsl:value-of select="body"/></pre></td>
	</tr>
      </table>

	<xsl:choose>
			<xsl:when test="count(message)!=0">
				<xsl:apply-templates select="message" mode="reply"/>
			</xsl:when>
	</xsl:choose>
</xsl:template>

<xsl:template match="message" mode="reply">
	<table border="0" cellspacing="0" cellpadding="0" class="email">
	<tr>
		<td><img src="/images/layout/spacer.gif" width="1" height="20"/></td>
	</tr>
       <tr> 
       	<td>
			<table border="0" cellspacing="0" cellpadding="0">
				<tr>
					<td><strong><xsl:value-of select="@subject"/></strong></td>
					<td><img src="/images/layout/spacer.gif" width="15" height="1"/></td>
					<td><xsl:value-of select="@date"/></td>
				</tr>
			</table>
		</td>
        </tr>
	<tr>
		<td><a href="{@fromemail}" title="Email {@from}"><xsl:value-of select="@from"/></a></td>
	</tr>
	<tr>
		<td><img src="/images/layout/spacer.gif" width="1" height="15"/></td>
	</tr>
	<tr>
		<td><pre><xsl:value-of select="body"/></pre></td>
	</tr>
      </table>
</xsl:template>
<!-- Messages Ends -->

<!-- Groups Files Ends -->


<!-- Forgotten Password Starts -->

<xsl:template match="forgottenpassword">
<form action="{//input[@id='forgottenpassword']/@target}" method="post">
	<table border="0" cellspacing="0" cellpadding="0">
		<tr>
			<td colspan="3"><img src="/images/layout/spacer.gif" width="1" height="15"/></td>
		</tr>
		<tr>
			<td><strong><xsl:value-of select="//input[@id='forgottenpassword']/object/label/text()"/>:</strong></td>
			<td><img src="/images/layout/spacer.gif" width="10" height="1"/></td>
			<td><input type="text" name="{//input[@id='forgottenpassword']/object[@id='username']/@id}"/></td>
		</tr>
		<tr>
			<td colspan="3"><img src="/images/layout/spacer.gif" width="1" height="10"/></td>
		</tr>
		<tr>
			<td colspan="3" align="right"><input type="submit" value="Send" name="Send"/></td>
		</tr>
	</table>
</form>
</xsl:template>

<!-- Forgotten Password Ends -->

<!-- Error/Result Messages Start -->
<xsl:template name="result-messages">
    <xsl:if test="//output/messages/message[@type='result']">
    <div class="message-result">
       <xsl:for-each select="//output/messages/message[@type='result']">
         <xsl:apply-templates />
       </xsl:for-each>
    </div>
    </xsl:if>
    <xsl:if test="//output/messages/message[@type='error']">
    <div class="message-error">
       <xsl:for-each select="//output/messages/message[@type='error']">
         <xsl:apply-templates />
       </xsl:for-each>
    </div>
    </xsl:if>
</xsl:template>
<!-- Error/Result Messages End -->

<xsl:template name="searcharea">
	<h3>Site Search</h3>
	<input type="text" class="text" name="sitesearch+query"/>
	<input type="submit" name="__submit+sitesearch+search" onclick="submitButtonHandler(this)" value="Go" class="button"/>
</xsl:template>

<xsl:template match="parenttitle">
      <tr>
         <td colspan="3"><img src="/images/layout/spacer.gif" width="10" height="1"/></td>
      </tr>
      <tr>
         <td colspan="3"><h2><xsl:value-of select="."/></h2></td>
      </tr>
</xsl:template>

<xsl:template match="fieldset">
   <fieldset>
       <xsl:apply-templates />
   </fieldset>
</xsl:template>

<xsl:template match="legend">
    <legend><xsl:apply-templates /></legend>
</xsl:template>

<!-- Results ends -->

</xsl:stylesheet>
