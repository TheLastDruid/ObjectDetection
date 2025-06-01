# Enhanced run script with model selection
# This script allows easy switching between different YOLOv8 models for better recognition

param(
    [string]$ImagePath = "input/sample.jpg",
    [switch]$SaveAnnotated,
    [switch]$SaveJson,
    [switch]$CountObjects,
    [switch]$Camera,
    [switch]$LiveCamera,
    [int]$CameraIndex = 0,
    [switch]$Display,
    [ValidateSet("nano", "small", "medium", "large", "xlarge", "n", "s", "m", "l", "x")]
    [string]$ModelSize = "nano",
    [string]$CustomModel = "",
    [float]$Confidence = 0.25
)

Write-Host "🔧 Enhanced Object Detection" -ForegroundColor Green

# Model mapping
$modelMap = @{
    "nano" = "yolov8n.pt"
    "n" = "yolov8n.pt"
    "small" = "yolov8s.pt"
    "s" = "yolov8s.pt"
    "medium" = "yolov8m.pt"
    "m" = "yolov8m.pt"
    "large" = "yolov8l.pt"
    "l" = "yolov8l.pt"
    "xlarge" = "yolov8x.pt"
    "x" = "yolov8x.pt"
}

# Determine model to use
if ($CustomModel -ne "") {
    $modelPath = $CustomModel
} else {
    $modelPath = "models/" + $modelMap[$ModelSize]
}

# Model info
$modelInfo = @{
    "yolov8n.pt" = @{ name = "Nano"; size = "6MB"; speed = "Fastest"; accuracy = "Good" }
    "yolov8s.pt" = @{ name = "Small"; size = "22MB"; speed = "Fast"; accuracy = "Better" }
    "yolov8m.pt" = @{ name = "Medium"; size = "52MB"; speed = "Medium"; accuracy = "Very Good" }
    "yolov8l.pt" = @{ name = "Large"; size = "87MB"; speed = "Slower"; accuracy = "Excellent" }
    "yolov8x.pt" = @{ name = "Extra Large"; size = "131MB"; speed = "Slowest"; accuracy = "Best" }
}

$currentModel = Split-Path -Leaf $modelPath
if ($modelInfo.ContainsKey($currentModel)) {
    $info = $modelInfo[$currentModel]
    Write-Host "📦 Using YOLOv8 $($info.name) model:" -ForegroundColor Cyan
    Write-Host "   Size: $($info.size) | Speed: $($info.speed) | Accuracy: $($info.accuracy)" -ForegroundColor Gray
} else {
    Write-Host "📦 Using custom model: $currentModel" -ForegroundColor Cyan
}

# Check if virtual environment exists
if (-not (Test-Path "venv")) {
    Write-Host "Virtual environment not found. Please run setup.ps1 first." -ForegroundColor Red
    exit 1
}

# Activate virtual environment
& ".\venv\Scripts\Activate.ps1"

# Build command arguments
$args = @("main.py")

# Input method
if ($Camera) {
    $args += "--camera"
    Write-Host "📸 Camera capture mode" -ForegroundColor Yellow
} elseif ($LiveCamera) {
    $args += "--live_camera"
    Write-Host "🎬 Live camera detection mode" -ForegroundColor Yellow
} else {
    $args += @("--image_path", $ImagePath)
}

# Camera settings
if ($Camera -or $LiveCamera) {
    $args += @("--camera_index", $CameraIndex)
}

# Model and confidence
$args += @("--model", $modelPath)
$args += @("--conf", $Confidence)

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
Write-Host "Running: python $($args -join ' ')" -ForegroundColor Gray
python @args

Write-Host "Detection completed!" -ForegroundColor Green
