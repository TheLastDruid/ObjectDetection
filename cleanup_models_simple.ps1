# Model Cleanup Script - Simple Version
Write-Host "Model Cleanup Utility" -ForegroundColor Cyan

# Ensure models directory exists
if (-not (Test-Path "models")) {
    New-Item -ItemType Directory -Path "models" -Force
    Write-Host "Created models/ directory" -ForegroundColor Green
}

# Move any model files from root to models/
$modelFiles = @("yolov8n.pt", "yolov8s.pt", "yolov8m.pt", "yolov8l.pt", "yolov8x.pt")
$movedCount = 0

foreach ($modelFile in $modelFiles) {
    if (Test-Path $modelFile) {
        $destination = "models\$modelFile"
        if (Test-Path $destination) {
            # Remove duplicate from root
            Remove-Item $modelFile -Force
            Write-Host "Removed duplicate $modelFile from root" -ForegroundColor Red
        } else {
            # Move to models directory
            Move-Item $modelFile $destination -Force
            Write-Host "Moved $modelFile to models/" -ForegroundColor Yellow
        }
        $movedCount++
    }
}

if ($movedCount -eq 0) {
    Write-Host "No cleanup needed - all models properly organized!" -ForegroundColor Green
} else {
    Write-Host "Cleanup complete! Processed $movedCount files" -ForegroundColor Green
}

# List current models
Write-Host ""
Write-Host "Current models in models/ directory:" -ForegroundColor Cyan
if (Test-Path "models") {
    Get-ChildItem -Path "models" -Filter "*.pt" | ForEach-Object {
        Write-Host "  $($_.Name)" -ForegroundColor White
    }
}
