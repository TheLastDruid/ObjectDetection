# Batch Processing Script for Object Detection
# Processes multiple images or videos with YOLOv8

param(
    [Parameter(Mandatory=$true)]
    [string]$InputPath,
    
    [Parameter(Mandatory=$false)]
    [string]$OutputDir = "output",
    
    [Parameter(Mandatory=$false)]
    [string]$ModelPath = "yolov8n.pt",
    
    [Parameter(Mandatory=$false)]
    [ValidateSet("images", "video")]
    [string]$Mode = "images",
    
    [Parameter(Mandatory=$false)]
    [double]$Confidence = 0.25,
    
    [Parameter(Mandatory=$false)]
    [switch]$SaveFrames,
    
    [Parameter(Mandatory=$false)]
    [int]$FrameInterval = 30,
    
    [Parameter(Mandatory=$false)]
    [switch]$NoAnnotated,
    
    [Parameter(Mandatory=$false)]
    [switch]$NoJson,
    
    [Parameter(Mandatory=$false)]
    [switch]$Help
)

function Show-Help {
    Write-Host @"

🚀 Batch Object Detection - Process Multiple Files
==============================================

USAGE:
    .\batch.ps1 -InputPath <path> [options]

EXAMPLES:
    # Process all images in a folder
    .\batch.ps1 -InputPath "input" -Mode images

    # Process images with better model
    .\batch.ps1 -InputPath "photos" -ModelPath "models\yolov8m.pt"

    # Process a video file
    .\batch.ps1 -InputPath "video.mp4" -Mode video -SaveFrames

    # Batch process with custom settings
    .\batch.ps1 -InputPath "dataset" -Confidence 0.5 -OutputDir "results"

PARAMETERS:
    -InputPath      Directory path (for images) or file path (for video) [REQUIRED]
    -OutputDir      Output directory (default: "output")
    -ModelPath      YOLOv8 model to use (default: "yolov8n.pt")
    -Mode           Processing mode: "images" or "video" (default: "images")
    -Confidence     Detection confidence threshold (default: 0.25)
    -SaveFrames     Save individual video frames with detections
    -FrameInterval  Process every N frames in video (default: 30)
    -NoAnnotated    Skip saving annotated images
    -NoJson         Skip saving JSON reports
    -Help           Show this help message

SUPPORTED FORMATS:
    Images: JPG, PNG, BMP, TIFF, WebP
    Videos: MP4, AVI, MOV, MKV, WMV, FLV

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

# Check if input path exists
if (-not (Test-Path $InputPath)) {
    Write-Host "❌ Input path not found: $InputPath" -ForegroundColor Red
    exit 1
}

# Activate virtual environment
Write-Host "🔧 Activating virtual environment..." -ForegroundColor Blue
& "venv\Scripts\Activate.ps1"

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to activate virtual environment" -ForegroundColor Red
    exit 1
}

# Prepare arguments
$pythonArgs = @(
    "batch_process.py"
    "--input", $InputPath
    "--output", $OutputDir
    "--model", $ModelPath
    "--mode", $Mode
    "--confidence", $Confidence.ToString()
)

if ($FrameInterval -ne 30) {
    $pythonArgs += "--frame-interval", $FrameInterval.ToString()
}

if ($SaveFrames) {
    $pythonArgs += "--save-frames"
}

if ($NoAnnotated) {
    $pythonArgs += "--no-annotated"
}

if ($NoJson) {
    $pythonArgs += "--no-json"
}

# Display configuration
Write-Host ""
Write-Host "🚀 Starting Batch Object Detection" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Green
Write-Host "📁 Input: $InputPath" -ForegroundColor Cyan
Write-Host "📤 Output: $OutputDir" -ForegroundColor Cyan
Write-Host "🔧 Model: $ModelPath" -ForegroundColor Cyan
Write-Host "🎯 Mode: $Mode" -ForegroundColor Cyan
Write-Host "📊 Confidence: $Confidence" -ForegroundColor Cyan

if ($Mode -eq "video") {
    Write-Host "🎬 Frame Interval: $FrameInterval" -ForegroundColor Cyan
    if ($SaveFrames) {
        Write-Host "💾 Save Frames: Yes" -ForegroundColor Cyan
    }
}

Write-Host ""

# Run batch processing
try {
    python @pythonArgs
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "✅ Batch processing completed successfully!" -ForegroundColor Green
        Write-Host "📁 Check output directory: $OutputDir" -ForegroundColor Yellow
        
        # Open output directory
        if (Test-Path $OutputDir) {
            $openChoice = Read-Host "Would you like to open the output directory? (y/n)"
            if ($openChoice -eq 'y' -or $openChoice -eq 'Y') {
                Invoke-Item $OutputDir
            }
        }
    } else {
        Write-Host "❌ Batch processing failed with exit code: $LASTEXITCODE" -ForegroundColor Red
    }
} catch {
    Write-Host "❌ Error during batch processing: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}
