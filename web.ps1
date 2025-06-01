# Web Interface Launcher for Object Detection
# Starts a local web server for easy GUI access

param(
    [Parameter(Mandatory=$false)]
    [string]$Host = "127.0.0.1",
    
    [Parameter(Mandatory=$false)]
    [int]$Port = 5000,
    
    [Parameter(Mandatory=$false)]
    [switch]$Debug,
    
    [Parameter(Mandatory=$false)]
    [switch]$OpenBrowser,
    
    [Parameter(Mandatory=$false)]
    [switch]$Help
)

function Show-Help {
    Write-Host @"

🌐 Object Detection Web Interface
===============================

DESCRIPTION:
    Launch a local web server for easy object detection through a browser interface.
    
    Features:
    - 📤 Upload images/videos for detection
    - 📷 Camera capture and detection
    - 🔧 Model management and selection
    - 📊 Real-time results display
    - 🎛️ Adjustable confidence settings

USAGE:
    .\web.ps1 [options]

EXAMPLES:
    # Start web interface (default settings)
    .\web.ps1

    # Start with custom host and port
    .\web.ps1 -Host "0.0.0.0" -Port 8080

    # Start in debug mode and open browser
    .\web.ps1 -Debug -OpenBrowser

    # Start with public access (accessible from other devices)
    .\web.ps1 -Host "0.0.0.0" -Port 5000

PARAMETERS:
    -Host         Host to bind to (default: "127.0.0.1")
    -Port         Port to bind to (default: 5000)
    -Debug        Enable debug mode with detailed logging
    -OpenBrowser  Automatically open web browser
    -Help         Show this help message

ACCESS:
    Local:    http://127.0.0.1:5000
    Network:  http://[your-ip]:5000 (if Host is 0.0.0.0)

REQUIREMENTS:
    - Virtual environment must be set up (run setup.ps1 first)
    - Flask package will be installed automatically if missing

"@
}

if ($Help) {
    Show-Help
    exit 0
}

# Check if virtual environment exists
if (-not (Test-Path "venv")) {
    Write-Host "❌ Virtual environment not found. Please run setup.ps1 first." -ForegroundColor Red
    exit 1
}

# Activate virtual environment
Write-Host "🔧 Activating virtual environment..." -ForegroundColor Blue
& "venv\Scripts\Activate.ps1"

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to activate virtual environment" -ForegroundColor Red
    exit 1
}

# Check and install Flask if needed
Write-Host "📦 Checking Flask installation..." -ForegroundColor Blue
$flaskCheck = python -c "import flask; print('installed')" 2>$null

if ($flaskCheck -ne "installed") {
    Write-Host "📦 Installing Flask..." -ForegroundColor Yellow
    pip install flask
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Failed to install Flask" -ForegroundColor Red
        exit 1
    }
}
    }
}

# Prepare arguments
$pythonArgs = @(
    "web_interface.py"
    "--host", $Host
    "--port", $Port.ToString()
)

if ($Debug) {
    $pythonArgs += "--debug"
}

# Display configuration
Write-Host ""
Write-Host "🌐 Starting Object Detection Web Interface" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Green
Write-Host "🔗 Host: $Host" -ForegroundColor Cyan
Write-Host "🔌 Port: $Port" -ForegroundColor Cyan
Write-Host "🌍 URL: http://$Host`:$Port" -ForegroundColor Cyan

if ($Debug) {
    Write-Host "🐛 Debug Mode: Enabled" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "📱 Features Available:" -ForegroundColor White
Write-Host "  • Upload images/videos for detection" -ForegroundColor Gray
Write-Host "  • Camera capture and live detection" -ForegroundColor Gray
Write-Host "  • Model selection and management" -ForegroundColor Gray
Write-Host "  • Adjustable confidence thresholds" -ForegroundColor Gray
Write-Host "  • Real-time results display" -ForegroundColor Gray
Write-Host ""

# Open browser if requested
if ($OpenBrowser) {
    Write-Host "🌐 Opening web browser..." -ForegroundColor Blue
    Start-Process "http://$Host`:$Port"
}

Write-Host "🚀 Starting web server..." -ForegroundColor Green
Write-Host "   (Press Ctrl+C to stop)" -ForegroundColor Gray
Write-Host ""

# Start the web server
try {
    python @pythonArgs
} catch {
    Write-Host "❌ Error starting web interface: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "✅ Web interface stopped." -ForegroundColor Green
