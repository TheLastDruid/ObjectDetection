# Run script for Object Detection project
# This script activates the virtual environment and runs the object detection

param(
    [string]$ImagePath = "input/sample.jpg",
    [switch]$SaveAnnotated,
    [switch]$SaveJson,
    [switch]$CountObjects,
    [string]$ModelPath = "models/yolov8n.pt",
    [switch]$Camera,
    [switch]$LiveCamera,
    [int]$CameraIndex = 0,
    [switch]$Display
)

Write-Host "Running Object Detection..." -ForegroundColor Green

# Check if virtual environment exists
if (-not (Test-Path "venv")) {
    Write-Host "Virtual environment not found. Please run setup.ps1 first." -ForegroundColor Red
    exit 1
}

# Activate virtual environment
& ".\venv\Scripts\Activate.ps1"

# Build command arguments
$args = @("main.py")

# Camera modes
if ($Camera) {
    $args += "--camera"
    Write-Host "Using camera capture mode" -ForegroundColor Yellow
} elseif ($LiveCamera) {
    $args += "--live_camera"
    Write-Host "Starting live camera detection mode" -ForegroundColor Yellow
    Write-Host "Press 'q' to quit, 's' to save frame, 'c' to capture frame" -ForegroundColor Cyan
} else {
    $args += @("--image_path", $ImagePath)
}

# Camera index
if ($Camera -or $LiveCamera) {
    $args += @("--camera_index", $CameraIndex)
}

# Model path
if ($ModelPath) {
    $args += @("--model", $ModelPath)
}

# Output options
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
Write-Host "Running: python $($args -join ' ')" -ForegroundColor Cyan
python @args
