#!/bin/bash
# Start Yogacara Chat Server

export FLASK_APP=app.py
export FLASK_DEBUG=true
export PORT=${PORT:-5000}

echo "Starting Yogacara Chat Server on port $PORT"
echo "API Key configured: $([ -n \"$OPENAI_API_KEY\" ] && echo 'Yes' || echo 'No')"

pip install -e ".[server]" > /dev/null 2>&1

python app.py
