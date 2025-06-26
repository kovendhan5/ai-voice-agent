@echo off
echo.
echo ================================
echo   OPENVOICE SETUP FOR ORPHEUS
echo ================================
echo.

echo Installing OpenVoice dependencies...
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cpu
pip install librosa soundfile numpy scipy matplotlib
pip install Pillow inflect phonemizer Unidecode
pip install cn2an pypinyin jieba langid-py gradio

echo.
echo Installing OpenVoice from GitHub...
pip install git+https://github.com/myshell-ai/OpenVoice.git

echo.
echo Installing MeloTTS...
pip install git+https://github.com/myshell-ai/MeloTTS.git

echo.
echo Downloading language models...
python -m unidic download

echo.
echo Running OpenVoice setup script...
python scripts/setup_openvoice.py

echo.
echo ================================
echo   SETUP COMPLETE!
echo ================================
echo.
echo To test the system:
echo   python src/app_live_orpheus.py
echo.
echo The system will automatically detect and use:
echo   - Real OpenVoice if available
echo   - Edge TTS as fallback
echo.
pause
