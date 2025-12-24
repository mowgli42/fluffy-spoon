<?xml version="1.0" encoding="UTF-8"?>

<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:r="http://www.example.com/recipe">

<xsl:output method="html" encoding="UTF-8" indent="yes"/>

<xsl:template match="/">
<html>
<head>
<title><xsl:value-of select="r:recipe/r:title"/></title>
<style><![CDATA[
body {
font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
max-width: 900px;
margin: 40px auto;
padding: 0 20px;
background-color: #f8f9fa;
color: #333;
line-height: 1.6;
}

.recipe-container {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  padding: 20px;
}

h1 {
  color: #667eea;
  margin-bottom: 10px;
  font-size: 1.8em;
  border-bottom: 3px solid #667eea;
  padding-bottom: 8px;
}

.description {
  background-color: #f0f1ff;
  padding: 12px;
  border-radius: 8px;
  margin: 10px 0;
  border-left: 4px solid #667eea;
  font-size: 0.9em;
  line-height: 1.4;
}

.tags {
  margin-top: 8px;
}

.tag {
  display: inline-block;
  background-color: #e8ebff;
  color: #667eea;
  padding: 3px 8px;
  border-radius: 20px;
  margin-right: 5px;
  margin-bottom: 5px;
  font-size: 0.75em;
  font-weight: 500;
}

.metadata {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
  gap: 10px;
  margin: 15px 0;
  padding: 12px;
  background-color: #f5f5f5;
  border-radius: 8px;
}

.metadata-item {
  text-align: center;
}

.metadata-label {
  font-weight: bold;
  color: #666;
  font-size: 0.75em;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.metadata-value {
  font-size: 0.9em;
  color: #667eea;
  margin-top: 3px;
}

h2 {
  color: #667eea;
  margin-top: 15px;
  margin-bottom: 10px;
  font-size: 1.3em;
  border-bottom: 2px solid #e8ebff;
  padding-bottom: 6px;
}

.ingredients {
  background-color: #f9f9f9;
  padding: 15px;
  border-radius: 8px;
  margin: 10px 0;
}

.ingredient {
  padding: 5px 0;
  border-bottom: 1px dotted #ddd;
  font-size: 0.95em;
  display: flex;
  align-items: flex-start;
  gap: 8px;
}

.ingredient:last-child {
  border-bottom: none;
}

.ingredient input[type="checkbox"] {
  margin-top: 4px;
  cursor: pointer;
  width: 18px;
  height: 18px;
  accent-color: #667eea;
}

.ingredient label {
  cursor: pointer;
  flex: 1;
}

.ingredient input[type="checkbox"]:checked + label {
  text-decoration: line-through;
  color: #999;
}

.preparation {
  margin: 10px 0;
}

.step {
  margin: 8px 0;
  padding: 10px 12px;
  background-color: #fafafa;
  border-radius: 8px;
  border-left: 4px solid #667eea;
  position: relative;
  padding-left: 45px;
}

.step-number {
  position: absolute;
  left: 8px;
  top: 50%;
  transform: translateY(-50%);
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  width: 26px;
  height: 26px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 0.8em;
}

.step-text {
  font-size: 0.95em;
  line-height: 1.5;
}

.ingredients-and-steps {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-top: 10px;
}

.ingredients-section,
.preparation-section {
  min-width: 0;
}

@media (max-width: 900px) {
  .ingredients-and-steps {
    grid-template-columns: 1fr;
  }
}
]]></style>
</head>
<body>
  <div class="recipe-container">
    <h1><xsl:value-of select="r:recipe/r:title"/></h1>
    
    <div class="description">
      <xsl:value-of select="r:recipe/r:description/r:summary"/>
      
      <xsl:if test="r:recipe/r:description/r:tags/r:tag">
        <div class="tags">
          <xsl:for-each select="r:recipe/r:description/r:tags/r:tag">
            <span class="tag"><xsl:value-of select="."/></span>
          </xsl:for-each>
        </div>
      </xsl:if>
    </div>
    
    <xsl:if test="r:recipe/r:metadata">
      <div class="metadata">
        <xsl:if test="r:recipe/r:metadata/r:servings">
          <div class="metadata-item">
            <div class="metadata-label">Servings</div>
            <div class="metadata-value"><xsl:value-of select="r:recipe/r:metadata/r:servings"/></div>
          </div>
        </xsl:if>
        <xsl:if test="r:recipe/r:metadata/r:prepTime">
          <div class="metadata-item">
            <div class="metadata-label">Prep Time</div>
            <div class="metadata-value"><xsl:value-of select="r:recipe/r:metadata/r:prepTime"/></div>
          </div>
        </xsl:if>
        <xsl:if test="r:recipe/r:metadata/r:cookTime">
          <div class="metadata-item">
            <div class="metadata-label">Cook Time</div>
            <div class="metadata-value"><xsl:value-of select="r:recipe/r:metadata/r:cookTime"/></div>
          </div>
        </xsl:if>
        <xsl:if test="r:recipe/r:metadata/r:totalTime">
          <div class="metadata-item">
            <div class="metadata-label">Total Time</div>
            <div class="metadata-value"><xsl:value-of select="r:recipe/r:metadata/r:totalTime"/></div>
          </div>
        </xsl:if>
        <xsl:if test="r:recipe/r:metadata/r:difficulty">
          <div class="metadata-item">
            <div class="metadata-label">Difficulty</div>
            <div class="metadata-value"><xsl:value-of select="r:recipe/r:metadata/r:difficulty"/></div>
          </div>
        </xsl:if>
      </div>
    </xsl:if>
    
    <div class="ingredients-and-steps">
      <div class="ingredients-section">
        <h2>Ingredients</h2>
        <div class="ingredients">
          <xsl:for-each select="r:recipe/r:ingredients/r:ingredient">
            <div class="ingredient">
              <input type="checkbox" id="ingredient_{position()}"/>
              <label for="ingredient_{position()}">
                <xsl:if test="@quantity">
                  <strong><xsl:value-of select="@quantity"/>
                  <xsl:if test="@unit">
                    <xsl:text> </xsl:text><xsl:value-of select="@unit"/>
                  </xsl:if>
                  </strong>
                  <xsl:text> - </xsl:text>
                </xsl:if>
                <xsl:value-of select="."/>
              </label>
            </div>
          </xsl:for-each>
        </div>
      </div>
      
      <div class="preparation-section">
        <h2>Preparation Steps</h2>
        <div class="preparation">
          <xsl:for-each select="r:recipe/r:preparation/r:step">
            <div class="step">
              <div class="step-number"><xsl:value-of select="@number"/></div>
              <div class="step-text"><xsl:value-of select="."/></div>
            </div>
          </xsl:for-each>
        </div>
      </div>
    </div>
  </div>
</body>
</html>
</xsl:template>

</xsl:stylesheet>
