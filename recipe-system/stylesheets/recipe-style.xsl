<?xml version="1.0" encoding="UTF-8"?>

<xsl:stylesheet version=“1.0”
xmlns:xsl=“http://www.w3.org/1999/XSL/Transform”
xmlns:r=“http://www.example.com/recipe”>

<xsl:output method=“html” encoding=“UTF-8” indent=“yes”/>

<xsl:template match=”/”>
<html>
<head>
<title><xsl:value-of select=“r:recipe/r:title”/></title>
<style>
body {
font-family: ‘Segoe UI’, Tahoma, Geneva, Verdana, sans-serif;
max-width: 900px;
margin: 40px auto;
padding: 0 20px;
background-color: #f8f9fa;
color: #333;
line-height: 1.6;
}

```
      .recipe-container {
        background: white;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        padding: 40px;
      }
      
      h1 {
        color: #d32f2f;
        margin-bottom: 20px;
        font-size: 2.5em;
        border-bottom: 3px solid #d32f2f;
        padding-bottom: 10px;
      }
      
      .description {
        background-color: #fff3e0;
        padding: 20px;
        border-radius: 8px;
        margin: 20px 0;
        border-left: 4px solid #ff9800;
      }
      
      .tags {
        margin-top: 15px;
      }
      
      .tag {
        display: inline-block;
        background-color: #e3f2fd;
        color: #1976d2;
        padding: 5px 12px;
        border-radius: 20px;
        margin-right: 8px;
        margin-bottom: 8px;
        font-size: 0.85em;
        font-weight: 500;
      }
      
      .metadata {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
        gap: 15px;
        margin: 30px 0;
        padding: 20px;
        background-color: #f5f5f5;
        border-radius: 8px;
      }
      
      .metadata-item {
        text-align: center;
      }
      
      .metadata-label {
        font-weight: bold;
        color: #666;
        font-size: 0.9em;
        text-transform: uppercase;
        letter-spacing: 0.5px;
      }
      
      .metadata-value {
        font-size: 1.2em;
        color: #d32f2f;
        margin-top: 5px;
      }
      
      h2 {
        color: #d32f2f;
        margin-top: 30px;
        margin-bottom: 15px;
        font-size: 1.8em;
        border-bottom: 2px solid #ffcdd2;
        padding-bottom: 8px;
      }
      
      .ingredients {
        background-color: #f9f9f9;
        padding: 20px 30px;
        border-radius: 8px;
        margin: 20px 0;
      }
      
      .ingredient {
        padding: 8px 0;
        border-bottom: 1px dotted #ddd;
        font-size: 1.05em;
      }
      
      .ingredient:last-child {
        border-bottom: none;
      }
      
      .ingredient:before {
        content: "✓ ";
        color: #4caf50;
        font-weight: bold;
        margin-right: 8px;
      }
      
      .preparation {
        margin: 20px 0;
      }
      
      .step {
        margin: 15px 0;
        padding: 15px 20px;
        background-color: #fafafa;
        border-radius: 8px;
        border-left: 4px solid #d32f2f;
        position: relative;
        padding-left: 60px;
      }
      
      .step-number {
        position: absolute;
        left: 15px;
        top: 15px;
        background-color: #d32f2f;
        color: white;
        width: 32px;
        height: 32px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        font-size: 0.9em;
      }
      
      .step-text {
        font-size: 1.05em;
        line-height: 1.7;
      }
    </style>
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
      
      <h2>Ingredients</h2>
      <div class="ingredients">
        <xsl:for-each select="r:recipe/r:ingredients/r:ingredient">
          <div class="ingredient">
            <xsl:if test="@quantity">
              <strong><xsl:value-of select="@quantity"/>
              <xsl:if test="@unit">
                <xsl:text> </xsl:text><xsl:value-of select="@unit"/>
              </xsl:if>
              </strong>
              <xsl:text> - </xsl:text>
            </xsl:if>
            <xsl:value-of select="."/>
          </div>
        </xsl:for-each>
      </div>
      
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
  </body>
</html>
```

</xsl:template>

</xsl:stylesheet>