# Camera script for Object Detection project
# Convenient wrapper for camera-based object detection

param(
    [Parameter(ParameterSetName="capture")]
    [switch]$Capture,
    
    [Parameter(ParameterSetName="live")]
    [switch]$Live,
    
    [int]$CameraIndex = 0,
    [switch]$SaveAnnotated,
    [switch]$SaveJson,
    [switch]$CountObjects,
    [switch]$Display,
    [string]$ModelPath = "models/yolov8n.pt"
)

Write-Host "Camera Object Detection" -ForegroundColor Green

# Check if virtual environment exists
if (-not (Test-Path "venv")) {
    Write-Host "Virtual environment not found. Please run setup.ps1 first." -ForegroundColor Red
    exit 1
}

# Activate virtual environment
& ".\venv\Scripts\Activate.ps1"

if ($Capture) {
    Write-Host "Capturing single photo from camera $CameraIndex..." -ForegroundColor Cyan
    $args = @(
        "main.py",
        "--camera",
        "--camera_index", $CameraIndex,
        "--model", $ModelPath
    )
} elseif ($Live) {
    Write-Host "Starting live camera detection on camera $CameraIndex..." -ForegroundColor Cyan
    Write-Host "Controls:" -ForegroundColor Yellow
    Write-Host "  - Press 'q' to quit" -ForegroundColor White
    Write-Host "  - Press 's' to save current frame (if objects detected)" -ForegroundColor White
    Write-Host "  - Press 'c' to capture current frame" -ForegroundColor White
    $args = @(
        "main.py",
        "--live_camera",
        "--camera_index", $CameraIndex,
        "--model", $ModelPath
    )
} else {
    Write-Host "Please specify either -Capture or -Live mode" -ForegroundColor Red
    Write-Host ""
    Write-Host "Examples:" -ForegroundColor Cyan
    Write-Host "  .\camera.ps1 -Capture -SaveAnnotated -SaveJson -CountObjects" -ForegroundColor White
    Write-Host "  .\camera.ps1 -Live -SaveAnnotated" -ForegroundColor White
    Write-Host "  .\camera.ps1 -Capture -CameraIndex 1 -Display" -ForegroundColor White
    exit 1
}

# Add output options
if ($SaveAnnotated) {
    $args += "--save_annotated"
}

if ($SaveJson) {
    $args += "--save_json"
}

if ($CountObjects) {
    $args += "--count_objects"
}

if ($Display) {
    $args += "--display"
}

# Run the detection
Write-Host "Running: python $($args -join ' ')" -ForegroundColor Gray
python @args

Write-Host "Camera detection completed." -ForegroundColor Green
