# 🎯 ObjectDetection Web Platform

> **High-performance web-based object detection platform with modern UI and real-time capabilities**

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://python.org)
[![YOLOv8](https://img.shields.io/badge/YOLOv8-Ultralytics-orange)](https://ultralytics.com)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux-lightgrey)](README.md)
[![Flask](https://img.shields.io/badge/Flask-Web%20Interface-blue)](https://flask.palletsprojects.com)

**ObjectDetection** is a streamlined, high-performance web-based object detection platform built with YOLOv8. It features a **modern web interface** with real-time camera detection, optimized for speed and ease of use.

## 🆕 What's New in v3.0.0

✨ **Web-Only Focus** - Streamlined to focus exclusively on the web interface for better performance  
⚡ **Speed Optimizations** - Model caching, GPU support, frame skipping, and threaded processing  
🧹 **Clean Architecture** - Removed command-line scripts and batch processing for simplified codebase  
🎯 **No Duplicates** - Clean model management with organized storage in `models/` directory  
� **Easy Launch** - Simple batch files and PowerShell scripts for instant web app startup  
📱 **Enhanced Mobile** - Optimized web interface works perfectly on mobile devices

## ✨ Key Features

🌐 **Modern Web Interface** - Clean, responsive browser-based GUI with drag-and-drop  
� **Real-time Camera Detection** - Live camera streaming with instant object detection  
�️ **Image Processing** - Upload and process images with multiple YOLO models  
🎥 **Video Support** - Process video files with frame-by-frame detection  
⚡ **Performance Optimized** - Model caching, GPU support, and threaded processing  
🎯 **Smart Model Management** - Multiple YOLO models with automatic optimization  
� **Mobile Friendly** - Fully responsive design works on phones and tablets  
🚀 **Easy Launch** - Simple batch files and PowerShell scripts for instant startup

## 🚀 Quick Start

### Prerequisites
- **Python 3.8+** installed on your system
- **Git** for cloning the repository
- At least **4GB RAM** available
- **Webcam** (optional, for camera features)

### One-Command Setup
```powershell
# Clone and setup
git clone https://github.com/YOUR_USERNAME/ObjectDetection.git
cd ObjectDetection
.\setup.ps1

# Download models for better performance
.\train_simple.ps1 -Action download
```

### Launch Web Interface
```powershell
# Easy launch with batch file (Windows)
.\start.bat

# Or with PowerShell (optimized)
.\fast_web.ps1

# Or with simple batch launcher
.\run_web.bat
```

Then open your browser to **http://127.0.0.1:5000** and start detecting objects!

### Quick Model Training Setup
```powershell
# Compare available models
.\train_simple.ps1 -Action compare

# Upgrade to better model for improved accuracy
.\train_simple.ps1 -Action upgrade
```

## 📖 Web Interface Usage

### 🖼️ Image Detection
1. **Upload Images**: Drag and drop images or click to browse
2. **Select Model**: Choose from YOLOv8n (fast) to YOLOv8l (accurate)
3. **Adjust Settings**: Use confidence slider for detection threshold
4. **View Results**: See detected objects with bounding boxes and labels
5. **Download**: Save annotated images and JSON reports

### 📷 Camera Detection
1. **Access Camera**: Navigate to `/camera` page or use camera button
2. **Grant Permissions**: Allow browser to access your camera
3. **Live Detection**: See real-time object detection in your browser
4. **Capture Photos**: Take snapshots with detected objects
5. **Live Streaming**: Enable continuous detection mode

### 🎥 Video Processing
1. **Upload Video**: Select video files for processing
2. **Frame Analysis**: Automatic frame-by-frame detection
3. **Results Export**: Download processed frames and detection data

## 🎯 Model Performance

The platform supports multiple YOLOv8 models with **optimized loading** and **smart caching**:

| Model | Size | Speed | Accuracy | Best For |
|-------|------|-------|----------|----------|
| **YOLOv8n** | 6MB | ⚡ Very Fast | Good | Quick testing, low resources |
| **YOLOv8s** | 22MB | ⚡ Fast | Better | Balanced performance |
| **YOLOv8m** | 52MB | 🔄 Medium | ⭐ **Best** | **Production use, optimal balance** |
| **YOLOv8l** | 87MB | 🐌 Slower | Excellent | Maximum accuracy needed |
| **YOLOv8x** | 131MB | 🐌 Slowest | Maximum | Research, ultimate precision |

> **Default Model**: YOLOv8 Medium is selected by default as it provides the best balance of speed and accuracy for most use cases.

## 🧠 Model Training & Management

### 🚀 Quick Model Operations

**Download All Models:**
```powershell
.\train_simple.ps1 -Action download
```

**Upgrade to Better Model:**
```powershell
.\train_simple.ps1 -Action upgrade
```

**Compare Model Performance:**
```powershell
.\train_simple.ps1 -Action compare
```

### 📊 Model Comparison Tool

The built-in comparison tool tests all available models on your sample images:

```powershell
# Compare models on sample image
python improve_model.py --demo --image input/sample.jpg

# Compare specific models
python train_model.py --action compare --models "models/yolov8n.pt" "models/yolov8m.pt" --test_images "your_test_folder"
```

**Example Output:**
```
🎯 DETECTION COMPARISON RESULTS
========================================================================
Model           Objects  Best Detection            Confidence   Time (s)
------------------------------------------------------------------------
YOLOV8M         3        bear                      0.864        1.43
YOLOV8N         2        bear                      0.671        2.99
YOLOV8S         2        dog                       0.880        0.88
```

### 🎯 Custom Model Training

Train models on your own datasets for specific object detection tasks:

**1. Prepare Your Dataset:**
```
dataset/
├── images/
│   ├── train/    # Training images (.jpg, .png)
│   ├── val/      # Validation images
│   └── test/     # Test images
└── labels/
    ├── train/    # YOLO format labels (.txt)
    ├── val/      # One file per image
    └── test/     # Format: class_id x_center y_center width height
```

**2. Train Custom Model:**
```bash
# Train new model from scratch
python train_model.py --action train --project_name "my_custom_model" --class_names "person" "car" "bike" --epochs 100 --dataset_dir "my_dataset"

# Fine-tune existing model
python train_model.py --action finetune --project_name "improved_model" --base_model "models/yolov8m.pt" --epochs 50
```

**3. Annotation Tools:**
- **LabelImg**: https://github.com/tzutalin/labelImg (Desktop tool)
- **Label Studio**: https://labelstud.io/ (Web-based)
- **Roboflow**: https://roboflow.com/ (Cloud-based with augmentation)

### 🔧 Model Organization

All models are properly organized in the `models/` directory:

```
models/
├── yolov8n.pt    # Nano - Fastest
├── yolov8s.pt    # Small - Fast
├── yolov8m.pt    # Medium - ⭐ Default
├── yolov8l.pt    # Large - High accuracy
└── yolov8x.pt    # XLarge - Maximum accuracy
```

**Cleanup Utility:**
```powershell
# Automatically organize any misplaced model files
.\cleanup_models_simple.ps1
```

### 🔧 Smart Model Management
- **Duplicate Detection**: Automatically prevents duplicate models in dropdown lists
- **Organized Storage**: Models stored in dedicated `models/` directory
- **Availability Validation**: Only shows models that actually exist and are accessible
- **Clean Interface**: Dropdown lists show only valid, usable models

### 🔧 Performance Features
- **Model Caching**: Models loaded once and cached for faster subsequent use
- **GPU Acceleration**: Automatic GPU detection and utilization when available
- **Frame Skipping**: Optimized for real-time camera detection
- **Threaded Processing**: Non-blocking processing for better web performance
- **Auto-resize**: Automatic image resizing for optimal processing speed
- **JPEG Compression**: Optimized image delivery for web interface

## 📁 Project Structure

```
ObjectDetection/
├── � Launch Scripts
│   ├── start.bat              # Simple batch launcher
│   ├── run_web.bat            # Alternative batch launcher  
│   ├── fast_web.ps1           # Optimized PowerShell launcher
│   └── setup.ps1              # Environment setup
├── 🐍 Core Application
│   └── web_interface.py       # Main Flask web application (optimized)
├── 📁 Models & Data
│   ├── models/                # YOLO models (yolov8n, s, m, l)
│   ├── templates/             # Web interface HTML templates
│   ├── web_uploads/           # File uploads from web interface
│   └── web_output/            # Detection results and outputs
├── ⚙️ Configuration
│   ├── requirements.txt       # Python dependencies
│   ├── .vscode/tasks.json     # VS Code tasks for web interface
│   └── .gitignore             # Git ignore rules
└── 📚 Documentation
    ├── README.md              # This file (updated for web-only)
    ├── CHANGELOG.md           # Version history
    ├── CONTRIBUTING.md        # Contribution guide
    └── LICENSE                # MIT license
```

## 🌐 Web Interface Features

Launch the web interface using any of the provided launchers:

```powershell
# Fastest launch (recommended)
.\fast_web.ps1

# Simple batch launcher
.\start.bat

# Alternative batch launcher
.\run_web.bat
```

**Core Features:**
- 🎨 **Modern Design** - Clean, responsive interface with smooth animations
- 📤 **Drag & Drop Upload** - Intuitive file handling with visual feedback
- 📷 **Camera Integration** - Browser-based camera access with live preview
- 🎥 **Live Camera Streaming** - Real-time object detection with live video feed
- 📸 **Instant Capture** - Take photos directly from web interface
- 🎛️ **Smart Model Selection** - Choose different YOLO models without duplicates
- ⚙️ **Interactive Settings** - Dynamic confidence threshold slider
- 📊 **Real-time Results** - Instant detection visualization
- 📱 **Mobile Responsive** - Optimized for phones and tablets
- ⚡ **Performance Optimized** - Fast loading and processing

## ️ Troubleshooting

<details>
<summary><b>🐍 Python Environment Issues</b></summary>

```powershell
# Recreate virtual environment
Remove-Item -Recurse -Force venv
.\setup.ps1

# Verify installation
.\venv\Scripts\Activate.ps1
python -c "import torch, cv2, ultralytics; print('✅ All packages working')"
```
</details>

<details>
<summary><b>📦 Missing Dependencies</b></summary>

```powershell
# Force reinstall all dependencies
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt --force-reinstall --no-cache-dir

# Install specific package
pip install ultralytics --upgrade
```
</details>

<details>
<summary><b>🌐 Web Interface Issues</b></summary>

```powershell
# Check if web interface is running
# Open browser to http://127.0.0.1:5000

# Restart web interface
# Press Ctrl+C in terminal, then rerun launcher

# Clear browser cache if interface looks broken
# Ctrl+Shift+R (hard refresh)
```
</details>

<details>
<summary><b>📷 Camera Not Working</b></summary>

```powershell
# Test camera access
python -c "import cv2; cap = cv2.VideoCapture(0); print('Camera available:', cap.isOpened()); cap.release()"

# Check browser permissions
# Allow camera access when prompted

# Try different browser (Chrome, Firefox, Edge)
# Check camera permissions in Windows Settings > Privacy & Security > Camera
```
</details>

<details>
<summary><b>🚀 Performance Issues</b></summary>

**Slow Detection:**
- Use lighter model: Select YOLOv8n in the web interface
- Close unnecessary applications
- Enable GPU if available (automatic detection)
- Use lower confidence threshold for faster processing

**High Memory Usage:**
- Use nano model (YOLOv8n) instead of larger models
- Process smaller images or reduce image size
- Restart web interface periodically for long sessions
- Close other browser tabs
</details>

<details>
<summary><b>🧠 Model Training Issues</b></summary>

```powershell
# Download all models if missing
.\train_simple.ps1 -Action download

# Check model organization
.\cleanup_models_simple.ps1

# Test model comparison
.\train_simple.ps1 -Action compare

# Fix model paths if training fails
# Ensure dataset structure is correct:
# dataset/images/train/, dataset/labels/train/
```

**Common Training Problems:**
- **Missing Dataset**: Ensure proper YOLO format dataset structure
- **Wrong Paths**: All models should be in `models/` directory
- **Insufficient Data**: Need at least 100 images per class for good results
- **Label Format**: Use YOLO format (class_id x_center y_center width height)

**Annotation Tools:**
- LabelImg: https://github.com/tzutalin/labelImg
- Label Studio: https://labelstud.io/
- Roboflow: https://roboflow.com/

</details>

<details>
<summary><b>🎯 Model Performance Issues</b></summary>

```powershell
# Compare model performance
python improve_model.py --demo --image input/sample.jpg

# Test different models
.\train_simple.ps1 -Action compare

# Use better model for accuracy
.\train_simple.ps1 -Action upgrade
```

**Performance Tips:**
- **YOLOv8n**: Fastest, basic accuracy (good for testing)
- **YOLOv8m**: Best balance (recommended for production)
- **YOLOv8l**: High accuracy (slower but more precise)
- **GPU**: Ensure CUDA is available for faster training

</details>

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Quick Contribution Setup
```powershell
# Fork the repository on GitHub
git clone https://github.com/YOUR_USERNAME/ObjectDetection.git
cd ObjectDetection

# Create feature branch
git checkout -b feature/awesome-feature

# Make changes and test
.\setup.ps1
# ... make your changes ...

# Submit pull request
git add .
git commit -m "Add awesome feature"
git push origin feature/awesome-feature
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **[Ultralytics](https://ultralytics.com)** - For the amazing YOLOv8 implementation
- **[OpenCV](https://opencv.org)** - For computer vision utilities
- **[Flask](https://flask.palletsprojects.com)** - For the web interface framework

## 📞 Support

- 📖 **Documentation**: Check our [Wiki](https://github.com/YOUR_USERNAME/ObjectDetection/wiki)
- 🐛 **Bug Reports**: [Open an issue](https://github.com/YOUR_USERNAME/ObjectDetection/issues)
- 💡 **Feature Requests**: [Request a feature](https://github.com/YOUR_USERNAME/ObjectDetection/issues)
- 💬 **Discussions**: [Join the discussion](https://github.com/YOUR_USERNAME/ObjectDetection/discussions)

---

<div align="center">

**⭐ Star this repository if you find it helpful!**

[Report Bug](https://github.com/YOUR_USERNAME/ObjectDetection/issues) • [Request Feature](https://github.com/YOUR_USERNAME/ObjectDetection/issues) • [Contribute](CONTRIBUTING.md)

</div>
