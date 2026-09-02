# OpenAI Tunnel Client & Local MCP Agent Setup Guide

This guide provides step-by-step instructions to configure, launch, and connect the OpenAI `tunnel-client` (local agent) to expose local Model Context Protocol (MCP) servers securely to ChatGPT without exposing public ingress ports.

---

## 📋 Table of Contents
1. [Prerequisites & Platform Setup](#1-prerequisites--platform-setup)
2. [Install the Tunnel Client](#2-install-the-tunnel-client)
3. [Configuration & Environment Setup](#3-configuration--environment-setup)
4. [Running Diagnostic Checks](#4-running-diagnostic-checks)
5. [Launching the Local Agent Daemon](#5-launching-the-local-agent-daemon)
6. [Connecting from the ChatGPT UI](#6-connecting-from-the-chatgpt-ui)
7. [Troubleshooting Common Issues](#7-troubleshooting-common-issues)

---

## 1. Prerequisites & Platform Setup

1. Open **[OpenAI Platform Settings > Tunnels](https://platform.openai.com/settings/organization/tunnels)**.
2. Go to **Organization > Tunnels** and create a new tunnel. Copy the generated `CONTROL_PLANE_TUNNEL_ID`.
3. Go to **API Keys** and create an API key with permissions to read/use the tunnel. Save this as your `CONTROL_PLANE_API_KEY`.
4. Ensure your target local MCP server is running on your machine (e.g., an HTTP server on `http://localhost:8000` or a STDIO-based local script).

---

## 2. Install the Tunnel Client

### Via Homebrew (macOS / Linux)
```bash
brew install openai/tools/tunnel-client
```

### Manual / Direct Download
Download the latest binary release directly from the official repository:
- **Repository:** `openai/tunnel-client`

Verify the installation:
```bash
tunnel-client --version
```

---

## 3. Configuration & Environment Setup

### Option A: Set Environment Variables (Foreground Run)
```bash
# Control Plane Credentials
export CONTROL_PLANE_API_KEY="your_api_key_here"
export CONTROL_PLANE_TUNNEL_ID="your_tunnel_id_here"

# Specify Local Target MCP Server
export MCP_SERVER_URL="http://localhost:8000"
```

### Option B: Save Profile Configuration (Managed Agent Run)
```bash
tunnel-client config set   --tunnel-id "your_tunnel_id_here"   --api-key "your_api_key_here"   --mcp-url "http://localhost:8000"
```

*Note:* If using a STDIO-based script instead of an HTTP server, supply `--mcp-command` (e.g., `node`) and `--mcp-args` (e.g., `dist/index.js`).

---

## 4. Running Diagnostic Checks

Before launching the tunnel daemon, run the diagnostic suite to verify network connectivity, control plane authentication, and local server availability:

```bash
tunnel-client doctor --explain
```

For profile-based diagnostics:
```bash
tunnel-client doctor --profile --explain
```

Ensure all health checks pass cleanly.

---

## 5. Launching the Local Agent Daemon

### Foreground Mode (For Debugging & Monitoring)
```bash
tunnel-client run
```

### Background Service / Managed Agent Mode
Start the background supervisor:
```bash
tunnel-client runtimes connect
```

Check supervisor status:
```bash
tunnel-client runtimes status
```

Stop the agent:
```bash
tunnel-client runtimes disconnect
```

### Local Health & Monitoring Endpoints
- **Health Check:** `http://localhost:8080/readyz`
- **Management UI:** `http://localhost:8080/ui#overview`

---

## 6. Connecting from the ChatGPT UI

1. Open **[ChatGPT](https://chatgpt.com)** and log into your account.
2. Click on your **Profile Picture / Name** (lower-left corner) $ightarrow$ **Settings**.
3. Navigate to **Apps** (or **Connectors / Integrations / Connected Apps**).
4. Ensure **Developer Mode** or **Custom MCP Connectors** is toggled **ON**.
5. Click **Add New Server** (or **Connect MCP Server**).
6. Fill in the connection details:
   - **Name:** `My Local MCP Agent` (or preferred name)
   - **Server URL:** `https://tunnel-service.gateway.unified-0.internal.api.openai.org/v1/mcp/tunnel_<YOUR_TUNNEL_ID>`
   - **Authentication Type:** Select **None** (or **No Auth**). *Do not select OAuth 2.0.*
7. Click **Save & Verify**.
8. Open a **New Chat**, click the **`+` (Tools & Apps)** icon in the prompt window, and check/enable your local connector.

---

## 7. Troubleshooting Common Issues

### ❌ Error: `Error fetching OAuth configuration ... does not implement OAuth`
- **Cause:** ChatGPT is configured to use OAuth authentication, but local MCP servers generally do not host OAuth discovery endpoints.
- **Fix:** Edit the connector settings in ChatGPT and switch **Authentication Type** to **None** (or **No Auth**).

### ❌ Error: `Connection Refused` / Host Unreachable
- **Docker Setup:** If running `tunnel-client` inside a container, `localhost` resolves to the container's isolated loopback network. Use `host.docker.internal` (macOS/Windows) or `172.17.0.1` (Linux) as your host target:
  ```bash
  export MCP_SERVER_URL="http://host.docker.internal:8000"
  ```
- Verify the local server is actively listening on your host machine:
  ```bash
  curl -I http://localhost:8000
  ```

### ❌ Invisible Settings Page
- Ensure Developer Mode is enabled under **Settings > Security & Login** or **Settings > Advanced**.
- Verify that your organization/workspace admin hasn't restricted developer features.
