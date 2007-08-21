<?xml version="1.0" ?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:metal="http://xml.zope.org/namespaces/metal"
  xmlns:tal="http://xml.zope.org/namespaces/tal">

  <xsl:include href="file://menu" />
  <xsl:include href="file://layout" />
  <xsl:include href="file://contacts" /> 
  <xsl:include href="file://news" />

  <xsl:include href="file://Presentation/Tofu/FileLibrary/xslt/files"/>
  <xsl:include href="file://Presentation/Tofu/SiteSearch/xslt/results"/>

  <xsl:output method="html" indent="yes" encoding="UTF8"
    omit-xml-declaration="yes"
    doctype-public="-//W3C//DTD HTML 4.01//EN"
    doctype-system="http://www.w3.org/TR/html4/strict.dtd" />

  <xsl:template match="root">
    <html>
      <head>
        <meta http-equiv="Content-Type" content="text/xhtml; charset=UTF8" />
        <title>
          <xsl:value-of select="//output/metadata/division/@name" />
          <xsl:if test="//output/metadata/title">:
          <xsl:value-of select="//output/metadata/title" />
        </xsl:if>
      </title>

      <link rel="stylesheet" type="text/css"
        href="/++resource++globalstyle-20070821.css" />
      <link 
        rel="stylesheet" type="text/css" 
        href="/PresentationCustom/Tofu/Common/css/globalstyle.css" />
      
      <xsl:if test="//link[@class='alternateRDF']">
        <xsl:for-each select="//link[@class='alternateRDF']">
          <link rel="alternate" type="application/rss+xml"
            href="{@url}">
            <xsl:attribute name="title">
              <xsl:value-of select="text()"/>
            </xsl:attribute>
          </link>
        </xsl:for-each>
      </xsl:if>
      
      <xsl:if test="//link[@class='alternateATOM']">
        <xsl:for-each select="//link[@class='alternateATOM']">
          <link rel="alternate" type="application/atom+xml"
            href="{@url}">
            <xsl:attribute name="title">
              <xsl:value-of select="text()"/>
            </xsl:attribute>
          </link>
        </xsl:for-each>
      </xsl:if>

      <base href="{//output/metadata/base/@href}" />

    </head>
    <body>
      <!-- Top Area Starts -->
      <div id="toparea">
        <!-- External Bar Starts -->
        <div id="externalbar">
          <xsl:call-template name="divisionswitcher" />
          <xsl:apply-templates
            select="output/menus/menu[@id='external']" />
        </div><!-- External Bar Ends -->

        <!-- Title Bar Starts -->
        <div id="titlebar">
          <span class="logo"/>
          <span class="group">
            <xsl:value-of select="output/metadata/sitename/text()" />
          </span>

          <xsl:if test="output/metadata/division/@name">
            <span class="division">
              <xsl:value-of select="output/metadata/division/@name" />
            </span>
          </xsl:if>

          <xsl:if test="output/metadata/bannerimage/@url">
            <span class="bannerimage">
              <a href="{output/metadata/bannerimage/@link}">
                <img src="{output/metadata/bannerimage/@url}"
                  alt="banner image" />
              </a>
            </span>
          </xsl:if>
        </div><!-- Title Bar Ends -->

        <!-- Utilities Start -->
        <div id="utilities">
          <xsl:call-template name="loggedinlinks" />
          <xsl:call-template name="groups" />
        </div><!-- Utilities End -->

        <!-- Navigation Bar Starts -->
        <xsl:apply-templates select="output/menus/menu[@id='main']" />
        <!-- Navigation Bar Ends -->
      </div><!-- Top Area Ends-->

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

      </div><!-- Main Content Area Ends -->

      <xsl:apply-templates select="output/menus/menu[@id='footerlinks']"/>

    </body>
  </html>
</xsl:template>

</xsl:stylesheet>
