# Simple Model Training Script
param(
    [string]$Action = "help",
    [string]$ProjectName = "custom_training",
    [string]$BaseModel = "models/yolov8n.pt",
    [int]$Epochs = 100,
    [switch]$Help
)

if ($Help -or $Action -eq "help") {
    Write-Host "YOLOv8 Model Training" -ForegroundColor Cyan
    Write-Host "===================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Actions:" -ForegroundColor Yellow
    Write-Host "  upgrade    - Download larger models for better accuracy"
    Write-Host "  compare    - Compare model performance" 
    Write-Host "  train      - Train custom model (requires dataset)"
    Write-Host "  download   - Download all model variants"
    Write-Host ""
    Write-Host "Examples:" -ForegroundColor Yellow
    Write-Host "  .\train_simple.ps1 -Action download"
    Write-Host "  .\train_simple.ps1 -Action upgrade"
    Write-Host "  .\train_simple.ps1 -Action compare"
    exit 0
}

# Check virtual environment
if (-not (Test-Path "venv\Scripts\python.exe")) {
    Write-Host "ERROR: Virtual environment not found. Run setup.ps1 first." -ForegroundColor Red
    exit 1
}

Write-Host "Model Training - Action: $Action" -ForegroundColor Green

switch ($Action.ToLower()) {
    "download" {        Write-Host "Downloading YOLO model variants..." -ForegroundColor Cyan
        & ".\venv\Scripts\python.exe" -c @"
from ultralytics import YOLO
import os
import shutil

# Ensure models directory exists
if not os.path.exists('models'):
    os.makedirs('models')

models = ['yolov8n.pt', 'yolov8s.pt', 'yolov8m.pt', 'yolov8l.pt', 'yolov8x.pt']
for model in models:
    model_path = f'models/{model}'
    if os.path.exists(model_path):
        print(f'✅ {model} already exists in models/')
        continue
        
    print(f'Downloading {model}...')
    try:
        # Download model (this saves to current directory)
        yolo = YOLO(model)
        
        # Move to models directory if downloaded to root
        if os.path.exists(model) and not os.path.exists(model_path):
            shutil.move(model, model_path)
            
        print(f'✅ {model} ready in models/')
    except Exception as e:
        print(f'❌ Error with {model}: {e}')

# Clean up any remaining model files in root
for model in models:
    if os.path.exists(model) and os.path.exists(f'models/{model}'):
        os.remove(model)
        print(f'🧹 Cleaned up duplicate {model} from root')
"@
    }
    
    "upgrade" {        Write-Host "Upgrading to larger model..." -ForegroundColor Cyan
        & ".\venv\Scripts\python.exe" -c @"
from ultralytics import YOLO
import os
import shutil

# Ensure models directory exists
if not os.path.exists('models'):
    os.makedirs('models')

print('Downloading YOLOv8m (medium) for better accuracy...')
try:
    model_path = 'models/yolov8m.pt'
    if os.path.exists(model_path):
        print('✅ YOLOv8m already exists in models/')
    else:
        # Download model
        model = YOLO('yolov8m.pt')
        
        # Move to models directory if downloaded to root
        if os.path.exists('yolov8m.pt') and not os.path.exists(model_path):
            shutil.move('yolov8m.pt', model_path)
            
        print('✅ Upgraded to YOLOv8m - Better accuracy!')
        print('   Location: models/yolov8m.pt')
        print('   Use in web interface: Select yolov8m.pt model')
        
except Exception as e:
    print(f'❌ Error: {e}')
"@
    }
    
    "compare" {
        Write-Host "Comparing model performance..." -ForegroundColor Cyan
        & ".\venv\Scripts\python.exe" -c @"
import time
from ultralytics import YOLO
import cv2
import os

# Test image
test_image = 'input/sample.jpg' if os.path.exists('input/sample.jpg') else None

if not test_image:
    print('❌ No test image found. Place an image in input/sample.jpg')
    exit()

models = []
for model_file in ['models/yolov8n.pt', 'models/yolov8s.pt', 'models/yolov8m.pt', 'models/yolov8l.pt']:
    if os.path.exists(model_file):
        models.append(model_file)

if not models:
    print('❌ No models found. Run download action first.')
    exit()

print(f'Testing models on: {test_image}')
print('-' * 50)

for model_path in models:
    try:
        print(f'Testing {model_path}...')
        model = YOLO(model_path)
        
        # Time the detection
        start_time = time.time()
        results = model(test_image, verbose=False)
        end_time = time.time()
        
        detection_time = end_time - start_time
        num_detections = len(results[0].boxes) if results[0].boxes else 0
        
        print(f'  ⏱️  Time: {detection_time:.3f}s')
        print(f'  🎯 Objects: {num_detections}')
        print(f'  📊 Speed: {1/detection_time:.1f} FPS')
        print()
        
    except Exception as e:
        print(f'  ❌ Error: {e}')
"@
    }
    
    "train" {
        Write-Host "Custom training requires dataset preparation..." -ForegroundColor Yellow
        Write-Host "For custom training, you need:"
        Write-Host "1. Images with annotations"
        Write-Host "2. YOLO format labels"
        Write-Host "3. Dataset configuration"
        Write-Host ""
        Write-Host "Use tools like:"
        Write-Host "- LabelImg: https://github.com/tzutalin/labelImg"
        Write-Host "- Roboflow: https://roboflow.com/"
        Write-Host ""
        Write-Host "Then run: python train_model.py"
    }
    
    default {
        Write-Host "Unknown action: $Action" -ForegroundColor Red
        Write-Host "Use -Help for available actions"
    }
}

Write-Host "Done!" -ForegroundColor Green
