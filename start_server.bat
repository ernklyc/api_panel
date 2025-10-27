@echo off
echo ============================================================
echo Movie Face AI - API Key Manager
echo ============================================================
echo.
echo 1. Initializing API Keys...
python initialize_api_keys.py
echo.
echo 2. Starting server...
python api_key_manager.py

