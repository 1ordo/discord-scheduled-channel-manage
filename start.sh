#!/bin/bash

# Discord Scheduled Channel Manager Bot - Quick Start Script
# This script helps you get the bot running quickly on Unix-like systems

set -e  # Exit on any error

echo "🚀 Discord Scheduled Channel Manager Bot - Quick Start"
echo "======================================================"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check Python version
python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
required_version="3.8"

if ! python3 -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)"; then
    echo "❌ Python 3.8 or higher is required. Current version: $python_version"
    exit 1
fi

echo "✅ Python version: $python_version"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Create configuration file if it doesn't exist
if [ ! -f "configuration.env" ]; then
    echo "📝 Creating configuration file..."
    cp configuration.env.template configuration.env
    
    echo ""
    echo "⚠️  IMPORTANT: Please edit configuration.env and add your Discord bot token!"
    echo ""
    
    # Prompt for bot token
    read -p "Do you want to enter your bot token now? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        read -p "Enter your Discord bot token: " bot_token
        if [ ! -z "$bot_token" ]; then
            sed -i.bak "s/your_discord_bot_token_here/$bot_token/" configuration.env
            echo "✅ Bot token configured!"
        fi
    fi
    
    # Prompt for timezone
    read -p "Enter your timezone (default: America/New_York): " timezone
    if [ ! -z "$timezone" ]; then
        sed -i.bak "s/America\/New_York/$timezone/" configuration.env
        echo "✅ Timezone configured!"
    fi
fi

# Test configuration
echo "🧪 Testing configuration..."
python3 -c "
try:
    from configuration import BOT_TOKEN, TIMEZONE
    if BOT_TOKEN == 'your_discord_bot_token_here':
        print('⚠️  Warning: Default bot token detected. Please update configuration.env')
    else:
        print('✅ Configuration loaded successfully')
    print(f'🌍 Timezone: {TIMEZONE}')
except Exception as e:
    print(f'❌ Configuration error: {e}')
    exit(1)
"

# Test database
echo "🗄️  Testing database..."
python3 -c "
try:
    from database import database
    database.connect()
    database.create_table()
    database.close()
    print('✅ Database initialized successfully')
except Exception as e:
    print(f'❌ Database error: {e}')
    exit(1)
"

echo ""
echo "🎉 Setup completed successfully!"
echo ""
echo "Next steps:"
echo "1. Make sure your bot token is set in configuration.env"
echo "2. Invite your bot to your Discord server with appropriate permissions"
echo "3. Run the bot with: python3 main.py"
echo ""
echo "Required Discord permissions:"
echo "- Read Messages"
echo "- Send Messages"
echo "- Manage Channels"
echo "- View Channels"
echo "- Manage Roles (if using role-based permissions)"
echo ""
echo "For more information, see README.md"
echo ""

# Ask if user wants to start the bot now
read -p "Do you want to start the bot now? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🚀 Starting the bot..."
    python3 main.py
fi
