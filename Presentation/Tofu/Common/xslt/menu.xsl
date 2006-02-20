<?xml version="1.0" ?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<!-- Main Navigation Starts -->

<xsl:template match="output/menus/menu[@id='main']">

	<div id="sitenavigation">

		<ul>

			<xsl:for-each select="menuitem">
				<xsl:choose>
  					<xsl:when test="@current='1'">
  					 <li class="current"><a  id="{@name}-menu-link" class="current" href="{@url}"><xsl:value-of select="@name"/></a></li></xsl:when>
  					<xsl:otherwise>
  					 <li><a  id="{@name}-menu-link" href="{@url}"><xsl:value-of select="@name"/></a></li></xsl:otherwise>
				</xsl:choose>
			</xsl:for-each>						
		</ul>
	</div>

</xsl:template>

<!-- Main Navigation Ends -->


<!-- Sub Navigation Starts -->

<xsl:template match="output/menus/menu[@id='side']">
  <xsl:variable name="mainmenu"
       select="//menu[@id='main']"/>

<div id="contextnav">
        <p class="label">
	  <xsl:value-of select ="$mainmenu/menuitem[@current='1']/@name"/>
	</p>
	<dl>
		<xsl:for-each select="menuitem">
			<xsl:choose>
				<xsl:when test="@current='1'">
			 		<dd><a class="current" href="{@url}"><xsl:value-of select="@name"/></a>
						<xsl:choose>
							<xsl:when test="count(menuitem)!=0">
								<dl>
									<xsl:for-each select="menuitem">
										<xsl:call-template name="thirdmenuitem"/>
									</xsl:for-each>
								</dl>
							</xsl:when>
						</xsl:choose>
					</dd>
				</xsl:when>
				<xsl:otherwise>
					<xsl:choose>
						<xsl:when test="count(menuitem)!=0">
							<dd class="current"><a href="{@url}"><xsl:value-of select="@name"/></a></dd>
						</xsl:when>
						<xsl:otherwise>
							<dd><a href="{@url}"><xsl:value-of select="@name"/></a></dd>
						</xsl:otherwise>
					</xsl:choose>
				</xsl:otherwise>
			</xsl:choose>
		</xsl:for-each>
	</dl>
</div>
</xsl:template>


<xsl:template name="thirdmenuitem">
	<xsl:choose>
		<xsl:when test="@current='1'">
			 <dd><a class="current" href="{@url}"><xsl:value-of select="@name"/></a></dd>
		</xsl:when>
		<xsl:otherwise>
			 <dd><a href="{@url}"><xsl:value-of select="@name"/></a></dd>
		</xsl:otherwise>
	</xsl:choose>
</xsl:template>


<!-- Sub Navigation Ends -->


<!-- External Menu Starts -->

<xsl:template match="output/menus/menu[@id='external']">
	<div id="externallinks">
		<ul>
			<xsl:for-each select="menuitem">
    				<li><a href="{@url}"><xsl:value-of select="@name"/></a></li>
			</xsl:for-each>			
		</ul>
	</div>
</xsl:template>

<!-- External Menu Ends -->

<!-- Bread Crumbs Starts -->

<xsl:template name="breadcrumbs">
        <div class="breadcrumb">
            <xsl:apply-templates select="output/context"/> <xsl:value-of select="//output/metadata/title/text()"/>
	</div>
</xsl:template>

<xsl:variable name="separatoricon">
  &gt;
</xsl:variable>

<xsl:template match="output/context">
  <xsl:call-template name="breadcrumb">
        <xsl:with-param name="context" select="./contextitem" />
        <xsl:with-param name="separator" select="$separatoricon" />
  </xsl:call-template>
</xsl:template>

<xsl:template name="breadcrumb">
  <xsl:param name="context"/>
  <xsl:param name="separator"/>
  
  <xsl:if test="$context">

  <xsl:choose>

<!-- Current Context Menu Reached -->

    <xsl:when test="$context/@current='1'">
      <xsl:value-of select="$context/@name"/>
    </xsl:when>
    
<!-- Keep going down the chain adding the next context item -->

    <xsl:otherwise>
      <a href="{$context/@url}"><xsl:value-of select="$context/@name"/></a>
      <xsl:value-of select="$separator"/>
      <xsl:call-template name="breadcrumb">
        <xsl:with-param name="context" select="$context/contextitem" />
        <xsl:with-param name="separator" select="$separator" />
      </xsl:call-template>
    </xsl:otherwise>
  </xsl:choose>
  </xsl:if>
</xsl:template>
<!-- Bread Crumbs Ends -->

<!-- Division Switcher Starts -->
<xsl:template name="divisionswitcher">

	<xsl:if test="count(input[@id='switch_division'])!=0">
		<xsl:call-template name="switch"/>
	</xsl:if>
</xsl:template>

<xsl:template name="switch">
<form name="{input[@id='switch_division']/@id}" method="post" action="{input[@id='switch_division']/@target}">
	<div id="division">
		<label><xsl:value-of select="input[@id='switch_division']/object/label/text()"/></label>
		<select name="{input[@id='switch_division']/object/@id}" onchange="javascript:switch_division.submit()">
			<xsl:for-each select="input[@id='switch_division']/object/element">
				<option value="{@value}">
                                        <xsl:if test="@current='1'"><xsl:attribute name="selected">selected</xsl:attribute></xsl:if>
					<xsl:value-of select="@description"/>
				</option>
			</xsl:for-each>	
		</select>

		<!-- input type="submit" name="send" value="Go"/ -->
	</div>
</form>

</xsl:template>
<!-- Division Switcher Ends -->

<!-- Group Icons Start -->
<xsl:template name="groups">
	<xsl:if test="count(output/menus/menu[@id='groups'])!=0">
		<xsl:call-template name="groupicons"/>
	</xsl:if>
</xsl:template>

<xsl:template name="groupicons">
	<div id="groups">
		<xsl:apply-templates select="output/menus/menu[@id='groups']/menuitem"/>
	</div>
</xsl:template>

<xsl:template match="output/menus/menu[@id='groups']/menuitem">
	<a href="{@url}" title="{@name}"><img src="{image/@url}" width="37" height="33" border="0"/></a>
</xsl:template>
<!-- Group Icons End -->

<!-- Logged in links Starts -->
<xsl:template name="loggedinlinks">
	<div id="utilitylinks">
		<ul>
		      <xsl:choose>
				<xsl:when test="output/user[@type='self']/id='Anonymous User'">
					<li><a id="log-in-link" href="/login" title="Log in here">Log In</a></li>
				</xsl:when>
				<xsl:otherwise>
					<li><a id="log-out-link" href="/cookie_authentication/logout">Log Out</a></li>
				        <li><a id="profile-link" href="{output/user[@type='self']/@url}" title="Profile for {output/user[@type='self']/name/preferredname} {output/user[@type='self']/name/lastname}"><xsl:value-of select="output/user[@type='self']/name/preferredname"/>&#160;<xsl:value-of select="output/user[@type='self']/name/lastname"/> (profile)</a></li>
				</xsl:otherwise>
			</xsl:choose>
		</ul>
	</div>
</xsl:template>
<!-- Logged in links Ends -->

</xsl:stylesheet>
