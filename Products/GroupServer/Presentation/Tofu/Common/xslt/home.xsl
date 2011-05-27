<xsl:stylesheet version="1.0"  xmlns:metal="http://xml.zope.org/namespaces/metal" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:tal="http://xml.zope.org/namespaces/tal">

<xsl:include href="menu.xsl"/>
<xsl:include href="layout.xsl"/>

<xsl:output method="xml" indent="yes" encoding="ISO-8859-1" omit-xml-declaration="yes" doctype-public="-//W3C//DTD HTML 4.01 Transitional//EN" doctype-system="http://www.w3.org/TR/html4/loose.dtd" />

<xsl:template match="root">
<html>
<head>
	<title>ABEL eCampus</title>
	<meta http-equiv="Content-Type" content="text/html" />
	<link rel="stylesheet"
		href="/++resource++globalstyle-20110406.css" />
        <link rel="stylesheet" media="print"
		href="/Presentation/Tofu/Common/css/print.css" />
        <base href="{//output/metadata/base/@href}" />
</head>

<body bgcolor="#ffffff" leftmargin="0" topmargin="0" marginwidth="0" marginheight="0">
<table width="100%" border="0" cellspacing="0" cellpadding="0" bgcolor="#CCCCCC" class="externalbar">
  <tr>
    <td> 
      <table width="100%" border="0" cellpadding="0" cellspacing="0">
        <tr>
		<form name="{input[@id='switch_division']/@id}" method="post" action="{input[@id='switch_division']/@target}">
	          	<td>
				<xsl:call-template name="divisionswitcher"/>
			</td>
		</form>
          <td><img src="/images/layout/spacer.gif" width="35" height="1"/></td>
          <td align="right">

<!-- Utility Menu Starts -->
<xsl:apply-templates select="output/menus/menu[@id='external']"/>
<!-- Utility Menu Ends -->

          </td>
        </tr>
      </table></td>
  </tr>
</table>
<table width="100%" border="0" cellpadding="0" cellspacing="0" bgcolor="#999999" class="topbar">
  <tr>
    <td><table width="100%" border="0" cellspacing="0" cellpadding="0">
        <tr>
          <td width="100%">
<table border="0" cellspacing="0" cellpadding="0">
              <tr> 
                <td><img src="/images/layout/logo-abel.gif" width="175" height="37"/></td>
                <td><xsl:call-template name="logo"/></td>
              </tr>
            </table>
          </td>
          <td width="20"><img src="/images/layout/spacer.gif" width="20" height="1"/></td>
          	<td width="84">
			<xsl:call-template name="groups"/>
		</td>
		<td width="20"><img src="/images/layout/spacer.gif" width="20" height="1"/></td>
          
		<td width="150">
			<xsl:call-template name="loginname"/>
          </td>

          <td width="20"><img src="/images/layout/spacer.gif" width="20" height="1"/></td>

          	<td width="70" align="right"> 
			<xsl:call-template name="loggedinlinks"/>
		</td>
	          <td width="15"><img src="/images/layout/spacer.gif" width="15" height="1"/></td>
	        </tr>
	      </table>
<!-- Groups and Login Details Ends -->
      
    </td>
  </tr>
</table>
<table width="100%" border="0" cellpadding="0" cellspacing="0" bgcolor="#CCCCCC" class="topbar2">
  <tr>
    <td>

<!-- Main Navigation Starts -->
<xsl:apply-templates select="output/menus/menu[@id='main']"/>
<!-- Main Navigation Ends -->	

</td>
  </tr>
</table>
<table width="100%" border="0" cellpadding="0" cellspacing="0">
  <tr>
    <td width="7"><img src="/images/layout/spacer.gif" width="7" height="1"/></td>
    <td width="120"><img src="/images/layout/spacer.gif" width="120" height="15"/></td>
    <td width="15"><img src="/images/layout/spacer.gif" width="15" height="1"/></td>
    <td width="100%"><img src="/images/layout/spacer.gif" width="1" height="1"/></td>
    <td width="15"><img src="/images/layout/spacer.gif" width="15" height="1"/></td>
  </tr>
  <tr>
    <td width="7" valign="top">&#160;</td>
    <td width="120" valign="top">


<!-- About Navigation Starts -->
<xsl:apply-templates select="output/menus/menu[@id='about']"/>
<!-- About Navigation Ends -->

     </td>
    <td width="15" valign="top">&#160;</td>
    <td width="100%" valign="top">

<!-- Body Content Starts -->
<xsl:apply-templates select="output/content" />
<!-- Body Content Ends -->

</td>
    <td width="15">&#160;</td>
  </tr>
  <tr>
    <td width="7"><img src="/images/layout/spacer.gif" width="1"/></td>
    <td width="120"><img src="/images/layout/spacer.gif" width="1" height="25"/></td>
    <td width="15"><img src="/images/layout/spacer.gif" width="1"/></td>
    <td width="100%"><img src="/images/layout/spacer.gif" width="1"/></td>
    <td width="15"><img src="/images/layout/spacer.gif" width="1"/></td>
  </tr>
</table>
</body>
</html>
</xsl:template>

<xsl:template match="output/content">
	<xsl:apply-templates/>
</xsl:template>

</xsl:stylesheet>
