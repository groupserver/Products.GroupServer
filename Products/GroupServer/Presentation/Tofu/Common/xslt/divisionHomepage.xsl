<?xml version="1.0" encoding="utf-8" ?>

<!--
  -   Division Homepage XSL Stylesheet
  -
  -   The main difference between this stylesheet and the "adminsection"
  - "divisionHomeContent" ID instead of a "content" ID.
  -
  -   Michael JasonSmith, 2006-03-02
  -->

<xsl:stylesheet version="1.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:metal="http://xml.zope.org/namespaces/metal"
  xmlns:xf="http://www.w3.org/2002/xforms"
  xmlns:tal="http://xml.zope.org/namespaces/tal"
  exclude-result-prefixes="xf">
    
  <xsl:include href="file://Presentation/Tofu/Common/xslt/menu" />
  <xsl:include href="file://Presentation/Tofu/Common/xslt/news" />
  <xsl:include href="file://Presentation/Tofu/Common/xslt/contacts" />
  <xsl:include href="file://Presentation/Tofu/Common/xslt/layout" />
  <xsl:include href="file://Presentation/Tofu/SiteSearch/xslt/results" />
  <xsl:include href="file://Presentation/Tofu/XForms/xslt/xforms" />
  
  <xsl:output method="xml" indent="yes" encoding="UTF8"
    omit-xml-declaration="yes"
    doctype-public="-//W3C//DTD HTML 4.01//EN"
    doctype-system="http://www.w3.org/TR/html4/strict.dtd" />
    
  <xsl:template match="root">
<html>
  <head>
    <title>
      <xsl:value-of select="//output/metadata/division/@name" />
      <xsl:if test="//output/metadata/title">:
      <xsl:value-of select="//output/metadata/title" />
      </xsl:if>
    </title>
    <link rel="stylesheet" type="text/css"
      href="/++resource++globalstyle-20110308.css" />
    <link rel="stylesheet" type="text/css" 
      href="/++resource++site-20110308.css" />

    <script type="text/javascript"
      src="/Presentation/Tofu/XForms/js/xforms.js">
      &#160;
    </script>

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
    <form method="post"
      enctype="application/x-www-form-urlencoded"
      action=""
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
        <xsl:call-template name="divisionswitch"/>
  <xsl:apply-templates select="output/menus/menu[@id='external']"/> 
      </div><!-- External Bar Ends -->
      
      <!-- Title Bar Starts -->
      <div id="titlebar">
          <span class="logo"/>
  <span class="group">
    <xsl:value-of select="output/metadata/sitename/text()" />
  </span>
  <xsl:if test="output/metadata/division/@name">
    <span class="division">
      <xsl:value-of select="output/metadata/division/@name"/>
    </span>
  </xsl:if>
      </div><!-- Title Bar Ends -->

      <!-- Utilities Start -->
      <div id="utilities">
  <xsl:call-template name="loggedinlinks" />
  <xsl:call-template name="groups" />
      </div><!-- Utilities End -->

      <!-- Site Navigation Bar Starts -->
      <xsl:apply-templates select="output/menus/menu[@id='main']" />
      <!-- Site Navigation Bar Ends -->
    </div><!--toparea-->
    
    <!-- Main Content Area Starts -->
    <div id="divisionHomeContent">
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

      <xsl:apply-templates select="output/menus/menu[@id='footerlinks']"/>

    </div><!--divisionHomeContent-->
  </xsl:template>
</xsl:stylesheet>
