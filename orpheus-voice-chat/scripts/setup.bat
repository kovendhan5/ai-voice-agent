@echo off
echo ================================================
echo 🔧 Setting up Orpheus Voice Chat Environment
echo ================================================

cd /d "%~dp0\.."
echo 📁 Working directory: %cd%

echo.
echo 🐍 Setting up Python virtual environment...
if not exist "venv" (
    echo Creating new virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ❌ Failed to create virtual environment
        pause
        exit /b 1
    )
    echo ✅ Virtual environment created
) else (
    echo ✅ Virtual environment already exists
)

echo.
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ❌ Failed to activate virtual environment
    pause
    exit /b 1
)

echo.
echo 📦 Upgrading pip...
python -m pip install --upgrade pip
if errorlevel 1 (
    echo ⚠️ Pip upgrade failed, continuing anyway...
)

echo.
echo 📋 Installing core dependencies (step by step)...

echo Installing Flask...
pip install flask==3.0.0
if errorlevel 1 (
    echo ❌ Failed to install Flask
    pause
    exit /b 1
)

echo Installing Flask-CORS...
pip install flask-cors==4.0.0
if errorlevel 1 (
    echo ❌ Failed to install Flask-CORS
    pause
    exit /b 1
)

echo Installing requests...
pip install requests==2.31.0
if errorlevel 1 (
    echo ❌ Failed to install requests
    pause
    exit /b 1
)

echo Installing numpy...
pip install numpy==1.24.3
if errorlevel 1 (
    echo ⚠️ Failed to install specific numpy version, trying latest...
    pip install numpy
)

echo Installing PyTorch (this may take a while)...
pip install torch==2.0.1 torchaudio==2.0.2 --index-url https://download.pytorch.org/whl/cpu
if errorlevel 1 (
    echo ⚠️ Failed to install specific PyTorch version, trying latest CPU version...
    pip install torch torchaudio --index-url https://download.pytorch.org/whl/cpu
    if errorlevel 1 (
        echo ⚠️ PyTorch installation failed, continuing without it...
    )
)

echo.
echo 🎭 Installing Orpheus TTS (optional - may fail)...
pip install orpheus-speech
if errorlevel 1 (
    echo ⚠️ Orpheus TTS installation failed
    echo 📝 Server will run in mock mode (silent audio)
    echo 💡 You can try manual installation later:
    echo    pip install orpheus-speech
) else (
    echo ✅ Orpheus TTS installed successfully!
)

echo.
echo ✅ Setup complete!
echo 📋 Installation summary:
echo    • Flask: ✅ Required for web server
echo    • Flask-CORS: ✅ Required for API access
echo    • Requests: ✅ Required for HTTP requests
echo    • NumPy: ✅ Required for audio processing
echo    • PyTorch: ⚠️ Check above for status
echo    • Orpheus TTS: ⚠️ Check above for status
echo.
echo 🚀 To start the server, run: scripts\start.bat
echo 🌐 Server will be available at: http://localhost:8080
echo.
echo 💡 Note: If Orpheus TTS failed to install, the server will run
echo    in mock mode with silent audio. This is normal for testing.

pause
