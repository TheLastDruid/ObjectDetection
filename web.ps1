# Web Interface Launcher for Object Detection
param(
    [string]$HostIP = "127.0.0.1",
    [int]$Port = 5000,
    [switch]$Debug,
    [switch]$OpenBrowser,
    [switch]$Help
)

if ($Help) {
    Write-Host "Object Detection Web Interface Launcher"
    Write-Host "Usage: .\web.ps1 [-HostIP 127.0.0.1] [-Port 5000] [-Debug] [-OpenBrowser] [-Help]"
    Write-Host ""
    Write-Host "Examples:"
    Write-Host "  .\web.ps1                    # Start with default settings"
    Write-Host "  .\web.ps1 -OpenBrowser       # Start and open browser"
    Write-Host "  .\web.ps1 -Debug             # Start in debug mode"
    Write-Host "  .\web.ps1 -Port 8080         # Use custom port"
    exit 0
}

# Check if virtual environment exists
if (-not (Test-Path "venv")) {
    Write-Host "Virtual environment not found. Please run setup.ps1 first." -ForegroundColor Red
    exit 1
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Blue
& "venv\Scripts\Activate.ps1"

# Check Flask installation
Write-Host "Checking Flask installation..." -ForegroundColor Blue
$flaskInstalled = python -c "import flask; print('OK')" 2>$null
if ($flaskInstalled -ne "OK") {
    Write-Host "Installing Flask..." -ForegroundColor Yellow
    pip install flask
}

# Prepare Python arguments
$pythonArgs = @("web_interface.py", "--host", $HostIP, "--port", $Port.ToString())
if ($Debug) {
    $pythonArgs += "--debug"
}

# Display configuration
Write-Host ""
Write-Host "Starting Object Detection Web Interface" -ForegroundColor Green
Write-Host "Host: $HostIP" -ForegroundColor Cyan
Write-Host "Port: $Port" -ForegroundColor Cyan
Write-Host "URL: http://$HostIP`:$Port" -ForegroundColor Cyan
if ($Debug) {
    Write-Host "Debug Mode: Enabled" -ForegroundColor Yellow
}
Write-Host ""

# Open browser if requested
if ($OpenBrowser) {
    Write-Host "Opening web browser in 3 seconds..." -ForegroundColor Blue
    Start-Job -ScriptBlock {
        Start-Sleep -Seconds 3
        Start-Process "http://127.0.0.1:5000"
    } | Out-Null
}

Write-Host "Starting web server..." -ForegroundColor Green
Write-Host "(Press Ctrl+C to stop)" -ForegroundColor Gray
Write-Host ""

# Start the web server
try {
    python @pythonArgs
} catch {
    Write-Host "Error starting web interface: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Web interface stopped." -ForegroundColor Green
