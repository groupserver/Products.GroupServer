<?xml version="1.0"?>
<xsl:stylesheet version="1.0"
	xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
	xmlns:dw="http://iopen.net/schema/docbook-web/0.9"
	xmlns:dc="http://purl.org/dc/elements/1.1/"
	xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
	xmlns:rss="http://purl.org/rss/1.0/"
	xmlns:slash="http://purl.org/rss/1.0/modules/slash/"
	xmlns:xml="http://www.w3.org/XML/1998/namespace"
	xmlns:a="http://purl.org/rss/1.0/modules/syndication/"
	xmlns:admin="http://webns.net/mvcb/"
	xmlns:pageinfo="http://iopen.net/schema/pageinfo"
	xmlns:nav="http://iopen.net/schema/nav"
	xmlns:xhtml="http://www.w3.org/1999/xhtml"
	xmlns:xf="http://www.w3.org/2002/xforms" 
	exclude-result-prefixes="xf xhtml nav pageinfo dw dc rdf rss slash xml a admin">
	
	<!-- Return true if the passed value (match) matches the value of the specified node (ref) -->
	<xsl:template name="match-single">
		<xsl:param name="ref" />
		<xsl:param name="match" />
		<xsl:variable name="orig">
			<xsl:value-of
				select="//data/xf:model/xf:instance/data/*[name()=$ref]/text()" />
		</xsl:variable>
		<xsl:value-of select="number($orig=$match)" />
	</xsl:template>

	<!-- Return true if the passed value (match), a space-delimited list of values, contains the value of the specified node (ref) -->
	<xsl:template name="match-in-list">
		<xsl:param name="ref" />
		<xsl:param name="match" />
		<xsl:param name="orig">
			<xsl:value-of
				select="//data/xf:model/xf:instance/data/*[name()=$ref]/text()" />
		</xsl:param>

		<xsl:variable name="before">
			<xsl:value-of select="substring-before($orig, ' ')" />
		</xsl:variable>
		<xsl:variable name="after">
			<xsl:value-of select="substring-after($orig, ' ')" />
		</xsl:variable>
		<xsl:choose>

			<xsl:when
				test="$before = '' and $after = '' and starts-with($orig, $match) and string-length($orig) = string-length($match)">
				<xsl:value-of select="'1'" />
			</xsl:when>
			<xsl:when
				test="starts-with($before, $match) and string-length($before) = string-length($match)">
				<xsl:value-of select="'1'" />
			</xsl:when>
			<xsl:when
				test="$after != '' and not(starts-with($before, $match))">
				<xsl:call-template name="match-in-list">
					<xsl:with-param name="ref">
						<xsl:value-of select="$ref" />
					</xsl:with-param>
					<xsl:with-param name="match">
						<xsl:value-of select="$match" />
					</xsl:with-param>
					<xsl:with-param name="orig">
						<xsl:value-of select="$after" />
					</xsl:with-param>
				</xsl:call-template>
			</xsl:when>
			<xsl:otherwise>
				<xsl:value-of select="'0'" />
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>

	<!-- Match the data node -->
	<xsl:template match="data" />

	<!-- Match an XForms model -->
	<xsl:template name="xf:model">
		<div class="xforms_model">
			<input type="hidden" name="__submit__" value="{@id}" />
			<xsl:for-each select="//data/xf:model">
				<input type="hidden" name="__models__" value="{@id}" />
				<xsl:for-each select="xf:instance/data/*">
					<input type="hidden"
						name="__instance+{ancestor::xf:model/@id}+{name()}"
						value="{text()}" />
				</xsl:for-each>
				<xsl:for-each select="xf:submission">
					<input type="hidden"
						name="__submission_action+{../@id}+{@id}" value="{@action}" />
					<input type="hidden"
						name="__submission_method+{../@id}+{@id}" value="{@method}" />
					<xsl:if test="@target">
						<input type="hidden"
							name="__submission_target+{../@id}+{@id}" value="{@target}" />
					</xsl:if>
				</xsl:for-each>
			</xsl:for-each>
		</div>
	</xsl:template>
	
	<!-- Match an XForms submit element -->
	<xsl:template match="xf:submit">
		<div class="formelement{@class}">
			<input type="submit" name="__submit+{@model}+{@submission}"
				onclick="submitButtonHandler(this)" class="{@class}"
				value="{xf:label/text()}" title="{xf:hint/text()}" />
		</div>
	</xsl:template>
	
	<!-- Match an XForms input element -->
	<xsl:template match="xf:input">
		<div class="formelement{@class}">
			<xsl:variable name="ref">
				<xsl:call-template name="getref">
					<xsl:with-param name="model" select="@model" />
					<xsl:with-param name="item" select="." />
				</xsl:call-template>
			</xsl:variable>
			<xsl:variable name="model">
				<xsl:value-of select="@model" />
			</xsl:variable>
			<xsl:variable name="bind">
				<xsl:value-of select="@bind" />
			</xsl:variable>

			<!-- Build the label -->
			<xsl:call-template name="label">
				<xsl:with-param name="labelNode" select="xf:label" />
			</xsl:call-template>

         	<div class="hint"><xsl:apply-templates select="xf:hint"/></div>
			<input type="text" id="{@model}-{$ref}"
				name="{@model}+{$ref}" class="{@class}" title="{xf:hint/text()}">
				<xsl:attribute name="value">	<xsl:call-template
						name="xforms-fetch-instance-data">
						<xsl:with-param name="model" select="@model" />
						<xsl:with-param name="bind" select="@bind" />
						<xsl:with-param name="ref" select="@ref" />
					</xsl:call-template>	</xsl:attribute>
				<!-- Add a "required" class if this is a required item -->
				<xsl:if
					test="boolean(//data/xf:model[@id=$model]/xf:bind[@id=$bind]/@required)">
					<xsl:attribute name="class">required</xsl:attribute>
				</xsl:if>
			</input>
		</div>
	</xsl:template>

	<!-- Match an XForms date element (basically the same as a text input field with an additional link to pop up a calendar control) -->

	<xsl:template match="xf:date">
		<div class="formelement{@class}">
			<xsl:variable name="ref">
				<xsl:call-template name="getref">
					<xsl:with-param name="model" select="@model" />
					<xsl:with-param name="item" select="." />
				</xsl:call-template>
			</xsl:variable>
			<xsl:variable name="model">
				<xsl:value-of select="@model" />
			</xsl:variable>
			<xsl:variable name="bind">
				<xsl:value-of select="@bind" />
			</xsl:variable>

			<!-- Build the label -->
			<xsl:call-template name="label">
				<xsl:with-param name="labelNode" select="xf:label" />
			</xsl:call-template>

			<input type="text" id="{@model}-{$ref}"
				name="{@model}+{$ref}" class="{@class}" title="{xf:hint/text()}">
				<xsl:attribute name="value">	<xsl:call-template
						name="xforms-fetch-instance-data">
						<xsl:with-param name="model" select="@model" />
						<xsl:with-param name="bind" select="@bind" />
						<xsl:with-param name="ref" select="@ref" />
					</xsl:call-template></xsl:attribute>
				<!-- Add a "required" class if this is a required item -->
				<xsl:if
					test="boolean(//data/xf:model[@id=$model]/xf:bind[@id=$bind]/@required)">
					<xsl:attribute name="class">required</xsl:attribute>
				</xsl:if>
			</input>

			<div class="calendarcontrol">

				<!-- Add the calendar control link -->
				<a href="javascript: void(0);"
					onmouseover="if (timeoutId) clearTimeout(timeoutId);window.status='Show Calendar';return true;"
					onmouseout="if (timeoutDelay) calendarTimeout();window.status='';"
					onclick="if (!g_Calendar) new Calendar(new Date(), '{@model}-{$ref}-calendar', 'Presentation/Tofu/XForms/images/');g_Calendar.show(event,'{@model}-{$ref}',false); return false;">
					<img
						src="/Presentation/Tofu/XForms/images/calendar.gif"
						name="imgCalendar" width="34" height="21" border="0" alt="" />
				</a>


				<!-- Add a DIV to contain the calendar control -->
				<div class="calendar" id="{@model}-{$ref}-calendar"
					onmouseout="calendarTimeout();"
					onmouseover="if (timeoutId) clearTimeout(timeoutId);">
					&#160;
				</div>
				<!--
					if (timeoutDelay) document.write('');
					document.write('></div>');
				-->
			</div>

		</div>
	</xsl:template>

	<!-- Match an XForms secret element -->
	<xsl:template match="xf:secret">
		<xsl:variable name="ref">
			<xsl:call-template name="getref">
				<xsl:with-param name="model" select="@model" />
				<xsl:with-param name="item" select="." />
			</xsl:call-template>
		</xsl:variable>
		<xsl:variable name="model">
			<xsl:value-of select="@model" />
		</xsl:variable>
		<xsl:variable name="bind">
			<xsl:value-of select="@bind" />
		</xsl:variable>
		<div class="formelement{@class}">
			<xsl:call-template name="label">
				<xsl:with-param name="labelNode" select="xf:label" />
			</xsl:call-template>
			<input type="password" id="{@model}-{$ref}"
				name="{@model}+{$ref}" class="{@class}" title="{xf:hint/text()}">
				<xsl:attribute name="value">	<xsl:call-template
						name="xforms-fetch-instance-data">
						<xsl:with-param name="model" select="@model" />
						<xsl:with-param name="bind" select="@bind" />
						<xsl:with-param name="ref" select="@ref" />
					</xsl:call-template>	</xsl:attribute>
				<!-- Add a "required" class if this is a required item -->
				<xsl:if
					test="boolean(//data/xf:model[@id=$model]/xf:bind[@id=$bind]/@required)">
					<xsl:attribute name="class">required</xsl:attribute>
				</xsl:if>
			</input>
		</div>
	</xsl:template>

	<!-- Get the value of the specified instance item (ref) from the specified (model). This may be from either
		a direct reference to the item, or via a bind element if no ref parameter is specified. Since XSLT can't evaluate
		XPath expressions at run time, we're assuming that the nodeset attribute simply refers to a ref in the same model (for now) -->

	<xsl:template name="xforms-fetch-instance-data">
		<xsl:param name="model" />
		<xsl:param name="bind" />
		<xsl:param name="ref" />

		<xsl:choose>
			<xsl:when test="$bind != ''">
				<xsl:variable name="bindref">
					<xsl:value-of
						select="//data/xf:model[@id=$model]/xf:bind[@id=$bind]/@nodeset" />
				</xsl:variable>
				<xsl:apply-templates
					select="//data/xf:model[@id=$model]/xf:instance//*[name()=$bindref]/." />
			</xsl:when>
			<xsl:when test="$ref != ''">
				<xsl:apply-templates
					select="//data/xf:model[@id=$model]/xf:instance//*[name()=$ref]/." />
			</xsl:when>
			<xsl:otherwise />
		</xsl:choose>

	</xsl:template>

	<!-- Get the instance reference from either the ref attribute of the passed node or the associated bind -->
	<xsl:template name="getref">
		<xsl:param name="model" />

		<xsl:param name="item" />
		<xsl:choose>
			<xsl:when test="$item/@bind">
				<xsl:value-of
					select="//data/xf:model[@id=$model]/xf:bind[@id=$item/@bind]/@nodeset" />
			</xsl:when>
			<xsl:when test="$item/@ref">
				<xsl:value-of select="$item/@ref" />
			</xsl:when>
			<xsl:otherwise />

		</xsl:choose>
	</xsl:template>

	<!-- Match an XForms textarea element -->
	<xsl:template match="xf:textarea">
		<xsl:variable name="ref">
			<xsl:call-template name="getref">
				<xsl:with-param name="model" select="@model" />
				<xsl:with-param name="item" select="." />
			</xsl:call-template>
		</xsl:variable>
		<xsl:variable name="model">
			<xsl:value-of select="@model" />
		</xsl:variable>
		<xsl:variable name="bind">
			<xsl:value-of select="@bind" />
		</xsl:variable>

		<div class="formelement{@class}">
			<!-- Build the label -->
			<xsl:call-template name="label">
				<xsl:with-param name="labelNode" select="xf:label" />
			</xsl:call-template>
			<div class="hint"><xsl:apply-templates select="xf:hint"/></div>
			<textarea name="{@model}+{$ref}" class="{@class}"
				id="{@model}-{$ref}" title="{xf:hint/text()}"><!-- Copy across all other attributes in the xhtml namespace --><xsl:for-each
					select="@*[namespace-uri(.)='http://www.w3.org/1999/xhtml']">
					<xsl:attribute name="{local-name()}"><xsl:value-of select="." />	</xsl:attribute>
				</xsl:for-each><xsl:if
					test="boolean(//data/xf:model[@id=$model]/xf:bind[@id=$bind]/@required)">
					<xsl:attribute name="class">required</xsl:attribute>
				</xsl:if><xsl:call-template name="xforms-fetch-instance-data">
					<xsl:with-param name="model" select="@model" />
					<xsl:with-param name="bind" select="@bind" />
					<xsl:with-param name="ref" select="@ref" />
				</xsl:call-template></textarea>
		</div>

	</xsl:template>
	
	<!-- Match an XForms upload element -->
	<xsl:template match="xf:upload">
		<xsl:variable name="ref">
			<xsl:call-template name="getref">
				<xsl:with-param name="model" select="@model" />
				<xsl:with-param name="item" select="." />
			</xsl:call-template>
		</xsl:variable>
		<xsl:variable name="model">
			<xsl:value-of select="@model" />
		</xsl:variable>
		<xsl:variable name="bind">
			<xsl:value-of select="@bind" />
		</xsl:variable>	
		<div class="formelement{@class}">
			<xsl:call-template name="label">
				<xsl:with-param name="labelNode" select="xf:label" />
			</xsl:call-template>
         	<div class="hint"><xsl:apply-templates select="xf:hint"/></div>
			<input type="file" name="{$model}+{$ref}"
				id="{$model}-{$ref}" title="{xf:hint/text()}" class="{@class}"
				value="" />
		</div>
	</xsl:template>

	<!-- Match an XForms select1 element (used for single selects and radio buttons) -->
	<xsl:template match="xf:select1">
		<xsl:variable name="ref">
			<xsl:call-template name="getref">
				<xsl:with-param name="model" select="@model" />
				<xsl:with-param name="item" select="." />
			</xsl:call-template>
		</xsl:variable>
		<xsl:variable name="model">
			<xsl:value-of select="@model" />
		</xsl:variable>
		<xsl:variable name="bind">
			<xsl:value-of select="@bind" />
		</xsl:variable>

		<div class="formelement{@class}">
			<!-- Build the label -->
			<xsl:call-template name="label">
				<xsl:with-param name="labelNode" select="xf:label" />
			</xsl:call-template>

			<xsl:choose>
				<xsl:when
					test="@appearance='minimal' or @appearance='compact'">
					<select name="{@model}+{$ref}" id="{@model}-{$ref}"
						title="{xf:hint/text()}" class="{@class}">
						<xsl:if
							test="boolean(//data/xf:model[@id=$model]/xf:bind[@id=$bind]/@required)">
							<xsl:attribute name="class">	required	</xsl:attribute>
						</xsl:if>
						<!-- Copy across all other attributes in the xhtml namespace -->
						<xsl:for-each
							select="@*[namespace-uri(.)='http://www.w3.org/1999/xhtml']">
							<xsl:attribute name="{local-name()}"><xsl:value-of select="." /></xsl:attribute>
						</xsl:for-each>
						<xsl:for-each select="xf:item">
							<xsl:variable name="selected">
								<xsl:call-template
									name="match-single">
									<xsl:with-param name="ref"
										select="$ref" />
									<xsl:with-param name="match"
										select="xf:value/text()" />
								</xsl:call-template>
							</xsl:variable>
							<option value="{xf:value/text()}">
								<xsl:if test="$selected='1'">
									<xsl:attribute name="selected">1	</xsl:attribute>
								</xsl:if>
								<xsl:value-of select="xf:label/text()" />
							</option>
						</xsl:for-each>
					</select>

				</xsl:when>
				<xsl:otherwise>
					<xsl:for-each select="xf:item">
						<xsl:variable name="selected">
							<xsl:call-template name="match-single">
								<xsl:with-param name="ref"
									select="$ref" />
								<xsl:with-param name="match"
									select="xf:value/text()" />
							</xsl:call-template>
						</xsl:variable>
						<div class="radiogroup">
							<input type="radio"
								title="{../xf:hint/text()}" name="{../@model}+{$ref}"
								id="{../@model}-{$ref}" value="{xf:value/text()}">
								<xsl:if test="$selected='1'">
									<xsl:attribute name="checked">1</xsl:attribute>
								</xsl:if>
							</input>
							<label>
								<xsl:value-of select="xf:label/text()" />
							</label>
						</div>
					</xsl:for-each>
				</xsl:otherwise>
			</xsl:choose>
		</div>
	</xsl:template>

	<xsl:template match="xf:group">
		<div><xsl:attribute name="class"><xsl:choose><xsl:when test="@class">xfgroup-<xsl:value-of select="@class"/></xsl:when><xsl:otherwise>xfgroup</xsl:otherwise></xsl:choose></xsl:attribute>
			<xsl:apply-templates />
		</div>
	</xsl:template>

	<!-- Match an XForms select element (used for multiple selects and checkboxes) -->
	<xsl:template match="xf:select">
		<xsl:variable name="ref">
			<xsl:call-template name="getref">
				<xsl:with-param name="model" select="@model" />
				<xsl:with-param name="item" select="." />
			</xsl:call-template>
		</xsl:variable>
		<xsl:variable name="model">
			<xsl:value-of select="@model" />
		</xsl:variable>
		<xsl:variable name="bind">
			<xsl:value-of select="@bind" />
		</xsl:variable>

		<div class="formelement{@class}">
			<!-- Build the label -->
			<xsl:call-template name="label">
				<xsl:with-param name="labelNode" select="xf:label" />
			</xsl:call-template>

			<!-- Build the control -->
			<xsl:choose>
				<xsl:when
					test="@appearance='minimal' or @appearance='compact'">
					<select name="{$model}+{$ref}" id="{$model}-{$ref}"
						title="{xf:hint/text()}" multiple="1">
						<xsl:if
							test="boolean(//data/xf:model[@id=$model]/xf:bind[@id=$bind]/@required)">
							<xsl:attribute name="class">	required	</xsl:attribute>
						</xsl:if>
						<!-- Copy across all other attributes in the xhtml namespace -->
						<xsl:for-each
							select="@*[namespace-uri(.)='http://www.w3.org/1999/xhtml']">
							<xsl:attribute name="{local-name()}"><xsl:value-of select="." />	</xsl:attribute>
						</xsl:for-each>
						<xsl:for-each select="xf:item">
							<xsl:variable name="selected">
								<xsl:call-template
									name="match-in-list">
									<xsl:with-param name="ref"
										select="$ref" />
									<xsl:with-param name="match"
										select="xf:value/text()" />

								</xsl:call-template>
							</xsl:variable>
							<option value="{xf:value/text()}">
								<xsl:if test="$selected='1'">
									<xsl:attribute name="selected">1</xsl:attribute>
								</xsl:if>
								<xsl:value-of select="xf:label/text()" />
							</option>
						</xsl:for-each>
					</select>
				</xsl:when>
				<xsl:otherwise>
					<xsl:for-each select="xf:item">
						<xsl:variable name="selected">
							<xsl:call-template name="match-in-list">
								<xsl:with-param name="ref"
									select="$ref" />
								<xsl:with-param name="match"
									select="xf:value/text()" />
							</xsl:call-template>
						</xsl:variable>
						<div class="checkgroup">
							<input type="checkbox"
								title="{../xf:hint/text()}" name="{../@model}+{$ref}"
								id="{../@model}-{$ref}" value="{xf:value/text()}">
								<xsl:if test="$selected='1'">
									<xsl:attribute name="checked">1</xsl:attribute>
								</xsl:if>
							</input>
							<label for="{../@model}-{$ref}">
								<xsl:value-of select="xf:label/text()" />
							</label>
						</div>
					</xsl:for-each>
				</xsl:otherwise>
			</xsl:choose>

			<!-- Apply any additional content templates -->
			<xsl:apply-templates select="ulink" />
		</div>
	</xsl:template>

	<!-- Standard label template, implementing the required field check -->
	<xsl:template name="label">
		<xsl:param name="labelNode" />

		<!-- Get the model and other attributes of corresponding form element -->
		<xsl:variable name="labelParent" select="$labelNode/.." />
		<xsl:variable name="model">
			<xsl:value-of select="$labelParent/@model" />
		</xsl:variable>
		<xsl:variable name="bind">
			<xsl:value-of select="$labelParent/@bind" />
		</xsl:variable>
		<xsl:variable name="class">
			<xsl:value-of select="$labelParent/@class" />
		</xsl:variable>

		<xsl:variable name="ref">
			<xsl:call-template name="getref">
				<xsl:with-param name="model" select="@model" />
				<xsl:with-param name="item" select="$labelParent" />
			</xsl:call-template>
		</xsl:variable>

		<!-- Build the label -->
		<label for="{$model}-{$ref}" class="{$class}">
			<xsl:if
				test="boolean(//data/xf:model[@id=$model]/xf:bind[@id=$bind]/@required)">
				<xsl:attribute name="class">required</xsl:attribute>
			</xsl:if>
			<xsl:value-of select="xf:label/text()" />

			<!-- Apply any other templates -->
			<xsl:apply-templates select="$labelNode/*" />
		</label>
	</xsl:template>

</xsl:stylesheet>
