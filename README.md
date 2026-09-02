# MCP Server start
python3 -m venv .venv && source .venv/bin/activate   # optional but recommended
pip install -r requirements.txt
python mcp-server.py

# Tunnel setup
Follow the Tunnel setup guide to setup tunnel for localhost
[Read Setup Guide](./OPENAI-TUNNEL-SETUP.md)

