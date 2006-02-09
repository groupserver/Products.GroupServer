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
		<ul class="contacts">
			<xsl:for-each select="user">
				<xsl:sort select="name/preferredname" order="ascending"/>
				<xsl:call-template name="user"/>
			</xsl:for-each>
		</ul>
	</xsl:template>
	<xsl:template name="user">
		<li>
			<span class="name">
				<xsl:apply-templates select="name"/>
			</span>
		</li>
	</xsl:template>
	<xsl:template match="name">
		<a href="{../link/@url}">
			<xsl:value-of select="preferredname"/>
			<span>&#160;</span>
			<xsl:value-of select="lastname"/>
		</a>
		<xsl:if test="../type/text()!=''"> ( <xsl:value-of select="../type"/> ) </xsl:if>
	</xsl:template>

	<!-- Contacts Ends -->

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
					<xsl:value-of select="name/preferredname"/> &#160; <xsl:value-of
						select="name/lastname"/>
					<xsl:if test="type"> &#160;( <xsl:value-of select="type/text()"/> )
					</xsl:if>
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
						<xsl:when test="//metadata/showEmailAddressTo/text() = 'request'"> Request
							Contact (feature coming) </xsl:when>
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
						<xsl:otherwise> Email address has been hidden </xsl:otherwise>
					</xsl:choose>
				</td>
			</tr>
			<xsl:for-each select="*[@present='auto']">
				<tr>
					<th valign="top">
						<xsl:value-of select="@title"/> : </th>
					<td>
						<xsl:choose>
							<xsl:when test="text() != ''">
								<xsl:apply-templates select="text()"/>
							</xsl:when>
							<xsl:otherwise>
								<!-- xsl:value-of select="name/preferredname"/> has not set a <xsl:value-of select="@title"/> yet.-->
								[not set] </xsl:otherwise>
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
							<p> Your photo is <strong>not</strong> visible to others </p>
						</xsl:otherwise>
					</xsl:choose>
				</div>
			</xsl:if>
			<fieldset>
				<legend>Your Profile as it Appears to Others</legend>
				<div class="row">
					<div class="label">Name:</div>
					<div class="field">
						<xsl:value-of select="name/preferredname"/> &#160; <xsl:value-of
							select="name/lastname"/>
						<xsl:if test="type"> &#160;( <xsl:value-of select="type/text()"/> )
						</xsl:if>
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
								Request Contact (feature coming) </xsl:when>
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
							<xsl:otherwise> Email address has been hidden </xsl:otherwise>
						</xsl:choose>
					</div>
				</div>
				<xsl:for-each select="*[@present='auto']">
					<div class="row">
						<div class="label">
							<xsl:value-of select="@title"/> : </div>
						<div class="field">
							<xsl:choose>
								<xsl:when test="text() != ''">
									<xsl:apply-templates select="text()"/>
								</xsl:when>
								<xsl:otherwise>[not set]</xsl:otherwise>
							</xsl:choose>
						</div>
					</div>
				</xsl:for-each>
			</fieldset>
		</div>
	</xsl:template>
	<!-- Personal User Detail Page Ends -->
</xsl:stylesheet>
