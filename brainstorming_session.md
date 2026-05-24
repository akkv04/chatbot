# Chatbot Project - Brainstorming & Technical Session

This document captures the brainstorming, design decisions, and implementation details for the Chatbot project.

## 🗓️ Session Date: 2026-05-24

### 1. Initial Requirements
- **Goal**: Create a simple, appealing chatbot for a JBoss-hosted webpage.
- **Features**: Answer based on predefined questions and reference PDFs (up to 5).
- **Environment**: Windows Server (co-hosted with JBoss).

### 2. Architecture Selection
After discussing 3 options (Widget, Iframe, JBoss-Native), we selected the **Widget Approach**:
- **Frontend**: Standalone Vanilla JS/CSS floating widget.
- **Backend**: Python FastAPI service for AI logic.
- **Integration**: Single script tag injection.

### 3. Technical Decisions
- **LLM**: Multi-provider support (Google Gemini 1.5 Pro and OpenAI GPT-4o).
- **RAG**: Retrieval-Augmented Generation using `LangChain` and `ChromaDB`.
- **Windows Hosting**: 
    - `run_windows.bat` for automatic environment setup.
    - `run_hidden.vbs` for silent background operation.
    - NSSM recommended for Windows Service hosting.
- **JBoss Integration**: 
    - Use `standalone.xml` for reverse proxying to solve CORS/SSL.
    - Centralize API URL in `jboss.properties`.

### 4. Implementation Steps
- [x] Backend implementation (FastAPI + RAG logic).
- [x] Frontend widget development (Floating bubble + chat window).
- [x] Windows compatibility enhancements.
- [x] Multi-provider support (OpenAI/Google).
- [x] Extensive testing and browser verification.
- [x] Detailed "Minute-Level" integration guide for JBoss.

### 5. Repository Setup
- **GitHub**: [github.com/akkv04/chatbot](https://github.com/akkv04/chatbot)
- **Git Config**: Included `.gitignore` to protect `.env` and PDF data.

---
*End of Session Summary*
