# Minute-Level Integration Guide (JBoss + Windows)

This guide provides every single step needed to move from zero to production.

## Phase 1: Server Environment Preparation
1.  **Install Python**: Download Python 3.10+ from python.org. During installation, **check the box "Add Python to PATH"**.
2.  **Create Folder**: Create a directory `C:\Services\Chatbot` and copy all project files there.
3.  **PDFs**: Copy your 5 PDFs into `C:\Services\Chatbot\backend\data\`.

## Phase 2: Backend & FAQ Configuration
1.  **Manage Your FAQ**: 
    - Open `backend/faq.json`. 
    - Add or edit your questions/answers.
2.  **First Run (Build) / Daily Start**:
    - Double-click **`run_windows.bat`**. 
    - **Note**: The first run will install dependencies (slow). Subsequent runs will skip this and start the server instantly (fast).
3.  **Updating Dependencies**:
    - If you ever change `requirements.txt`, run **`update_windows.bat`** to refresh your environment.

## Phase 3: Making it a Windows Service (Always Running)
1.  Download **NSSM** (nssm.cc) and extract `nssm.exe` to `C:\Services\Chatbot`.
2.  Open **Command Prompt as Administrator**.
3.  Type: `C:\Services\Chatbot\nssm.exe install ChatbotService`
4.  In the popup:
    - **Path**: `C:\Services\Chatbot\run_windows.bat`
    - **Startup directory**: `C:\Services\Chatbot`
5.  Go to **Windows Services** (services.msc), find `ChatbotService`, and click **Start**.

## Phase 4: JBoss Seamless Integration
### Step 1: Reverse Proxy (standalone.xml)
Open your JBoss `standalone.xml` (usually in `bin/standalone/configuration/`).
1.  Find the `<subsystem xmlns="urn:jboss:domain:undertow:...">` section.
2.  Inside `<server name="default-server">`, find your `<host name="default-host" ...>`.
3.  Add this handler **above** your existing deployments:
    ```xml
    <filter-ref name="chatbot-proxy" predicate="path-prefix(/chatbot-api)"/>
    ```
4.  Find the `<filters>` section in the same subsystem and add:
    ```xml
    <reverse-proxy name="chatbot-proxy">
        <host name="chatbot-backend" outbound-socket-binding="chatbot-api-socket" path="/"/>
    </reverse-proxy>
    ```
5.  Find the `<socket-binding-group>` section at the end of the file and add:
    ```xml
    <outbound-socket-binding name="chatbot-api-socket">
        <remote-destination host="127.0.0.1" port="8000"/>
    </outbound-socket-binding>
    ```

### Step 2: Global Script Injection (index.jsp)
Since your `index.jsp` is inside a `.war` file, follow these steps:

1.  **Place the files**: Copy `chatbot-widget.js` and `chatbot-widget.css` into a directory that your web app can see (e.g., your app's `js` and `css` folders, or a global folder).
2.  **Edit index.jsp**: Use this exact placement:

```jsp
<html>
<head>
    <link rel="stylesheet" href="css/chatbot-widget.css"> <!-- 1. ADD CSS HERE -->
    <meta ...>
</head>
<body>
    <!-- Your existing content -->

    <script src="js/chatbot-widget.js"></script> <!-- 2. ADD JS HERE (Just before </body>) -->
</body>
</html>
```

3.  **Deployment**: 
    - If your JBoss is using "exploded" deployments, you can edit the file directly in `standalone/deployments/yourapp.war/index.jsp`.
    - If it's a zipped `.war`, you will need to update the file and re-deploy.

## Phase 5: Final Validation
1.  Restart JBoss.
2.  Visit `http://yourserver/chatbot-api/health`. It should return `{"status":"ok"}`.
3.  Visit your app; the blue bubble should appear!

---

## 🛠️ Troubleshooting & Common Issues

### 1. "Mixed Content" Error (HTTPS)
- **Problem**: Your JBoss site is on `https://` but the chatbot is on `http://`.
- **Solution**: Use the **JBoss Reverse Proxy** (Section 4B). This makes the chatbot share the same HTTPS certificate as your main site.

### 2. "Connection Refused"
- **Check 1**: Is `run_windows.bat` open or is the Windows Service started?
- **Check 2**: Is Port 8000 open in the Windows Firewall? 
- **Check 3**: If JBoss and the Chatbot are on different servers, update `API_URL` to the correct IP in `chatbot-widget.js`.

### 3. "No Documents Found"
- **Solution**: Ensure your PDFs are inside `backend/data/`. Note: Desktop hidden files (starting with `.~`) are ignored.

### 4. Port 8000 is occupied
- **Solution**: Change `8000` to `8001` in both `run_windows.bat` and `standalone.xml`.
