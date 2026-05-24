## 1. Backend Setup (Windows Server)

1.  **Install Python**: Ensure Python 3.9+ is installed on your Windows Server.
2.  **Add Your PDFs**: Place up to 5 PDFs in `backend/data/`.
3.  **Configure LLM Provider**:
    - Copy `.env.example` to `.env`.
    - Set `LLM_PROVIDER` to either `google` (Gemini) or `openai` (GPT).
    - Add the corresponding API Key (`GOOGLE_API_KEY` or `OPENAI_API_KEY`).
4.  **Launch**: Double-click `run_windows.bat`.

## 2. Frontend Integration (JBoss/JSP)

Add this snippet to your HTML/JSP file (usually in `footer.jsp` or before `</body>`):

```html
<!-- Chatbot Styles and Script -->
<link rel="stylesheet" href="path/to/chatbot-widget.css">
<script src="path/to/chatbot-widget.js"></script>
```

> [!IMPORTANT]
> **API URL**: Open `chatbot-widget.js` and update `const API_URL = "http://your-server-ip:8000";`. If the backend is on the same machine, use the server's actual IP rather than `localhost` to ensure external clients can access it.

## 3. Production & Security on Windows

### Auto-start & Persistence
To ensure your chatbot is always running (even if no user is logged into the server):

1.  **Option A: NSSM (Recommended for Production)**
    - Download [NSSM](https://nssm.cc/download).
    - Open CMD as Administrator and run: `nssm install ChatbotBrain`.
    - In the UI, set **Path** to `cmd.exe` and **Arguments** to `/c run_windows.bat`.
    - Set the **Startup directory** to your `Chatbot` folder.
    - Click **Install Service**. Now it will start/stop like JBoss!

2.  **Option B: Hidden Background Run**
    - Double-click `run_hidden.vbs`. This will start the backend without a visible console window.

3.  **Option C: Windows Task Scheduler**
    - Create a task that triggers "At system startup".
    - Set the action to "Start a program" and point it to `run_windows.bat`.
    - Check "Run whether user is logged on or not".

## 4. Seamless JBoss Integration (Experimental/Advanced)

To integrate the chatbot without modifying every individual application file, use these JBoss-native methods.

### A. Centralizing URL in `jboss.properties`
Add this line to your `jboss.properties` file:
```properties
chatbot.api.url=http://your-server-ip:8000
```
This allows you to change the backend URL in one place for all environments.

### B. Reverse Proxy in `standalone.xml` (Best for Prod)
This removes CORS issues by making the Chatbot API appear as part of your JBoss site (e.g., `yourapp.com/chatbot-api`).

Under the `<subsystem xmlns="urn:jboss:domain:undertow:...">` section, add a reverse proxy handler:

```xml
<handlers>
    <reverse-proxy name="chatbot-proxy">
        <host name="chatbot-backend" outbound-socket-binding="chatbot-api-socket" path="/"/>
    </reverse-proxy>
</handlers>
<filters>
    <filter-ref name="chatbot-proxy" predicate="path-prefix(/chatbot-api)"/>
</filters>
```

And add the socket binding at the end of `standalone.xml`:
```xml
<outbound-socket-binding name="chatbot-api-socket">
    <remote-destination host="${chatbot.api.host}" port="8000"/>
</outbound-socket-binding>
```

### C. Global Script Injection (All Pages)
To inject the script into **every page** served by JBoss:

1.  **Filter Method**: If you use a custom Global Filter (Valve) in JBoss, you can intercept the response and append the chatbot `<script>` tag just before `</body>`.
2.  **Static Content Inclusion**: If your JBoss setup has a shared "header/footer" static directory, place the `chatbot-widget.js` there and update your master template.

---

## 🛡️ Minimal Risk Deployment Strategy
1.  **Test Environment**: Deploy the Python backend on a test port (e.g., 8001).
2.  **Manual Check**: Add the script to a single test JSP first.
3.  **Global Rollout**: Once verified, apply the `standalone.xml` proxy and global injection.
