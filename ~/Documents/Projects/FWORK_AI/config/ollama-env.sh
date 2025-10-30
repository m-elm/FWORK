#!/bin/bash

# 🤖 FWORK_AI Ollama Environment Configuration
# This script configures Ollama to use the FWORK_AI directory structure

# Get the absolute path to FWORK_AI directory
FWORK_AI_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# Set Ollama environment variables
export OLLAMA_MODELS="$FWORK_AI_DIR/models/ollama"
export OLLAMA_HOST="127.0.0.1:11434"
export OLLAMA_LOGS="$FWORK_AI_DIR/logs"

# Set additional environment variables for organization
export FWORK_AI_ROOT="$FWORK_AI_DIR"
export FWORK_AI_CACHE="$FWORK_AI_DIR/cache"
export FWORK_AI_CONFIG="$FWORK_AI_DIR/config"

# Create necessary directories if they don't exist
mkdir -p "$OLLAMA_MODELS"
mkdir -p "$OLLAMA_LOGS"
mkdir -p "$FWORK_AI_CACHE"

echo "🤖 FWORK_AI Ollama Environment Configured"
echo "📁 FWORK_AI Root: $FWORK_AI_ROOT"
echo "🗂️  Models Path: $OLLAMA_MODELS"
echo "📋 Logs Path: $OLLAMA_LOGS"
echo "🔧 Host: $OLLAMA_HOST"

# Function to start Ollama service
start_ollama() {
    echo "🚀 Starting Ollama service..."
    
    # Check if Ollama is already running
    if pgrep -x "ollama" > /dev/null; then
        echo "✅ Ollama is already running"
    else
        # Start Ollama in background
        nohup ollama serve > "$OLLAMA_LOGS/ollama.log" 2>&1 &
        echo $! > "$FWORK_AI_ROOT/.ollama_pid"
        
        # Wait a moment for service to start
        sleep 2
        
        if pgrep -x "ollama" > /dev/null; then
            echo "✅ Ollama service started successfully"
        else
            echo "❌ Failed to start Ollama service"
            return 1
        fi
    fi
}

# Function to stop Ollama service
stop_ollama() {
    echo "🛑 Stopping Ollama service..."
    
    # Stop using PID file if it exists
    if [ -f "$FWORK_AI_ROOT/.ollama_pid" ]; then
        kill $(cat "$FWORK_AI_ROOT/.ollama_pid") 2>/dev/null
        rm "$FWORK_AI_ROOT/.ollama_pid"
        echo "✅ Ollama service stopped"
    else
        # Fallback to killing all ollama processes
        pkill -x "ollama" 2>/dev/null
        echo "✅ Ollama processes terminated"
    fi
}

# Function to check Ollama status
check_ollama_status() {
    echo "🔍 Ollama Status Check"
    echo "====================="
    
    if pgrep -x "ollama" > /dev/null; then
        echo "✅ Ollama service: Running"
        echo "🗂️  Models directory: $OLLAMA_MODELS"
        echo "📋 Log file: $OLLAMA_LOGS/ollama.log"
        
        # Show available models
        echo ""
        echo "📦 Available models:"
        ollama list 2>/dev/null || echo "  No models installed yet"
        
        # Show disk usage
        echo ""
        echo "💾 Storage usage:"
        du -sh "$OLLAMA_MODELS" 2>/dev/null || echo "  No models directory yet"
    else
        echo "❌ Ollama service: Not running"
        echo "💡 Run 'start_ollama' to start the service"
    fi
}

# Create convenient aliases
alias ollama-start='start_ollama'
alias ollama-stop='stop_ollama'
alias ollama-status='check_ollama_status'
alias ollama-logs='tail -f "$OLLAMA_LOGS/ollama.log"'

echo ""
echo "🎯 Available commands:"
echo "  ollama-start   - Start Ollama service"
echo "  ollama-stop    - Stop Ollama service"  
echo "  ollama-status  - Check service status"
echo "  ollama-logs    - View service logs"
echo "  ollama pull    - Download models"
echo "  ollama run     - Chat with models"
echo ""
echo "💡 Run 'ollama-start' to begin!" 