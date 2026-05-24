# Advanced Production Troubleshooting Guide

If the chatbot bubble is not appearing on your page, follow this systematic checklist.

## 1. Browser Diagnosis (The "F12" Test)
Open your browser, press **F12**, and go to the **Console** and **Network** tabs.
- **Red Errors**: Look for "Mixed Content" or "Refused to load script". This means your HTTPS site is blocking an HTTP script.
- **404 Errors**: Check if `chatbot-widget.js` or `chatbot-widget.css` are failing to load. If they are, your path is incorrect.

## 2. Path Resolution (Relative vs Absolute)
In your `index.jsp` or `.xhtml` file, you used:
`<link rel="stylesheet" href="css/chatbot-widget.css">`

**The Problem**: If your URL is `.../c/p/s/menu.xhtml`, the browser looks for the CSS in the `/c/p/s/css/` folder.
**The Fix**: Use an absolute path starting with `/`. 
- If your app is at the root: `/css/chatbot-widget.css`
- If your app has a context name: `/YourAppName/css/chatbot-widget.css`

## 3. JSF (.xhtml) Integration
Since your page ends in `.xhtml`, you are likely using **JavaServer Faces (JSF)**.
- **Don't edit index.jsp**: Use your main template file (often called `template.xhtml` or `layout.xhtml`).
- **JSF Tags**: Use the JSF way to include resources:
```xml
<h:head>
    <h:outputStylesheet name="chatbot-widget.css" library="css" />
</h:head>
<h:body>
    ...
    <script src="#{request.contextPath}/js/chatbot-widget.js"></script>
</h:body>
```

## 4. HTTPS & "Mixed Content"
If your JBoss is on `https` (Port 10443), your chatbot's internally configured `API_URL` must also be reached via HTTPS.
- **The Fix**: Ensure Section 4 of the [Minute-Level Guide](minute_level_guide.md) (Reverse Proxy) is completed. Your JS code should use:
`const API_URL = window.location.origin + "/chatbot-api";`

## 5. JBoss Cache
JBoss sometimes caches files inside the `tmp` folder.
- **The Fix**: Restart JBoss and clear your browser cache (Ctrl + F5).
