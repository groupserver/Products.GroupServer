<?xml version="1.0" ?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:metal="http://xml.zope.org/namespaces/metal"
                              xmlns:xf="http://www.w3.org/2002/xforms" xmlns:tal="http://xml.zope.org/namespaces/tal"
                              exclude-result-prefixes="xf">

<xsl:include href="file://menu"/>
<xsl:include href="file://layout"/>
<xsl:include href="file://contacts"/>
<xsl:include href="file://useremail"/>
<xsl:include href="file://news"/>

<xsl:include href="file://Presentation/Tofu/MailingListManager/xslt/email"/>
<xsl:include href="file://Presentation/Tofu/FileLibrary/xslt/files"/> 
<xsl:include href="file://Presentation/Tofu/Common/xslt/forms"/>
<xsl:include href="file://Presentation/Tofu/SiteSearch/xslt/results"/>
<xsl:include href="file://Presentation/Tofu/XForms/xslt/xforms"/>

<xsl:output method="html" indent="yes" encoding="UTF-8" omit-xml-declaration="yes"
            doctype-public="-//W3C//DTD HTML 4.01 Transitional//EN" doctype-system="http://www.w3.org/TR/html4/loose.dtd" />

<xsl:template match="root">
<html>
<head>
	<title>
		<xsl:value-of select="//output/metadata/sitename"/>
		<xsl:if test="//output/metadata/title">: <xsl:value-of select="//output/metadata/title"/></xsl:if>
	</title>
	<link rel="stylesheet" href="/Presentation/Tofu/Common/css/globalstyle.css" />
        <script type="text/javascript" src="/Presentation/Tofu/XForms/js/xforms.js">&#160;</script>
        <script type="text/javascript" src="/Presentation/Tofu/XForms/js/calendar.js">&#160;</script>
        <base href="{//output/metadata/base/@href}" />
</head>

<body>
       		<xsl:choose>
          		<xsl:when test=".//xf:*">
            			<form method="post" enctype="application/x-www-form-urlencoded" action="" onkeypress="javascript:return keypressEventHandler(this, event)">
              				<xsl:call-template name="xf:model"/>
              				<xsl:call-template name="body"/>
           			</form>
          		</xsl:when>
          	<xsl:otherwise>
            		<xsl:call-template name="body"/>
          	</xsl:otherwise>
        	</xsl:choose>

</body>

</html>
</xsl:template>

<xsl:template name="body">
<!-- Top Area Starts -->
<div id="toparea">
	<!-- External Bar Starts -->
	<div id="externalbar">
		<!-- <xsl:call-template name="divisionswitcher"/>
		<xsl:apply-templates select="output/menus/menu[@id='external']"/> -->
	</div>
	<!-- External Bar Ends -->
	
	<!-- Title Bar Starts -->
	<div id="titlebar">
		<span class="group"><xsl:value-of select="output/metadata/sitename/text()"/></span>
		<span class="division"><xsl:value-of select="output/metadata/division/@name"/></span>
	</div>
	<!-- Title Bar Ends -->


	<!-- Utilities Start -->
	<div id="utilities">
		<xsl:call-template name="loggedinlinks"/>
		<xsl:call-template name="loginname"/>
		<xsl:call-template name="groups"/>
	</div>
	<!-- Utilities End -->


	<!-- Navigation Bar Starts -->
	<xsl:apply-templates select="output/menus/menu[@id='main']"/>
	<!-- Navigation Bar Ends -->
	
	<!-- Search Starts -->
        <!-- <xsl:if test="//user[@type='self']/id/text()!='Anonymous User'">
	<div id="searcharea">
		<xsl:call-template name="searcharea"/>
	</div>
        </xsl:if> -->
	<!-- Search Ends -->
	
	
</div>
<!-- Top Area Starts -->


<!-- Contextual Navigation Starts -->
<xsl:apply-templates select="output/menus/menu[@id='side']"/>
<!-- Contextual Navigation Ends -->


<!-- Main Content Area Starts -->
<div id="content">

	<!-- Breadcrumbs Start -->
		<xsl:call-template name="breadcrumbs"/>
	<!-- Breadcrumbs End -->
	
	<!-- Body Content Starts -->
	<xsl:apply-templates select="output/content" />
	<!-- Body Content Ends -->

</div>
<!-- Main Content Area Ends -->

</xsl:template>

<xsl:template match="output/content">
        <xsl:if test="//output/messages"><xsl:call-template name="result-messages"/></xsl:if>
	<xsl:apply-templates/>
</xsl:template>

</xsl:stylesheet>
