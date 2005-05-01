<?xml version="1.0"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">


	<!-- User Instructions Starts -->
	<xsl:template match="userinstructions">
		<div class="userinstructions">
			<xsl:apply-templates/>
		</div>
	</xsl:template>
 
	<!-- User Instructions Ends -->

	<!-- Contacts Starts -->
	<xsl:template match="users">
		<table class="contacts">
                        <xsl:for-each select="user">
                            <xsl:sort select="name/preferredname" order="ascending"/>
			    <xsl:call-template name="user"/>
                        </xsl:for-each>
		</table>
	</xsl:template>
	<xsl:template name="user">
		<tr>
			<td class="name">
				<xsl:apply-templates select="name"/>
			</td>
			<td class="userdetail">
				<a href="{link/@url}">Profile</a>
			</td>
			<td>
				<xsl:call-template name="userbioicon"/>
			</td>
			<td>
				<xsl:call-template name="userphotoicon"/>
			</td>
		</tr>
	</xsl:template>
	
	
	<xsl:template match="name">
		<a href="{../link/@url}">
			<xsl:value-of select="preferredname"/>&#160;<xsl:value-of select="lastname"/>
		</a><xsl:if test="../type/text()!=''"> (<xsl:value-of select="../type"/>)</xsl:if>
	</xsl:template>
	<xsl:template name="userbioicon">
		<xsl:choose>
			<xsl:when test="count(biography)=1">
				<img src="/images/other/icon-bio.gif" width="16" height="16" alt="Bio Available" title="Bio Available"/>
			</xsl:when>
			<xsl:when test="count(biography)!=1">
				<img src="/images/layout/spacer.gif" width="16" height="16"/>
			</xsl:when>
		</xsl:choose>
	</xsl:template>
	<xsl:template name="userphotoicon">
		<xsl:choose>
			<xsl:when test="count(image)=1">
				<img src="/images/other/photo.gif" width="20" height="13" alt="Photo Available" title="Photo Available"/>
			</xsl:when>
			<xsl:when test="count(image)!=1">
				<img src="/images/layout/spacer.gif" width="20" height="13"/>
			</xsl:when>
		</xsl:choose>
	</xsl:template>
	
	
	
	<!-- User Detail Page Starts -->
	<xsl:template match="userdetails">
		<xsl:apply-templates select="//root/output/user"/>
	</xsl:template>
	
	<xsl:template match="//root/output/user">
		<xsl:choose>
			<xsl:when test="@type='other'">
				<xsl:call-template name="userother"/>
			</xsl:when>
			<xsl:when test="@type='self'">
				<xsl:choose>
					<xsl:when test="count(//root/output/user[@type='other'])=0">
						<xsl:call-template name="userself"/>
					</xsl:when>
				</xsl:choose>
			</xsl:when>
		</xsl:choose>
	</xsl:template>
	
	
	<!-- Other User Detail Page Starts -->
	<xsl:template name="userother">
		<xsl:if test="count(image)=1">
			<div class="userimage">
				<img src="{image}" alt="Photo of {name/preferredname}"/>
			</div>
		</xsl:if>
		<table class="userother">
			<tr>
				<th valign="top">Name:</th>
				<td>
					<xsl:value-of select="name/preferredname"/>&#160;<xsl:value-of select="name/lastname"/> <xsl:if test="type">&#160;(<xsl:value-of select="type/text()"/>)</xsl:if>
				</td>
			</tr>
                        <xsl:if test="groupmemberships/groupmembership">
			<tr>
				<th valign="top">Group Memberships:</th>
				<td>
                                        <ul class="groups">
						<xsl:for-each select="groupmemberships/groupmembership">
							<li>
								<a href="{@url}">
									<xsl:value-of select="@title"/>
								</a>
							</li>
						</xsl:for-each>
					</ul>
				</td>
			</tr>
                        </xsl:if>
			<tr>
				<th valign="top">Email Addresses:</th>
				<td>
                                  <xsl:choose>
                                    <xsl:when test="//metadata/showEmailAddressTo/text() = 'request'">
                                       Request Contact (feature coming)
                                    </xsl:when>
                                    <xsl:when test="//metadata/showEmailAddressTo/text() != 'nobody'">
					<ul class="emails">
						<xsl:for-each select="emailaddresses/emailaddress">
							<li>
								<a href="mailto:{.}">
									<xsl:value-of select="."/>
								</a>
							</li>
						</xsl:for-each>
					</ul>
                                    </xsl:when>
                                    <xsl:otherwise>
                                        Email address has been hidden
                                    </xsl:otherwise>
                                  </xsl:choose>
				</td>
			</tr>
                        <xsl:for-each select="*[@present='auto']">
                        <tr>
				<th valign="top"><xsl:value-of select="@title"/>:</th>
				<td>
   		                    <xsl:choose>
			              <xsl:when test="text() != ''">
				        <xsl:apply-templates select="text()"/>
			              </xsl:when>
			              <xsl:otherwise>
                                         <!-- xsl:value-of select="name/preferredname"/> has not set a <xsl:value-of select="@title"/> yet.-->
					[not set]
			              </xsl:otherwise>
		                    </xsl:choose>
				</td>
			</tr>
                        </xsl:for-each>
		</table>

	</xsl:template>
	<!-- Other User Detail Page Ends -->
	
	
	<!-- Personal User Detail Page Starts -->
	<xsl:template name="userself">
		
		<div id="userself">

			<xsl:if test="count(//input[@id='changepassword'])=0 and count(//input[@id='set_biography'])=0">

<xsl:if test="count(image)=1">
			<div class="userimage">
				<img src="{image}" alt="Photo of {name/preferredname}"/>
				<xsl:choose>
					<xsl:when test="//input[@id='show_image']/object/element/@default='1'">
						<p>Your photo is visible to others</p>
					</xsl:when>
					<xsl:when test="//output/metadata/alwaysshowphoto/text()='1'">
						<p>Your photo is visible to others</p>
					</xsl:when>
					<xsl:otherwise>
						<p>Your photo is <strong>not</strong> visible to others</p>
					</xsl:otherwise>
				</xsl:choose>
			</div>
		</xsl:if>

			<fieldset>
				<legend>Your Profile as it Appears to Others</legend>

				<div class="row">
					<div class="label">Name:</div>
					<div class="field">
                                            <xsl:value-of select="name/preferredname"/>&#160;<xsl:value-of select="name/lastname"/> <xsl:if test="type">&#160;(<xsl:value-of select="type/text()"/>)</xsl:if>
					</div>
				</div>

                                <xsl:if test="groupmemberships/groupmembership">        
                                <div class="row">
				        <div class="label">Group Memberships:</div>
                                        <div class="field">
                                        <ul class="emails">
						<xsl:for-each select="groupmemberships/groupmembership">
							<li>
								<a href="{@url}">
									<xsl:value-of select="@title"/>
								</a>
							</li>
						</xsl:for-each>
					</ul>
                                        </div>
				</div>
	                        </xsl:if>
                             
			        <div class="row">
				    <div class="label">Email Addresses:</div>
				    <div class="field">

                                    <xsl:choose>
                                    <xsl:when test="//metadata/showEmailAddressTo/text() = 'request'">
                                       Request Contact (feature coming)
                                    </xsl:when>
                                    <xsl:when test="//metadata/showEmailAddressTo/text() != 'nobody'">
					<ul class="emails">
						<xsl:for-each select="emailaddresses/emailaddress">
							<li>
								<a href="mailto:{.}">
									<xsl:value-of select="."/>
								</a>
							</li>
						</xsl:for-each>
					</ul>
                                    </xsl:when>
                                    <xsl:otherwise>
                                        Email address has been hidden
                                    </xsl:otherwise>
                                  </xsl:choose>        

				    </div>
			        </div>   
                        <xsl:for-each select="*[@present='auto']">
                        <div class="row">
				<div class="label"><xsl:value-of select="@title"/>:</div>
				<div class="field">
   		                    <xsl:choose>
			              <xsl:when test="text() != ''">
				        <xsl:apply-templates select="text()"/>
			              </xsl:when>
			              <xsl:otherwise>
                                        [not set]
			              </xsl:otherwise>
		                    </xsl:choose>
				</div>
			</div>
                        </xsl:for-each>

			</fieldset>

			</xsl:if>
                                        
			<xsl:if test="//input[@id='changepassword']">
			<fieldset>
				<legend>Change Password</legend>
				
				<div class="row">
						<xsl:apply-templates select="//input[@id='changepassword']"/>
				</div>
			</fieldset>
                        </xsl:if>

			<xsl:apply-templates select="//input[@id='set_biography']"/>
			<xsl:apply-templates select="//input[@id='show_image']"/>
		</div>
		
	</xsl:template>
	<!-- Personal User Detail Page Ends -->	

	<xsl:template match="userprofile">
		<xsl:apply-templates select="//input[@id='change_profile']"/>
	</xsl:template>


	<xsl:template match="//input[@id='change_profile']">
		<form action="{@target}" method="post">
		
		<fieldset>
			<legend>Change Profile</legend>
			<xsl:for-each select="object">
                        <div class="row">
				<div class="label">
				        <xsl:value-of select="label"/>:<br/>
					<span class="note"><xsl:value-of select="description"/></span>
				</div>
				<div class="field">
                                        <xsl:choose>
                                            <xsl:when test="@type='string' and @displayhint='textarea'">
   					        <textarea rows="8" cols="40" name="{@id}">
						    <xsl:value-of select="element/text()"/>
					        </textarea>
                                            </xsl:when>
                                            <xsl:otherwise>
                                                <input type="text" size="40" name="{@id}" value="{element/text()}"/>
                                            </xsl:otherwise>
                                        </xsl:choose>
				</div>
			</div>
			</xsl:for-each>
                        
			<div class="buttonrow">
                                <input type="hidden" name="came_from" value="{//output[@id='main']/metadata/division/@url}/contacts/{//root/output/user[@type='self']/id/text()}/userprofile.xml"/>
				<input type="submit" value="Update Profile" name="submit" class="button"/>
			</div>

			</fieldset>
		</form>
	</xsl:template>
        
	<xsl:template match="//input[@id='set_biography']">
		<form action="{@target}" method="post">
		
		<fieldset>
			<legend>Biography Details</legend>
			<div class="row">
				<div class="label">
					Biography:<br/>
					<span class="note">Add/Edit your biography and click "Update Biography"</span>
				</div>
				<div class="field">
					<textarea rows="8" cols="40" name="{object[@id='biography']/@id}">
						<xsl:value-of select="object/element"/>
					</textarea>
				</div>
			</div>
			
			<div class="buttonrow">
                                <input type="hidden" name="came_from" value="{//output[@id='main']/metadata/division/@url}/contacts/{//root/output/user[@type='self']/id/text()}/userbio.xml"/>
				<input type="submit" value="Update Biography" name="submit" class="button"/>
			</div>

			</fieldset>
		</form>
	</xsl:template>
	
	<xsl:template match="biography">
		<xsl:apply-templates/>
	</xsl:template>
	
	<xsl:template match="//input[@id='show_image']">
		<form action="{@target}" method="post">
		
		<fieldset>
			<legend>Photo</legend>
			
			<div class="row">
				<div class="label">
					Show my photo to other participants:<br/>
					<span class="note">Check the box if you would like your photo to be visible to other participants then click "Update"</span>
				</div>
				<div class="field">
					<xsl:choose>
						<xsl:when test="object/element/@default='1'">
							<input type="checkbox" name="{object/@id}" checked="checked"/>
						</xsl:when>
						<xsl:otherwise>
							<input type="checkbox" name="{object/@id}"/>
						</xsl:otherwise>
					</xsl:choose>
				</div>
			</div>
			
			<div class="buttonrow">
				<input type="submit" value="Update" name="submit" class="button"/>
			</div>
			
		</fieldset>
	</form>
	</xsl:template>
	
	<xsl:template match="//input[@id='change_email']">
		<form action="{//input[@id='change_email']/@target}" method="post">
				<table class="changeemail">
					<tr>
						<th>&#160;</th>
						<th>Remove</th>
						<th>Send email to this Address</th>
					</tr>
					<xsl:apply-templates select="//user/emailaddresses/emailaddress" mode="changeemail"/>
				</table>
				
				<div class="buttonrow">
					<input type="submit" value="Update Email" name="update" class="button"/>
				</div>
				
		</form>
	</xsl:template>
	
	<xsl:template match="//user/emailaddresses/emailaddress" mode="changeemail">
			<tr>
				<td><xsl:value-of select="."/></td>
				<td><input type="checkbox" name="delete:list" value="{.}"/></td>
				<td><input type="checkbox" name="preferred:list" value="{.}">
						<xsl:if test="@preferred=1">
							<xsl:attribute name="checked">1</xsl:attribute>
						</xsl:if>
					</input></td>
			</tr>
	</xsl:template>
	
	<xsl:template match="//input[@id='add_email']">
	
		<table border="0" cellspacing="0" cellpadding="0">
			<tr>
				<form action="{//input[@id='add_email']/@target}" method="post">
					<td>
						<input type="text" size="25" name="{//input[@id='add_email']/object[@id='email']/@id}"/>
					</td>
					<td>
						<img src="/images/layout/spacer.gif" width="10" height="1"/>
					</td>
					<td>
						<input type="submit" name="{//input[@id='add_email']/@id}" value="Add" class="button"/>
					</td>
				</form>
			</tr>
		</table>
	</xsl:template>
	<xsl:template match="//input[@id='changepassword']|changepassword">
		<form action="{//input[@id='changepassword']/@target}" method="post">
		
			<div class="row">
				<div class="label">Please enter your new password:</div>
				<div class="field">
					<input type="password" size="25" name="{//input[@id='changepassword']/object[@id='password1']/@id}"/>
				</div>
			</div>
			
			<div class="row">
				<div class="label">Please repeat your new password:</div>
				<div class="field">
					<input type="password" size="25" name="{//input[@id='changepassword']/object[@id='password2']/@id}"/>
				</div>
			</div>
			
			<div class="buttonrow">
                                <input type="hidden" name="came_from" value="{//output[@id='main']/metadata/division/@url}/contacts/{//root/output/user[@type='self']/id/text()}/userpassword.xml"/>
				<input type="submit" name="submit" value="Save New Password" class="button"/>
			</div>
		</form>
	</xsl:template>
	<!-- Contacts Ends -->
</xsl:stylesheet>
