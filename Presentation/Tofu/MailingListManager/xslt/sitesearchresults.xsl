<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:email="http://xwft.net/namespaces/email/0.9/" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
	<xsl:output method="html" encoding="UTF-8"/>
	<xsl:template name="email-present-sitesearch-results">
		<table cellpadding="3" cellspacing="0" width="99%">
			<xsl:choose>
				<xsl:when test="@size=0">
					<p>No matching messages found.</p>
				</xsl:when>
				<xsl:otherwise>
					<p>Postings <strong><xsl:value-of select="@start"/></strong> to <strong><xsl:value-of select="number(@end)"/></strong> of the most recent postings are shown. There have been <strong><xsl:value-of select="@size"/></strong> postings in total. <xsl:value-of select="number(@end)-number(@start)+1"/> shown.</p>

				<table id="results">
					<tr>
						<th>Date</th>
						<th>Subject</th>
						<th>From</th>
					</tr>
					<xsl:for-each select="email:email">
						<tr>
							<xsl:if test="position() mod 2 != 0">
								<xsl:attribute name="class">alternate</xsl:attribute>
							</xsl:if>
							<td><xsl:value-of select="email:mailDate"/></td>
							<td><a href="view_email?id={@id}"><xsl:value-of select="email:mailSubject/text()"/></a></td>
							<td><xsl:value-of select="email:mailFrom/text()"/></td>
						</tr>
					</xsl:for-each>
					
					</table>
					
					<div class="resultsnav">
						<xsl:if test="@prev">
							<a href="{@prev}">prev <xsl:value-of select="@prevbsize"/></a>
						</xsl:if>
						<xsl:if test="@next">
							<a href="{@next}">next <xsl:value-of select="@nextbsize"/></a>
						</xsl:if>
					</div>
					
				</xsl:otherwise>
			</xsl:choose>
		</table>
	</xsl:template>
</xsl:stylesheet>
