<?xml version="1.0"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <!-- User Instructions Starts -->
  <xsl:template match="userinstructions">
    <div class="userinstructions">
      <xsl:apply-templates/>
    </div>
  </xsl:template>
  <!-- User Instructions Ends -->
  <!-- Contacts Starts -->
  <xsl:template match="users">
    <ul class="contacts">
      <xsl:for-each select="user">
        <xsl:sort select="name/preferredname" order="ascending"/>
        <xsl:call-template name="user"/>
      </xsl:for-each>
    </ul>
  </xsl:template>
  <xsl:template name="user">
    <li>
      <span class="name">
        <xsl:apply-templates select="name"/>
      </span>
      <xsl:apply-templates select="image | biography"
        mode="name"/>
    </li>
  </xsl:template>
  <xsl:template match="name">
    <a href="{../link/@url}">
      <xsl:value-of select="firstname"/>&#160;<xsl:value-of select="lastname"/>
    </a>
    <xsl:if test="../*[@present='auto']">&#160;(<xsl:for-each select="../*[@present='auto']"><xsl:if test="position()!=1">, </xsl:if><xsl:value-of select="@title"/>: <xsl:choose><xsl:when test="text()"><xsl:value-of select="text()"/></xsl:when><xsl:otherwise>[not set]</xsl:otherwise></xsl:choose></xsl:for-each>)</xsl:if>
  </xsl:template>

  <xsl:template match="image" mode="name">
    <img 
      src="/Presentation/Tofu/Common/images/16x16/image-x-generic.gif"
      width="16" height="16"
      alt="Image present."/>
  </xsl:template>

  <xsl:template match="biography" mode="name">
    <img 
      src="/Presentation/Tofu/Common/images/16x16/text-x-generic.gif"
      width="16" height="16" 
      alt="Biography present."/>
  </xsl:template>

  <!-- Contacts Ends -->

  <!-- User Detail Page Starts -->
  <xsl:template match="userdetails">
    <xsl:apply-templates select="//root/output/user"/>
  </xsl:template>
  <xsl:template match="//root/output/user">
    <xsl:choose>
      <xsl:when test="@type='other'">
        <xsl:call-template name="userother"/>
      </xsl:when>
      <xsl:when test="@type='self'">
        <xsl:choose>
          <xsl:when test="count(//root/output/user[@type='other'])=0">
            <xsl:call-template name="userself"/>
          </xsl:when>
        </xsl:choose>
      </xsl:when>
    </xsl:choose>
  </xsl:template>
  <!-- Other User Detail Page Starts -->
  <xsl:template name="userother">
    <xsl:if test="count(image)=1">
      <div class="userimage">
        <img src="{image}" alt="Photo of {name/preferredname}"/>
      </div>
    </xsl:if>
    <table class="userother">
      <tr>
        <th valign="top">Name:</th>
        <td>
          <xsl:value-of select="name/preferredname"/> 
          (<xsl:value-of select="name/firstname"/> 
          <xsl:value-of select="name/lastname"/>)
          <xsl:if test="type"> &#160;( <xsl:value-of select="type/text()"/> )
        </xsl:if>
      </td>
    </tr>
    <xsl:if test="groupmemberships/groupmembership">
      <tr>
        <th valign="top">Group Memberships:</th>
        <td>
          <ul class="groups">
            <xsl:for-each select="groupmemberships/groupmembership">
              <xsl:sort select="@divisionUrl"/>
              <li>
                <a href="{@url}">
                  <xsl:value-of select="@title"/>
                </a> (<xsl:value-of select="@divisionName"/>)
              </li>
            </xsl:for-each>
          </ul>
        </td>
      </tr>
    </xsl:if>
    <tr>
      <th valign="top">Email Addresses:</th>
      <td>
        <xsl:choose>
          <xsl:when test="//metadata/showEmailAddressTo/text() = 'request'">
            <a href="/contacts/{id}/user-request-contact.xml"
              title="Request contact with {name/preferredname}">Request
            Contact</a>
          </xsl:when>
          <xsl:when test="//metadata/showEmailAddressTo/text() != 'nobody'">
            <ul class="emails">
              <xsl:for-each select="emailaddresses/emailaddress">
                <li>
                  <a href="mailto:{.}">
                    <xsl:value-of select="."/>
                  </a>
                </li>
              </xsl:for-each>
            </ul>
          </xsl:when>
          <xsl:otherwise> Email address has been hidden </xsl:otherwise>
        </xsl:choose>
      </td>
    </tr>
    <xsl:for-each select="*[@present='auto']">
      <tr>
        <th valign="top">
          <xsl:value-of select="@title"/> : </th>
          <td>
            <xsl:choose>
              <xsl:when test="@href != '' and text() != ''">
                <a href="{@href}"><xsl:apply-templates select="text()"/></a>
              </xsl:when>
              <xsl:when test="text() != ''">
                <xsl:apply-templates select="text()"/>
              </xsl:when>
              <xsl:otherwise>
                [not set]
              </xsl:otherwise>
            </xsl:choose>
          </td>
        </tr>
      </xsl:for-each>
    </table>
  </xsl:template>
  <!-- Other User Detail Page Ends -->
  <!-- Personal User Detail Page Starts -->
  <xsl:template name="userself">
    <div id="userself">
      <xsl:if test="count(image)=1">
        <div class="userimage">
          <img src="{image}" alt="Photo of {name/preferredname}"/>
          <xsl:choose>
            <xsl:when
              test="//input[@id='show_image']/object/element/@default='1'">
              <p>Your photo is visible to others</p>
            </xsl:when>
            <xsl:when test="//output/metadata/alwaysshowphoto/text()='1'">
              <p>Your photo is visible to others</p>
            </xsl:when>
            <xsl:otherwise>
              <p> Your photo is <strong>not</strong> visible to others </p>
            </xsl:otherwise>
          </xsl:choose>
        </div>
      </xsl:if>
      <fieldset>
        <legend>Your Profile as it Appears to Others</legend>
        <div class="row">
          <div class="label">Name:</div>
          <div class="field">
            <span class="firstname">
              <xsl:value-of select="name/preferredname"/>
            </span>&#160;<span class="lastname">
            <xsl:value-of select="name/lastname"/>
          </span>
          <xsl:if test="type">&#160;( <xsl:value-of select="type/text()"/> )
        </xsl:if>
      </div>
    </div>
    <xsl:if test="groupmemberships/groupmembership">
      <div class="row">
        <div class="label">Group Memberships:</div>
        <div class="field">
          <ul class="emails">
            <xsl:for-each select="groupmemberships/groupmembership">
              <xsl:sort select="@divisionUrl"/>
              <li>
                <a href="{@url}">
                  <xsl:value-of select="@title"/>
                </a> (<xsl:value-of select="@divisionName"/>)
              </li>
            </xsl:for-each>
          </ul>
        </div>
      </div>
    </xsl:if>
    <div class="row">
      <div class="label">Email Addresses:</div>
      <div class="field">
        <xsl:choose>
          <xsl:when test="//metadata/showEmailAddressTo/text() = 'request'">
            <a href="/contacts/{user[@type=other]/id}/user-request-contact.xml"
              title="Request contact with {name/preferredname}">Request
            Contact</a>
          </xsl:when>
          <xsl:when test="//metadata/showEmailAddressTo/text() != 'nobody'">
            <ul class="emails">
              <xsl:for-each select="emailaddresses/emailaddress">
                <li>
                  <a href="mailto:{.}">
                    <xsl:value-of select="."/>
                  </a>
                </li>
              </xsl:for-each>
            </ul>
          </xsl:when>
          <xsl:otherwise> Email address has been hidden </xsl:otherwise>
        </xsl:choose>
      </div>
    </div>
    <xsl:for-each select="*[@present='auto']">
      <div class="row">
        <div class="label">
          <xsl:value-of select="@title"/>:</div>
          <div class="field">
            <xsl:choose>
              <xsl:when test="@href != '' and text() != ''">
                <a href="{@href}"><xsl:apply-templates select="text()"/></a>
              </xsl:when>
              <xsl:when test="text() != ''">
                <xsl:apply-templates select="text()"/>
              </xsl:when>
              <xsl:otherwise>
                [not set]
              </xsl:otherwise>
            </xsl:choose>
          </div>
        </div>
      </xsl:for-each>
    </fieldset>
  </div>
</xsl:template>
<!-- Personal User Detail Page Ends -->
</xsl:stylesheet>
