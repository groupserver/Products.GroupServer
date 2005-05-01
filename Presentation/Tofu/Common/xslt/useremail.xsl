<?xml version="1.0"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
	
	<xsl:template match="emaildetails">
	    <xsl:call-template name="useremail"/>
	</xsl:template>

	<xsl:template name="useremail">
         <xsl:variable name="havepreferred">
           <xsl:choose><xsl:when test="//user/emailaddresses/emailaddress/@preferred='1'">1</xsl:when><xsl:otherwise>0</xsl:otherwise></xsl:choose>
         </xsl:variable>
         <xsl:variable name="havenotpreferred">
           <xsl:choose><xsl:when test="//user/emailaddresses/emailaddress/@preferred='0'">1</xsl:when><xsl:otherwise>0</xsl:otherwise></xsl:choose>
         </xsl:variable>

		<div id="useremail">
			<fieldset>
				<legend>Email Addresses</legend>
                                <form action="/Scripts/set/" method="POST">
				<div class="row">Only email addresses listed here will be accepted when sending email
                                                 to a group. Please list all email addresses you might use for this purpose.</div>
				<div class="row">
	   			        <table class="manageemail">
                                          <xsl:if test="//user/emailaddresses/emailaddress">
                                          <xsl:for-each select="//user/emailaddresses/emailaddress">
                                              <tr>
				                  <td><xsl:value-of select="."/></td>
				                  <td><input type="checkbox" name="email:list" value="{.}"/></td>
                               		      </tr>
                                          </xsl:for-each>
                                              <tr>
                                                  <td>&#160;</td>
				                  <td><input type="submit" name="unset_email:method" value="Delete"/></td>
                               		      </tr>
                                              <tr><td colspan="2">Add an address for delivery:</td></tr>
                                          </xsl:if>
                                              <tr>
                                                  <td><input type="text" name="email:list" value="" width="60"/></td>
				                  <td><input type="submit" name="set_email:method" value="Add"/></td>
                               		      </tr>
                                        </table>
          			</div>
                                </form>
			</fieldset>

                        <xsl:if test="//user/emailaddresses/emailaddress">
			<fieldset>
				<legend>Default Email Delivery</legend>
                                <form action="/Scripts/set/" method="POST">
				<div class="row">If "Default Delivery" is selected in the groups below, these are the addresses at which you will
                                                 receive email. These addresses will be visible on your Profile to other people who are logged in 
                                                 to this site (people who are not logged in can not see your profile).</div>

				<div class="row">
	   			        <table class="manageemail">
                                          <xsl:if test="$havepreferred='1'">
                                          <xsl:for-each select="//user/emailaddresses/emailaddress">
                                              <xsl:if test="@preferred=1">
                                              <tr>
				                  <td><xsl:value-of select="."/></td>
				                  <td><input type="checkbox" name="email:list" value="{.}"/></td>
                               		      </tr>
                                              </xsl:if>
                                          </xsl:for-each>
                                              <tr>
                                                  <td>&#160;</td>
				                  <td><input type="submit" name="unset_default_email:method" value="Stop Delivery"/></td>
                               		      </tr>
                                          </xsl:if>
                                          <xsl:if test="$havenotpreferred='1'">
                                              <tr><td colspan="2">Add an address for delivery:</td></tr>
                                              <tr>
                                                  <td><select name="email:list" type="text">
                                                        <xsl:for-each select="//user/emailaddresses/emailaddress">
                                                          <xsl:if test="@preferred!=1"><option><xsl:value-of select="."/></option></xsl:if>
                                                        </xsl:for-each>
                                                      </select>
                                                  </td>
				                  <td><input name="set_default_email:method" value="Start Delivery" type="submit"/></td>
                               		      </tr>
                                          </xsl:if>
                                        </table>
				</div>
                                </form>
			</fieldset>

                        <xsl:for-each select="//user/groupmemberships/groupmembership">
                        <xsl:sort select="@id"/>
                        <xsl:variable name="gid" select="@id"/>
                        <xsl:variable name="delivery_setting" select="//user/groupdeliveries/group[@id=$gid]/@delivery_setting"/>
			<fieldset>
				<legend>Email Delivery for <a href="{@url}"><xsl:value-of select="@title"/></a></legend>
                                <form action="/Scripts/set/" method="POST">
                                <input type="hidden" name="came_from" value="{//output[@id='main']/metadata/division/@url}/contacts/{//root/output/user[@type='self']/id/text()}/useremail.xml"/>
                                <div class="row">
	   			        <table class="manageemail">
                                          <input type="hidden" name="group_id" value="{$gid}"/>
                                          <xsl:choose>
                                            <xsl:when test="$delivery_setting!='1' and //user/groupdeliveries/group[@id=$gid]/emailaddress">
                                              <xsl:for-each select="//user/groupdeliveries/group[@id=$gid]/emailaddress">
                                                <tr>
				                  <td><xsl:value-of select="."/></td>
				                  <td><input type="checkbox" name="email:list" value="{.}"/></td>
                                		</tr>
                                              </xsl:for-each>
                                              <tr>
                                                  <td>&#160;</td>
				                  <td><input type="submit" name="unset_delivery_email:method" value="Stop Delivery"/></td>
                               		      </tr>
                                            </xsl:when>
                                            <xsl:otherwise>
                                              <tr>
				                  <td colspan="2">No changes have been made to default email addresses</td>
				                  <!-- <td><input type="submit" name="disable_delivery:method" value="Disable Delivery"/></td> -->
                               		      </tr>
                                            </xsl:otherwise>
                                          </xsl:choose>
                                          <tr><td colspan="2">Add an address for delivery:</td></tr>
                                          <tr>
                                              <td><select name="email:list" type="text">
                                                    <xsl:if test="$delivery_setting!='1' and //user/groupdeliveries/group[@id=$gid]/emailaddress">
                                                      <option>Default Delivery</option>
                                                    </xsl:if>
                                                    <xsl:for-each select="//user/emailaddresses/emailaddress">
                                                      <xsl:variable name="email" select="."/>
                                                      <xsl:variable name="group" select="//user/groupdeliveries/group[@id=$gid]"/>
                                                      <xsl:if test="$delivery_setting='1' or count($group/emailaddress[.=$email])=0">
                                                        <option><xsl:value-of select="$email"/></option>
                                                      </xsl:if>
                                                    </xsl:for-each>
                                                   </select>
                                               </td>
				               <td><input name="set_delivery_email:method" value="Start Delivery" type="submit"/></td>
                               		  </tr>
                                          <tr><td colspan="2">The way you receive group email:</td></tr>
                                          <tr>
                                              <td><select name="delivery_type:list" type="text">
                                                    <option value="regular"><xsl:if test="$delivery_setting='3' and $delivery_setting='0'"><xsl:attribute name="selected">1</xsl:attribute></xsl:if>One email per group post</option>
                                                    <option value="topicdigest"><xsl:if test="$delivery_setting='3'"><xsl:attribute name="selected">1</xsl:attribute></xsl:if>Digest of topics</option>
                                                    <option value="disable"><xsl:if test="$delivery_setting='0'"><xsl:attribute name="selected">1</xsl:attribute></xsl:if>Delivery Disabled</option>
                                                  </select>
                                              </td>
				              <td><input name="set_delivery_type:method" value="Change Method" type="submit"/></td>
                               		  </tr>
                                        </table>
				</div>
                                </form>
                        </fieldset>

                        </xsl:for-each>

                        </xsl:if>
	        </div>
	</xsl:template>
</xsl:stylesheet>
