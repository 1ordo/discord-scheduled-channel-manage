@echo off
REM Discord Scheduled Channel Manager Bot - Quick Start Script for Windows
REM This script helps you get the bot running quickly on Windows

echo 🚀 Discord Scheduled Channel Manager Bot - Quick Start
echo ======================================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.8 or higher.
    echo Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Check Python version
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set python_version=%%i
echo ✅ Python version: %python_version%

REM Create virtual environment if it doesn't exist
if not exist venv (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo 🔄 Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo ⬆️ Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies
echo 📦 Installing dependencies...
pip install -r requirements.txt

REM Create configuration file if it doesn't exist
if not exist configuration.env (
    echo 📝 Creating configuration file...
    copy configuration.env.template configuration.env > nul
    
    echo.
    echo ⚠️ IMPORTANT: Please edit configuration.env and add your Discord bot token!
    echo.
    
    REM Prompt for bot token
    set /p "answer=Do you want to enter your bot token now? (y/N): "
    if /i "%answer%"=="y" (
        set /p "bot_token=Enter your Discord bot token: "
        if not "!bot_token!"=="" (
            powershell -Command "(gc configuration.env) -replace 'your_discord_bot_token_here', '!bot_token!' | Out-File -encoding ASCII configuration.env"
            echo ✅ Bot token configured!
        )
    )
    
    REM Prompt for timezone
    set /p "timezone=Enter your timezone (default: America/New_York): "
    if not "%timezone%"=="" (
        powershell -Command "(gc configuration.env) -replace 'America/New_York', '%timezone%' | Out-File -encoding ASCII configuration.env"
        echo ✅ Timezone configured!
    )
)

REM Test configuration
echo 🧪 Testing configuration...
python -c "try:
    from configuration import BOT_TOKEN, TIMEZONE
    if BOT_TOKEN == 'your_discord_bot_token_here':
        print('⚠️ Warning: Default bot token detected. Please update configuration.env')
    else:
        print('✅ Configuration loaded successfully')
    print(f'🌍 Timezone: {TIMEZONE}')
except Exception as e:
    print(f'❌ Configuration error: {e}')
    exit(1)"

if errorlevel 1 (
    echo Configuration test failed!
    pause
    exit /b 1
)

REM Test database
echo 🗄️ Testing database...
python -c "try:
    from database import database
    database.connect()
    database.create_table()
    database.close()
    print('✅ Database initialized successfully')
except Exception as e:
    print(f'❌ Database error: {e}')
    exit(1)"

if errorlevel 1 (
    echo Database test failed!
    pause
    exit /b 1
)

echo.
echo 🎉 Setup completed successfully!
echo.
echo Next steps:
echo 1. Make sure your bot token is set in configuration.env
echo 2. Invite your bot to your Discord server with appropriate permissions
echo 3. Run the bot with: python main.py
echo.
echo Required Discord permissions:
echo - Read Messages
echo - Send Messages
echo - Manage Channels
echo - View Channels
echo - Manage Roles (if using role-based permissions)
echo.
echo For more information, see README.md
echo.

REM Ask if user wants to start the bot now
set /p "answer=Do you want to start the bot now? (y/N): "
if /i "%answer%"=="y" (
    echo 🚀 Starting the bot...
    python main.py
) else (
    echo To start the bot later, run: python main.py
    pause
)
