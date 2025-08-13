#!/usr/bin/env bash
set -euo pipefail

# Node tools
npm i -g n8n pnpm

# Project bootstrap
if [ ! -f package.json ]; then
  pnpm init -y
fi

# NPM scripts
jq '.scripts += {
  "n8n:start": "n8n",
  "n8n:import": "n8n import:workflow --input workflows --separate",
  "n8n:export": "n8n export:workflow --all --output workflows --separate"
}' package.json > package.json.tmp && mv package.json.tmp package.json

# Folders
mkdir -p workflows .vscode

# Env seed
if [ ! -f .env ]; then
  echo "N8N_ENCRYPTION_KEY=$(openssl rand -hex 16)" > .env
  cat >> .env <<'EOF'
# Auth to n8n UI
N8N_BASIC_AUTH_ACTIVE=true
N8N_BASIC_AUTH_USER=admin
N8N_BASIC_AUTH_PASSWORD=change_me

# Platform tokens
AIRTABLE_PERSONAL_ACCESS_TOKEN=
HUBSPOT_API_ACCESS_TOKEN=
SHOPIFY_ADMIN_API_ACCESS_TOKEN=
OPENAI_API_KEY=
EOF
fi

# VS Code settings if missing
if [ ! -f .vscode/settings.json ]; then
  cat > .vscode/settings.json <<'JSON'
{
  "editor.formatOnSave": true,
  "files.insertFinalNewline": true,
  "files.trimTrailingWhitespace": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "editor.tabSize": 2
}
JSON
fi

echo "Post-create complete."
