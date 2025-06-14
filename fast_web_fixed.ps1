# Fast Web Interface Launch Script
# Optimized for maximum performance

param(
    [switch]$OpenBrowser,
    [switch]$Production,
    [int]$Port = 5000,
    [switch]$Help
)

if ($Help) {
    Write-Host "🚀 Fast Web Interface Launcher" -ForegroundColor Green
    Write-Host "==============================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Usage:" -ForegroundColor Cyan
    Write-Host "  .\fast_web.ps1                    # Launch in development mode"
    Write-Host "  .\fast_web.ps1 -OpenBrowser       # Launch and open browser"
    Write-Host "  .\fast_web.ps1 -Production        # Launch in production mode"
    Write-Host "  .\fast_web.ps1 -Port 8080         # Use custom port"
    Write-Host ""
    Write-Host "Optimizations:" -ForegroundColor Yellow
    Write-Host "  ⚡ GPU acceleration when available"
    Write-Host "  🖼️ Automatic image resizing"
    Write-Host "  📱 Frame skipping for live detection"
    Write-Host "  🗜️ Optimized JPEG compression"
    Write-Host "  💾 Model caching"
    exit 0
}

Write-Host "🚀 Fast Object Detection Web Interface" -ForegroundColor Green
Write-Host "=======================================" -ForegroundColor Green

# Check if virtual environment exists
if (-not (Test-Path "venv")) {
    Write-Host "❌ Virtual environment not found. Please run setup.ps1 first." -ForegroundColor Red
    exit 1
}

# Activate virtual environment
Write-Host "🔧 Activating virtual environment..." -ForegroundColor Cyan
& ".\venv\Scripts\Activate.ps1"

# Check for CUDA availability
Write-Host "🔍 Checking GPU availability..." -ForegroundColor Cyan
try {
    $cudaCheck = python -c "import torch; print(torch.cuda.is_available())" 2>$null
    if ($cudaCheck -eq "True") {
        Write-Host "✅ GPU acceleration available!" -ForegroundColor Green
    } else {
        Write-Host "⚠️  Using CPU (consider GPU for better performance)" -ForegroundColor Yellow
    }
} catch {
    Write-Host "⚠️  Could not check GPU availability" -ForegroundColor Yellow
}

# Set environment variables for optimization
if ($Production) {
    $env:FLASK_ENV = "production"
    $env:FLASK_DEBUG = "0"
    Write-Host "🏭 Production mode: Maximum performance" -ForegroundColor Green
} else {
    $env:FLASK_ENV = "development"
    $env:FLASK_DEBUG = "1"
    Write-Host "🔧 Development mode: Fast reloading" -ForegroundColor Cyan
}

$env:PYTHONUNBUFFERED = "1"

Write-Host "🌐 Starting optimized web server on port $Port..." -ForegroundColor Cyan

if ($OpenBrowser) {
    Write-Host "🌐 Opening browser in 3 seconds..." -ForegroundColor Yellow
    Start-Job -ScriptBlock {
        Start-Sleep -Seconds 3
        Start-Process "http://localhost:$using:Port"
    } | Out-Null
}

# Start the web interface
Write-Host "📱 Access the interface at: http://localhost:$Port" -ForegroundColor Yellow
Write-Host "🔄 Press Ctrl+C to stop the server" -ForegroundColor Gray
Write-Host ""

python web_interface.py

Write-Host ""
Write-Host "✅ Web interface stopped." -ForegroundColor Green
