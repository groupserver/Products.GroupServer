<?xml version="1.0" ?>
<xsl:stylesheet version="1.0" 
	xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
	xmlns:metal="http://xml.zope.org/namespaces/metal"
	xmlns:tal="http://xml.zope.org/namespaces/tal"
	xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
	xmlns:a="http://purl.org/rss/1.0/modules/syndication/"
	xmlns:admin="http://webns.net/mvcb/"
	xmlns:dc="http://purl.org/dc/elements/1.1/"
	xmlns:slash="http://purl.org/rss/1.0/modules/slash/"
	xmlns:xml="http://www.w3.org/XML/1998/namespace"
	xmlns:rss="http://purl.org/rss/1.0"
        exclude-result-prefixes="rdf a admin dc slash xml rss">

<xsl:template match="rss_feed">
	<xsl:apply-templates select="//rdf:RDF/rss:channel" mode="rssnews"/>
</xsl:template>

<xsl:template match="//rdf:RDF/rss:channel" mode="rssnews">
<h2><xsl:value-of select="rss:title"/></h2>
<img src="{rss:image/@rdf:about}" alt="" />
    <xsl:for-each select="rss:items/rdf:Seq/rdf:li">
      <xsl:variable name="resource" select="@rdf:resource"/>
      <xsl:apply-templates select="ancestor::rdf:RDF/rss:item[@rdf:about=$resource]" mode="rssnews"/>
    </xsl:for-each>
</xsl:template>

<xsl:template match="rss:item" mode="rssnews">
        <h3><xsl:value-of select="rss:title"/></h3>
	<h4><xsl:value-of select="dc:date/text()"/></h4>
	<xsl:apply-templates select="rss:description/text()"/>
        <p><a href="{rss:link/text()}">Full Story</a></p>
</xsl:template> 


<!-- Old Style -->

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
        <!--Dan hid Author <p><strong><xsl:value-of select="author"/></strong></p> -->
</xsl:template>

<!-- News Feeds Ends -->


</xsl:stylesheet>
