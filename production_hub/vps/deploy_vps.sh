#!/usr/bin/env bash
# ==============================================================================
# VISMART AUTOMATED MEDIA PRODUCTION HUB — 1-CLICK VPS DEPLOYMENT
# Target OS: Ubuntu 22.04 / 24.04 LTS or Debian 12
# Zero-Cost Setup: FFmpeg, Python Edge-TTS, Node.js 22, Remotion Headless Chromium
# ==============================================================================

set -e

echo "=========================================================="
echo "🚀 [1/5] UPDATING SYSTEM PACKAGES & INSTALLING CORE TOOLS"
echo "=========================================================="
sudo apt update && sudo apt upgrade -y
sudo apt install -y curl wget git ffmpeg build-essential python3 python3-pip python3-venv chromium-browser fonts-noto-cjk fonts-deva

echo "=========================================================="
echo "⚡ [2/5] INSTALLING NODE.JS 22 LTS"
echo "=========================================================="
if ! command -v node &> /dev/null; then
    curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
    sudo apt install -y nodejs
fi
node -v
npm -v

echo "=========================================================="
echo "🐍 [3/5] SETTING UP PYTHON VIRTUAL ENVIRONMENT & TTS"
echo "=========================================================="
python3 -m venv /opt/vismart_env
source /opt/vismart_env/bin/activate
pip install --upgrade pip
pip install edge-tts requests fastapi uvicorn pydantic

echo "=========================================================="
echo "🎬 [4/5] INSTALLING REMOTION & CHROMIUM DRIVERS"
echo "=========================================================="
cd /opt
if [ -d "/opt/media_hub" ]; then
    echo "Directory exists. Updating dependencies..."
    cd /opt/media_hub/hindi-reel && npm install
else
    echo "Cloning and preparing workspace..."
    # If deploying from git or copying from local directory
fi

# Set Chromium environment variables for headless rendering
export PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true
export CHROMIUM_PATH=$(which chromium-browser || which chromium)
echo "export CHROMIUM_PATH=$(which chromium-browser || which chromium)" >> ~/.bashrc

echo "=========================================================="
echo "⏰ [5/5] STARTING 24/7 DASHBOARD & BATCH FACTORY SERVICE"
echo "=========================================================="
if ! command -v pm2 &> /dev/null; then
    npm install -g pm2
fi
pm2 start "/opt/vismart_env/bin/python3 -m uvicorn web.app:app --host 0.0.0.0 --port 5000" --name "vismart-hub" --cwd "/opt/media_hub/production_hub"
pm2 save

# Cron Job: Hourly check to ensure batch worker is churning
CRON_JOB="0 * * * * curl -s -X POST http://127.0.0.1:5000/api/batch/start >> /var/log/vismart_cron.log 2>&1"
(crontab -l 2>/dev/null | grep -Fv "api/batch/start" ; echo "$CRON_JOB") | crontab -

echo "=========================================================="
echo "✅ DEPLOYMENT COMPLETE! YOUR VPS IS 100% READY FOR AUTOMATION!"
echo "=========================================================="
