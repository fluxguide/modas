#!/bin/sh

# Start crond in the background
crond -b -l 2

# Print the host environment for debugging
echo "Hosts file contents:"
cat /etc/hosts
echo "Attempting to resolve app container"

# Wait for the Streamlit application to be available
while ! nc -z {{COMPOSE_PROJECT_NAME}}-app 8501; do
    echo "Trying to connect to Streamlit app at {{COMPOSE_PROJECT_NAME}}-app:8501..."
    sleep 1
done
echo "Streamlit app is up and running. Starting Nginx..."

# Run nginx in the foreground
exec nginx -g 'daemon off;'
