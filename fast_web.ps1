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
$cudaCheck = python -c "import torch; print('CUDA available:', torch.cuda.is_available())" 2>$null
if ($cudaCheck -match "True") {
    Write-Host "✅ GPU acceleration available!" -ForegroundColor Green
} else {
    Write-Host "⚠️  Using CPU (consider GPU for better performance)" -ForegroundColor Yellow
}

# Set environment variables for optimization
$env:FLASK_ENV = if ($Production) { "production" } else { "development" }
$env:FLASK_DEBUG = if ($Production) { "0" } else { "1" }
$env:PYTHONUNBUFFERED = "1"

Write-Host "🌐 Starting optimized web server on port $Port..." -ForegroundColor Cyan

if ($Production) {
    Write-Host "🏭 Production mode: Maximum performance" -ForegroundColor Green
    # Use Waitress for production
    python -c @"
try:
    from waitress import serve
    from web_interface import app
    print('🚀 Starting production server...')
    serve(app, host='0.0.0.0', port=$Port, threads=4)
except ImportError:
    print('⚠️  Waitress not available, using Flask dev server')
    from web_interface import app
    app.run(host='0.0.0.0', port=$Port, debug=False, threaded=True)
"@
} else {
    Write-Host "🔧 Development mode: Fast reloading" -ForegroundColor Cyan
    if ($OpenBrowser) {
        Start-Sleep -Seconds 2
        Start-Process "http://localhost:$Port"
    }
    python web_interface.py
}

Write-Host ""
Write-Host "✅ Web interface stopped." -ForegroundColor Green
