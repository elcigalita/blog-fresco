<?xml version="1.0"?>
<xsl:stylesheet version="1.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:atom="http://www.w3.org/2005/Atom">

  <xsl:output method="html" indent="yes"/>

  <xsl:template match="/atom:feed">
    <html>
      <head>
        <title><xsl:value-of select="atom:title"/></title>
        <style>
          body { font-family: Arial; max-width: 800px; margin: auto; }
          h2 { color: #4CAF50; }
          .entry { border-bottom: 1px solid #ccc; margin: 20px 0; padding-bottom: 10px; }
          .date { color: #888; font-size: 0.9em; }
        </style>
      </head>
      <body>
        <h1><xsl:value-of select="atom:title"/></h1>
        <p><xsl:value-of select="atom:subtitle"/></p>
        <xsl:for-each select="atom:entry">
          <div class="entry">
            <h2><a href="{atom:link/@href}"><xsl:value-of select="atom:title"/></a></h2>
            <p class="date"><xsl:value-of select="atom:updated"/></p>
            <div><xsl:value-of select="atom:content" disable-output-escaping="yes"/></div>
          </div>
        </xsl:for-each>
      </body>
    </html>
  </xsl:template>

</xsl:stylesheet>
