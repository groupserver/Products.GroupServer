<xsl:stylesheet version="1.0"  xmlns:metal="http://xml.zope.org/namespaces/metal" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:tal="http://xml.zope.org/namespaces/tal">

<xsl:output method="html" indent="yes" encoding="UTF-8" omit-xml-declaration="yes" />

<!-- Main Navigation Starts -->

<xsl:template match="menu[@id='main']">
    <ul>
      <xsl:for-each select="menuitem">
	<xsl:choose>
	 <xsl:when test="@current='1'">
	  <li>
	    <a class="current"
	      href="{@url}"
	      id="{translate(@name, ' .', '--')}-menu-link">
          <xsl:value-of select="@name"/>
      </a>
	  </li>
	</xsl:when>
	<xsl:otherwise>
	  <li>
	    <a id="{translate(@name, ' .', '--')}-menu-link"
	      href="{@url}"><xsl:value-of select="@name"/></a>
	  </li>
	</xsl:otherwise>
      </xsl:choose>
    </xsl:for-each>						
  </ul>
</xsl:template>

<!-- Main Navigation Ends -->


<!-- Side Menu -->

<xsl:template match="/menu[@id='side']">
  <dl>
    <xsl:for-each select="menuitem">
      <xsl:choose>
	<xsl:when test="@current='1'">
	  <dd>
	    <a href="{@url}"
	      class="current"><xsl:value-of select="@name"/></a>
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
		<dd>
		  <a href="{@url}"
		    class="current"><xsl:value-of select="@name"/></a>
		</dd>
	      </xsl:when>
	      <xsl:otherwise>
		<dd>
		  <a href="{@url}">
		    <xsl:value-of select="@name"/></a>
		</dd>
	      </xsl:otherwise>
	    </xsl:choose>
	  </xsl:otherwise>
	</xsl:choose>
      </xsl:for-each>
    </dl>
</xsl:template>

<xsl:template name="thirdmenuitem">
  <xsl:choose>
    <xsl:when test="@current='1'">
      <dd>
	<a class="current" href="{@url}"><xsl:value-of select="@name"/></a>
      </dd>
    </xsl:when>
    <xsl:otherwise>
      <dd>
	<a href="{@url}"><xsl:value-of select="@name"/></a>
      </dd>
    </xsl:otherwise>
  </xsl:choose>
</xsl:template>

<!-- End of Side Menu -->

<!-- External Menu -->

<xsl:template match="/menu[@id='external']">
	<div id="externallinks">
		<ul>
			<xsl:for-each select="menuitem">
    				<li><a href="{@url}"><xsl:value-of select="@name"/></a></li>
			</xsl:for-each>			
		</ul>
	</div>
</xsl:template>

<!-- End of External Menu -->

<!-- Bread Crumbs Starts -->

<xsl:template match="context/">
  <xsl:call-template name="breadcrumb">
        <xsl:with-param name="context" select="./contextitem" />
        <xsl:with-param name="separator" select="$separatoricon" />
  </xsl:call-template>
</xsl:template>

<xsl:template name="breadcrumbs">
        <div class="breadcrumb">
            <xsl:apply-templates select="output/context"/> <xsl:value-of select="//output/metadata/title/text()"/>
	</div>
</xsl:template>

<xsl:variable name="separatoricon">
  &gt;
</xsl:variable>

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


</xsl:stylesheet>
