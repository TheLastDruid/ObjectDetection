# Model Cleanup Script
# Moves any YOLO model files from root to models/ directory

Write-Host "🧹 Model Cleanup Utility" -ForegroundColor Cyan
Write-Host "========================" -ForegroundColor Cyan

# Ensure models directory exists
if (-not (Test-Path "models")) {
    New-Item -ItemType Directory -Path "models" -Force
    Write-Host "📁 Created models/ directory" -ForegroundColor Green
}

# List of YOLO model files to check
$modelFiles = @("yolov8n.pt", "yolov8s.pt", "yolov8m.pt", "yolov8l.pt", "yolov8x.pt")
$movedCount = 0

foreach ($modelFile in $modelFiles) {
    $rootPath = $modelFile
    $modelsPath = "models\$modelFile"
    
    # If model exists in root but not in models/, move it
    if ((Test-Path $rootPath) -and (-not (Test-Path $modelsPath))) {
        Move-Item -Path $rootPath -Destination $modelsPath -Force
        Write-Host "📦 Moved $modelFile to models/ directory" -ForegroundColor Yellow
        $movedCount++
    }
    # If model exists in both locations, remove from root
    elseif ((Test-Path $rootPath) -and (Test-Path $modelsPath)) {
        Remove-Item -Path $rootPath -Force
        Write-Host "🗑️  Removed duplicate $modelFile from root" -ForegroundColor Red
        $movedCount++
    }
    # Check if model exists in models/
    elseif (Test-Path $modelsPath) {
        Write-Host "✅ $modelFile is properly located in models/" -ForegroundColor Green
    }
}

if ($movedCount -eq 0) {
    Write-Host "✨ No cleanup needed - all models are properly organized!" -ForegroundColor Green
} else {
    Write-Host "✅ Cleanup complete! Moved/removed $movedCount files" -ForegroundColor Green
}

Write-Host ""
Write-Host "Current models in models/ directory:" -ForegroundColor Cyan
Get-ChildItem -Path "models" -Filter "*.pt" | ForEach-Object {
    $size = [math]::Round($_.Length / 1MB, 1)
    $name = $_.Name
    Write-Host "   $name ($size MB)" -ForegroundColor White
}
