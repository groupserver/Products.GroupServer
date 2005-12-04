<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
	<xsl:template name="email-present-threadsummary" xmlns:email="http://xwft.net/namespaces/email/0.9/">
            <xsl:variable name="groupId" select="//metadata/group/@id"/>
                        <h1>Topics</h1>

			<p><xsl:if test="number(@size)"><span class="note"><a href="view_results">Posts</a></span>
                           &#160;&#160;&#160;&#160;</xsl:if>
                           <xsl:if test="//groupmemberships/groupmembership[@id=$groupId]">
                             <span class="note"><a href="view_send_email">Start a new Topic</a></span>
                           </xsl:if>
                        </p>

                    <xsl:choose>
                        <xsl:when test="number(@size)">			
			<p>Numbers <strong><xsl:value-of select="@start"/></strong> to <strong><xsl:value-of select="number(@end)"/></strong> of the most recent topics are shown. <strong><xsl:value-of select="@size"/></strong> topics have taken place in total. <xsl:value-of select="number(@end)-number(@start)+1"/> shown.</p>

			<table id="results">
				<tr>
					<th>Date of Last Post</th>
					<th>Topic</th>
					<th>Posts</th>
			</tr>
				
			<xsl:for-each select="email:thread">
				<tr>
					<xsl:if test="position() mod 2 != 0">
						<xsl:attribute name="class">alternate</xsl:attribute>
					</xsl:if>
					<td><xsl:value-of select="email:lastdate"/></td>
					<td><a href="view_email?id={email:lastid}&amp;show_thread=1"><xsl:value-of select="email:subject"/></a></td>
					<td><xsl:value-of select="@size"/></td>
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
                        </xsl:when>
                        <xsl:otherwise>
                            <p>There are currently no topics in this group.</p>
                        </xsl:otherwise>
                    </xsl:choose>
                    
                    <xsl:if test="//metadata/group/@visibility='open'"><hr/><p>An RSS feed of the latest 20 messages is available <a href="view_thread_rss">here</a>.</p></xsl:if>
                    
	</xsl:template>
</xsl:stylesheet>
