<?xml version="1.0" ?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
	xmlns:metal="http://xml.zope.org/namespaces/metal"
	xmlns:xf="http://www.w3.org/2002/xforms"
	xmlns:tal="http://xml.zope.org/namespaces/tal" exclude-result-prefixes="xf">
    
	<xsl:include href="file://menu" />
	<xsl:include href="file://news" />
	<xsl:include href="file://contacts" />
	<xsl:include href="file://layout" />
	<xsl:include href="file://Presentation/Tofu/MailingListManager/xslt/email" />
	<xsl:include href="file://Presentation/Tofu/FileLibrary/xslt/files" />
	<xsl:include href="file://Presentation/Tofu/FileLibrary2/xslt/files" />
	<xsl:include href="file://Presentation/Tofu/SiteSearch/xslt/results" />
	<xsl:include href="file://Presentation/Tofu/XForms/xslt/xforms" />
	
	<xsl:output method="html" indent="yes" encoding="UTF8"
		omit-xml-declaration="yes"
		doctype-public="-//W3C//DTD HTML 4.01//EN"
		doctype-system="http://www.w3.org/TR/html4/strict.dtd" />
		
	<xsl:template match="root">	<html>
			<head>
				<title>
					<xsl:value-of select="//output/metadata/sitename" />
					<xsl:if test="//output/metadata/title">
						:
						<xsl:value-of select="//output/metadata/title" />
					</xsl:if>
				</title>
				<link rel="stylesheet" type="text/css"
					href="/Presentation/Tofu/Common/css/globalstyle.css" />
				<link rel="stylesheet" type="text/css" 
					media="print"
                                        href="/Presentation/Tofu/Common/css/print.css" />

				<script type="text/javascript"
					src="/Presentation/Tofu/XForms/js/xforms.js">
					&#160;
				</script>
				<script type="text/javascript"
					src="/Presentation/Tofu/XForms/js/calendar.js">
					&#160;
				</script>
				<script type="text/javascript" src="/Presentation/Tofu/Ajax/js/mochikit/MochiKit.js">
					&#160;
				</script>
				<script type="text/javascript" src="/Presentation/Tofu/Ajax/js/mochikit/dynamic_load.js">
					&#160;
				</script>
				<base href="{//output/metadata/base/@href}" />
			</head>
			<body onLoad="javascript:LoadStuff()">
				<form method="post" enctype="application/x-www-form-urlencoded" action=""
					onkeypress="javascript:return keypressEventHandler(this, event)">
					<xsl:call-template name="xf:model"/>
					<xsl:call-template name="body"/>
				</form>
			</body>

		</html>
	</xsl:template>
	
	<xsl:template name="body">
		<!-- Top Area Starts -->
		<div id="toparea">
			<!-- External Bar Starts -->
			<div id="externalbar">
				<xsl:call-template name="divisionswitcher"/>
					<xsl:apply-templates select="output/menus/menu[@id='external']"/>
			</div>
			<!-- External Bar Ends -->

			<!-- Title Bar Starts -->
			<div id="titlebar">
				<span class="group">
					<xsl:value-of select="output/metadata/sitename/text()" />
				</span>
				<xsl:if test="output/metadata/division/@name">
					<span class="division">
						<xsl:value-of select="output/metadata/division/@name"/>
					</span>
				</xsl:if>
			</div>
			<!-- Title Bar Ends -->


			<!-- Utilities Start -->
			<div id="utilities">
				<xsl:call-template name="loggedinlinks" />
				<xsl:call-template name="groups" />
			</div>
			<!-- Utilities End -->


			<!-- Navigation Bar Starts -->
			<xsl:apply-templates select="output/menus/menu[@id='main']" />
			<!-- Navigation Bar Ends -->

			<!-- Search Starts -->
			<xsl:if test="//user[@type='self']/id/text()!='Anonymous User'">
				<div id="searcharea">
					<xsl:call-template name="searcharea" />
				</div>
			</xsl:if>
			<!-- Search Ends -->

		</div>
		<!-- Top Area Starts -->

		<!-- Contextual Navigation Starts -->
		<xsl:apply-templates select="output/menus/menu[@id='side']" />
		<!-- Contextual Navigation Ends -->

		<!-- Main Content Area Starts -->
		<div id="content">

			<!-- Breadcrumbs Start -->
			<xsl:call-template name="breadcrumbs" />
			<!-- Breadcrumbs End -->

			<!-- Present any messages from the system -->
			<xsl:if test="//output/messages/message">
				<xsl:call-template name="result-messages" />
			</xsl:if>
			<!-- Messages End -->

			<!-- Body Content Starts -->
			<xsl:apply-templates select="output/content" />
			<!-- Body Content Ends -->

		</div>
		<!-- Main Content Area Ends -->
	
	</xsl:template>
    
</xsl:stylesheet>
