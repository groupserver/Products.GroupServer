<?xml version="1.0" encoding="ISO-8859-1"?>
<xsl:stylesheet version="1.0"
               xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
               xmlns:search="http://purl.org/rss/1.0/modules/search/"
               xmlns:results="http://xwft.org/ns/rss/modules/results/0.9"
               xmlns:rss="http://purl.org/rss/1.0/"
               xmlns:email="http://xwft.net/namespaces/email/0.9/"
               xmlns:files="http://xwft.net/namespaces/files/0.9/"
               xmlns:groups="http://xwft.net/namespaces/groups/0.9/"
               xmlns:dc="http://purl.org/dc/elements/1.1/"
               xmlns:file="http://xwft.org/ns/filelibrary/0.9/" 
               xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:output method="html" encoding="ISO-8859-1"/>

    <xsl:template match="rdf:RDF">
      <xsl:apply-Templates select="rss:channel"/>
    </xsl:template>
    
    <xsl:template match="rss:channel">
      <xsl:choose>
        <xsl:when test="@id='emailresults'">
          <xsl:call-template name="email-results"/>
        </xsl:when>        
        <xsl:when test="@id='fileresults'">
          <xsl:call-template name="file-results"/>
        </xsl:when>        
      </xsl:choose>
    </xsl:template>
    
    <xsl:template name="email-results">

	<h2>Search Results found in Messages</h2>
	
	<xsl:choose>
        	<xsl:when test="count(rss:items/rdf:Seq/rdf:li)=0">
			<p>No matching messages found.</p>
       	 </xsl:when>
       	 <xsl:otherwise>
			<p>
				Messages <xsl:value-of select="number(results:first/text())+1"/> to <xsl:value-of select="number(results:last/text())"/> of the <xsl:value-of select="number(results:total/text())"/> messages containing your search text:
			</p>
        
			<table id="results">
				<tr>
					<th>Date</th>
					<th>Subject</th>
					<th>From</th>
					<th>Group</th>
				</tr>
				
				<xsl:for-each select="rss:items/rdf:Seq/rdf:li">
			            <xsl:variable name="resource" select="@rdf:resource"/>
			            <xsl:variable name="item" select="ancestor::rdf:RDF/rss:item[@rdf:about=$resource]"/>
			            <tr>
			               <xsl:if test="position() mod 2 != 0">
			               	<xsl:attribute name="class">alternate</xsl:attribute>
			               </xsl:if>
			              <td><xsl:value-of select="$item/dc:date/text()"/></td>
			              <td><a href="{/root/output/metadata/division/@url}/groups/{$item/email:listId/text()}/messages/view_email?id={$item/email:id/text()}"><xsl:value-of select="$item/rss:title/text()"/></a></td>
			              <td><xsl:choose>
                                              <xsl:when test="$item/email:mailUserId/text() and $item/email:mailFromName/text()">
                                                   <a href="{/root/output/metadata/division/@url}/contacts/{$item/email:mailUserId/text()}"><xsl:value-of select="$item/email:mailFromName/text()"/></a>
                                              </xsl:when>
                                              <xsl:otherwise>
                                                   <xsl:value-of select="$item/email:from/text()"/>
                                              </xsl:otherwise>
                                          </xsl:choose></td>
			              <td><a href="{/root/output/metadata/division/@url}/groups/{$item/email:listId/text()}"><xsl:value-of select="$item/email:listId/text()"/></a></td>
			            </tr>
			        </xsl:for-each>
			</table>
			
			<div class="resultsnav">
				<xsl:if test="results:prevlink">
					<a href="{results:prevlink/text()}">previous</a>
				</xsl:if>
				<xsl:if test="results:nextlink">
					<a href="{results:nextlink/text()}">next</a>
				</xsl:if>
			</div>
        </xsl:otherwise>
        </xsl:choose>
    </xsl:template>


    <xsl:template name="file-results">

	<h2>Search Results found in Files</h2>
	
	<xsl:choose>
	
        	<xsl:when test="count(rss:items/rdf:Seq/rdf:li)=0">
			<p>No matching files found.</p>
       	 </xsl:when>

       	 <xsl:otherwise>
			<p>
				Files <xsl:value-of select="number(results:first/text())+1"/> to <xsl:value-of select="number(results:last/text())"/> of the <xsl:value-of select="number(results:total/text())"/> files containing your search text (in the Title or Description):
			</p>
        
			<table id="results">
				<tr>
					<th>Date</th>
					<th>Title</th>
					<th>Description</th>
					<th>Creator</th>
					<th>Group</th>
				</tr>
				
				<xsl:for-each select="rss:items/rdf:Seq/rdf:li">
					<xsl:variable name="resource" select="@rdf:resource"/>
					<xsl:variable name="item" select="ancestor::rdf:RDF/rss:item[@rdf:about=$resource]"/>
						<tr>
			               		<xsl:if test="position() mod 2 != 0">
			               			<xsl:attribute name="class">alternate</xsl:attribute>
			              		 </xsl:if>
               			              		<td>
								<xsl:value-of select="$item/dc:date/text()"/>
							</td>
					              <td>
								<a href="/{$item/groups:url/text()}/files/get_file?id={$item/files:id/text()}"><xsl:value-of select="$item/rss:title/text()"/></a>
							</td>
					              <td>
								<xsl:value-of select="$item/rss:description/text()"/>
							</td>
					              <td>
								<a href="/contacts/{$item/dc:creator/text()}"><xsl:value-of select="$item/dc:creator/text()"/></a>
							</td>
							<td>
						            <a href="/{$item/groups:url/text()}"><xsl:value-of select="$item/groups:title/text()"/></a>
							</td>
			            		</tr>
			        </xsl:for-each>
			</table>
			
			<div class="resultsnav">
				<xsl:if test="results:prevlink">
					<a href="{results:prevlink/text()}">previous</a>
				</xsl:if>
				<xsl:if test="results:nextlink">
					<a href="{results:nextlink/text()}">next</a>
				</xsl:if>
			</div>
			
        </xsl:otherwise>

        </xsl:choose>

    </xsl:template>


</xsl:stylesheet>
