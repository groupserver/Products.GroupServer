<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:file="http://xwft.org/ns/filelibrary/0.9/"  xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method="html" encoding="UTF-8"/>
    <xsl:template name="file-present-results">
    <xsl:variable name="anonymous" select="//user[@type='self']/roles/role/text() = 'Anonymous'"/>    
    <xsl:choose>
        <xsl:when test="@isroot='1'">
        <h1>Files Area</h1>
        </xsl:when>
        <xsl:otherwise>
        <h1>Files Area: <xsl:value-of select="@foldertitle"/></h1>
        </xsl:otherwise>
    </xsl:choose>

            <xsl:for-each select="file:folder">
              <xsl:if test="number(@depth)&lt;0">
              <p>Parent folder: <a href="../view_files"><xsl:value-of select="@id"/></a> (<xsl:value-of select="@filecount"/> files, <xsl:value-of select="@foldercount"/> folders)</p>
              </xsl:if>
            </xsl:for-each>

        <xsl:choose>
          <xsl:when test="count(file:folder[@id!='files']) > 0">
          <xsl:choose>
            <xsl:when test="@isroot='1'">
              <p>The files area contains these folders: <xsl:if test="$anonymous != 'true'"><a href="view_add_folder">add a new folder</a></xsl:if></p>
            </xsl:when>
            <xsl:otherwise>
              <p><strong><xsl:value-of select="@foldertitle"/></strong> contains these folders: <xsl:if test="$anonymous != 'true'"><a href="view_add_folder">add a new folder</a></xsl:if></p>
            </xsl:otherwise>
          </xsl:choose>
          <ul class="folders">   
            <xsl:for-each select="file:folder">
              <xsl:if test="number(@depth)&gt;0">
              <li><a href="{@id}/view_files"><xsl:value-of select="@id"/></a> (<xsl:value-of select="@filecount"/> files, <xsl:value-of select="@foldercount"/> folders) 
		   <xsl:if test="@deletable='1'">
		       <a href="remove_folder?id={@id}" title="Remove this Folder">remove this folder (and all files)</a>
		   </xsl:if></li>
              </xsl:if>
            </xsl:for-each>
          </ul> 
          </xsl:when>
                     
          <xsl:otherwise>
            <xsl:choose>
              <xsl:when test="@isroot='1'">
                <p>The files area contains no folders. <xsl:if test="$anonymous != 'true'"><a href="view_add_folder">add a new folder</a></xsl:if></p>
              </xsl:when>
              <xsl:otherwise>
                <p><strong><xsl:value-of select="@foldertitle"/></strong> contains no folders. <xsl:if test="$anonymous != 'true'"><a href="view_add_folder">add a new folder</a></xsl:if></p> 
              </xsl:otherwise>
            </xsl:choose> 
          </xsl:otherwise>

        </xsl:choose>

        <xsl:choose>
        <xsl:when test="@size=0">
            <xsl:choose>
              <xsl:when test="@isroot='1'">
                <p>The files area contains no files. <xsl:if test="$anonymous != 'true'"><a href="view_add_file">add a new file</a></xsl:if></p>
              </xsl:when>
              <xsl:otherwise>
                <p><strong><xsl:value-of select="@foldertitle"/></strong> contains no files. <xsl:if test="$anonymous != 'true'"><a href="view_add_file">add a new file</a></xsl:if></p> 
              </xsl:otherwise>
            </xsl:choose>
        </xsl:when>
        <xsl:otherwise>


            <xsl:choose>
              <xsl:when test="@isroot='1'">
                <p>The files area contains <strong><xsl:value-of select="@size"/></strong> files (files <strong><xsl:value-of select="@start"/></strong> to <strong><xsl:value-of select="number(@end)"/></strong> shown): <xsl:if test="$anonymous != 'true'"><a href="view_add_file">add a new file</a></xsl:if></p>
              </xsl:when>
              <xsl:otherwise>
                <p><strong><xsl:value-of select="@foldertitle"/></strong> contains <strong><xsl:value-of select="@size"/></strong> files (files <strong><xsl:value-of select="@start"/></strong> to <strong><xsl:value-of select="number(@end)"/></strong> shown): <xsl:if test="$anonymous != 'true'"><a href="view_add_file">add a new file</a></xsl:if></p> 
              </xsl:otherwise>
            </xsl:choose>

	<table id="results">
        	<tr>
			<th><a href="{@reversedate}" title="Sort by Date">Date</a>	</th>
			<th>Title</th>
			<th>Description</th>
			<th>Size</th>
			<th>Posted By</th>
		</tr>
		
       	<xsl:for-each select="file:file">
        		<xsl:choose>
            			<xsl:when test="position() mod 2 != 0">
            				<tr class="alternate">
             					<td><xsl:value-of select="file:modification_time"/></td>
						<td><a href="get_file?id={@id}"><xsl:value-of select="file:title"/></a></td>
						<td><xsl:value-of select="dc:Description"/></td>
						<td><xsl:value-of select="file:size"/></td>
						<td>
							<a href="/contacts/{dc:Creator}/">
								<xsl:value-of select="file:Creator"/>
							</a>
						</td>
						<xsl:if test="@deletable='1'">
							<td><a href="remove_file?id={@id}" title="Remove this File">remove file</a></td>
						</xsl:if>
            				</tr>
           			</xsl:when>
            			<xsl:otherwise>
            				<tr>
              				<td><xsl:value-of select="file:modification_time"/></td>
						<td><a href="get_file?id={@id}"><xsl:value-of select="file:title"/></a></td>
						<td><xsl:value-of select="dc:Description"/></td>
						<td><xsl:value-of select="file:size"/></td>
						<td>
							<a href="/contacts/{dc:Creator}/">
								<xsl:value-of select="file:Creator"/>
							</a>
						</td>
						<xsl:if test="@deletable='1'">
							<td><a href="remove_file?id={@id}" title="Remove this File">remove file</a></td>
						</xsl:if>					
            				</tr>
            			</xsl:otherwise>
        		</xsl:choose>
        	</xsl:for-each>
	</table>
	
	<div class="resultsnav">
		<xsl:if test="@prev"><a href="{@prev}">prev <xsl:value-of select="@prevbsize"/> file/s</a></xsl:if>
		<xsl:if test="@next"><a href="{@next}">next <xsl:value-of select="@nextbsize"/> file/s</a></xsl:if>
	</div>

        </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
</xsl:stylesheet>
