# Model Training and Improvement Script for YOLOv8 Object Detection
# ================================================================

param(
    [string]$Action = "help",
    [string]$ProjectName = "custom_training",
    [string]$BaseModel = "yolov8n.pt",
    [int]$Epochs = 100,
    [string]$DatasetDir = "",
    [string[]]$ClassNames = @(),
    [string]$TestImages = "",
    [string[]]$Models = @(),
    [switch]$Help
)

function Show-Help {
    Write-Host "🔧 YOLOv8 Model Training and Improvement" -ForegroundColor Cyan
    Write-Host "=======================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "USAGE:" -ForegroundColor Yellow
    Write-Host "  .\train.ps1 -Action <action> [options]" -ForegroundColor White
    Write-Host ""
    Write-Host "ACTIONS:" -ForegroundColor Yellow
    Write-Host "  upgrade       - Upgrade to a larger/better model" -ForegroundColor Green
    Write-Host "  compare       - Compare different model sizes" -ForegroundColor Green
    Write-Host "  evaluate      - Evaluate model performance" -ForegroundColor Green
    Write-Host "  train         - Train custom model (requires dataset)" -ForegroundColor Green
    Write-Host "  prepare       - Prepare dataset for training" -ForegroundColor Green
    Write-Host "  download      - Download additional models" -ForegroundColor Green
    Write-Host ""
    Write-Host "OPTIONS:" -ForegroundColor Yellow
    Write-Host "  -ProjectName  Project name for training" -ForegroundColor White
    Write-Host "  -BaseModel    Base model to use (yolov8n.pt, yolov8s.pt, etc.)" -ForegroundColor White
    Write-Host "  -Epochs       Number of training epochs" -ForegroundColor White
    Write-Host "  -TestImages   Directory with test images" -ForegroundColor White
    Write-Host "  -Models       List of models to compare" -ForegroundColor White
    Write-Host ""
    Write-Host "EXAMPLES:" -ForegroundColor Yellow
    Write-Host "  # Upgrade to better model and compare" -ForegroundColor Gray
    Write-Host "  .\train.ps1 -Action upgrade" -ForegroundColor White
    Write-Host ""
    Write-Host "  # Compare model performance" -ForegroundColor Gray
    Write-Host "  .\train.ps1 -Action compare -TestImages 'input'" -ForegroundColor White
    Write-Host ""
    Write-Host "  # Download multiple model sizes" -ForegroundColor Gray
    Write-Host "  .\train.ps1 -Action download" -ForegroundColor White
    Write-Host ""
}

function Ensure-VirtualEnv {
    if (-not (Test-Path "venv\Scripts\Activate.ps1")) {
        Write-Host "❌ Virtual environment not found. Please run .\setup.ps1 first" -ForegroundColor Red
        exit 1
    }
    
    Write-Host "🔧 Activating virtual environment..." -ForegroundColor Blue
    & ".\venv\Scripts\Activate.ps1"
}

function Download-Models {
    Write-Host "📥 Downloading YOLOv8 Models..." -ForegroundColor Cyan
    
    # Ensure models directory exists
    if (-not (Test-Path "models")) {
        New-Item -ItemType Directory -Path "models" | Out-Null
    }
    
    $models = @(
        @{name="YOLOv8 Nano"; file="yolov8n.pt"; size="~6MB"; speed="Fastest"},
        @{name="YOLOv8 Small"; file="yolov8s.pt"; size="~22MB"; speed="Fast"},
        @{name="YOLOv8 Medium"; file="yolov8m.pt"; size="~52MB"; speed="Medium"}
    )
    
    foreach ($model in $models) {
        Write-Host "📦 Downloading $($model.name) ($($model.size))..." -ForegroundColor Green
        python -c "from ultralytics import YOLO; YOLO('$($model.file)')"
        
        # Move to models directory if not already there
        if (Test-Path $model.file) {
            Move-Item $model.file "models\" -Force
        }
        
        Write-Host "   ✅ $($model.name) ready" -ForegroundColor Green
    }
    
    Write-Host "🎉 All models downloaded to 'models\' directory" -ForegroundColor Cyan
}

function Upgrade-Model {
    Write-Host "⬆️  Upgrading Model for Better Recognition..." -ForegroundColor Cyan
    
    # First download better models
    Download-Models
    
    # Test current model vs upgraded models
    Write-Host "🧪 Testing model performance..." -ForegroundColor Blue
    python improve_model.py --demo --image "input\sample.jpg"
    
    Write-Host ""
    Write-Host "💡 RECOMMENDATIONS:" -ForegroundColor Yellow
    Write-Host "  1. Use YOLOv8s (Small) for balanced speed/accuracy" -ForegroundColor White
    Write-Host "  2. Use YOLOv8m (Medium) for better accuracy" -ForegroundColor White
    Write-Host "  3. Use YOLOv8l/x for maximum accuracy (slower)" -ForegroundColor White
    Write-Host ""
    Write-Host "To use a better model:" -ForegroundColor Yellow
    Write-Host "  .\run.ps1 -ModelPath 'models\yolov8s.pt' -SaveAnnotated" -ForegroundColor White
    Write-Host "  .\camera.ps1 -Capture -ModelPath 'models\yolov8m.pt' -SaveAnnotated" -ForegroundColor White
}

# Main execution
Ensure-VirtualEnv

switch ($Action.ToLower()) {
    "help" { Show-Help }
    "upgrade" { Upgrade-Model }
    "download" { Download-Models }
    default { 
        Write-Host "❌ Unknown action: $Action" -ForegroundColor Red
        Show-Help 
    }
}

if ($Help) {
    Show-Help
}
