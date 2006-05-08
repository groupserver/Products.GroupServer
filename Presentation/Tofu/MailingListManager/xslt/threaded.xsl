<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:template name="email-present-threadsummary" xmlns:email="http://xwft.net/namespaces/email/0.9/">
    <xsl:variable name="groupId" select="//metadata/group/@id"/>
    <h1>
      <span class="groupName"><xsl:value-of select="//metadata/group"/></span>
      Topics
    </h1>

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
        <th class="dateCol">Date of Last Post</th>
        <th class="topicCol">Topic</th>
        <th class="postsCol">Posts</th>

      </tr>
      
      <xsl:for-each select="email:thread">
        <tr>
          <xsl:if test="position() mod 2 != 0">
            <xsl:attribute name="class">alternate</xsl:attribute>
          </xsl:if>
          <td class="dateCol"><xsl:value-of select="email:lastdate"/></td>
          <td class="topicCol"><a href="view_email?id={email:lastid}&amp;show_thread=1"><xsl:value-of select="email:subject"/></a></td>
          <td class="postsCol"><xsl:value-of select="@size"/></td>
        </tr>
      </xsl:for-each>
    </table>
    
    <!--=mpj17 Previous and next have changed their defns, sorry. =-->
    <ul class="resultsnav">
      <xsl:if test="@prev">
        <li>
          <a href="{@prev}">Next <xsl:value-of select="@prevbsize"/></a>
        </li>
      </xsl:if>
      <xsl:if test="@next">
        <li>
          <a href="{@next}">Previous <xsl:value-of select="@nextbsize"/></a>
        </li>
      </xsl:if>
    </ul><!--resultsnav-->
  </xsl:when>
  <xsl:otherwise>
    <p>There are currently no topics in this group.</p>
  </xsl:otherwise>
</xsl:choose>

<xsl:if test="//metadata/group/@visibility='open'"><hr/><p>An RSS feed of the latest 20 messages is available <a href="view_thread_rss">here</a>.</p></xsl:if>

</xsl:template>
</xsl:stylesheet>
