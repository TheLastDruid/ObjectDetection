#!/usr/bin/env pwsh
# Fast Web Interface Launch Script

param(
    [switch]$OpenBrowser,
    [switch]$Production,
    [int]$Port = 5000,
    [switch]$Help
)

if ($Help) {
    Write-Host "Fast Web Interface Launcher" -ForegroundColor Green
    Write-Host "Usage:"
    Write-Host "  .\fast_web.ps1                    # Launch web interface"
    Write-Host "  .\fast_web.ps1 -OpenBrowser       # Launch and open browser"
    Write-Host "  .\fast_web.ps1 -Production        # Production mode"
    Write-Host "  .\fast_web.ps1 -Port 8080         # Custom port"
    return
}

Write-Host "Fast Object Detection Web Interface" -ForegroundColor Green

# Check virtual environment
if (-not (Test-Path "venv\Scripts\python.exe")) {
    Write-Host "ERROR: Virtual environment not found. Run setup.ps1 first." -ForegroundColor Red
    return
}

# Set environment
if ($Production) {
    $env:FLASK_ENV = "production"
    $env:FLASK_DEBUG = "0"
    Write-Host "Production mode enabled" -ForegroundColor Green
} else {
    $env:FLASK_ENV = "development"
    $env:FLASK_DEBUG = "1"
    Write-Host "Development mode enabled" -ForegroundColor Cyan
}

$env:PYTHONUNBUFFERED = "1"

Write-Host "Starting web server on port $Port..." -ForegroundColor Cyan

if ($OpenBrowser) {
    Write-Host "Browser will open automatically..." -ForegroundColor Yellow
    Start-Process powershell -ArgumentList "-Command", "Start-Sleep 3; Start-Process 'http://localhost:$Port'" -WindowStyle Hidden
}

Write-Host "Access at: http://localhost:$Port" -ForegroundColor Yellow
Write-Host "Press Ctrl+C to stop"
Write-Host ""

# Activate venv and start web interface
& ".\venv\Scripts\python.exe" "web_interface.py"

Write-Host "Web interface stopped." -ForegroundColor Green
