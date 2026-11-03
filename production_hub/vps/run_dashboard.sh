#!/usr/bin/env bash
# Vismart Media Production Hub — VPS 24/7 Service Runner
set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$DIR"

echo "======================================================="
echo " 🚀 STARTING VISMART AI MEDIA HUB ON VPS"
echo " 🌐 Dashboard will be live at: http://YOUR_VPS_IP:5000"
echo "======================================================="

# Run using pm2 or nohup
if command -v pm2 &> /dev/null; then
    pm2 delete vismart-hub 2>/dev/null || true
    pm2 start "python3 -m uvicorn web.app:app --host 0.0.0.0 --port 5000" --name "vismart-hub"
    pm2 save
    echo "✅ Running 24/7 under PM2 as 'vismart-hub'!"
else
    nohup python3 -m uvicorn web.app:app --host 0.0.0.0 --port 5000 > /var/log/vismart_hub.log 2>&1 &
    echo "✅ Running 24/7 in background (logs at /var/log/vismart_hub.log)!"
fi
