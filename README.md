# 🎯 ObjectDetection Platform

> **Advanced object detection platform with web interface, batch processing, and PowerShell automation**

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://python.org)
[![YOLOv8](https://img.shields.io/badge/YOLOv8-Ultralytics-orange)](https://ultralytics.com)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux-lightgrey)](README.md)

**ObjectDetection** is a comprehensive, production-ready object detection platform built with YOLOv8. It features a modern web interface, batch processing, real-time camera detection, and powerful configuration management - all wrapped in intuitive PowerShell scripts.

## ✨ Key Features

🖼️ **Multiple Input Methods** - Images, videos, camera capture, live detection  
🌐 **Web Interface** - Modern browser-based GUI with drag-and-drop  
🔄 **Batch Processing** - Handle multiple files with comprehensive reporting  
📷 **Camera Integration** - Real-time detection and capture capabilities  
⚙️ **Configuration Management** - Preset management for different use cases  
🚀 **PowerShell Scripts** - Windows-native scripts for easy operation  
🎯 **Model Management** - Multi-model support with automatic downloading  
📊 **Performance Analysis** - Built-in benchmarking and comparison tools

## 🚀 Quick Start

### Prerequisites
- **Python 3.8+** installed on your system
- **PowerShell** (Windows) or **Bash** (Linux)
- At least **4GB RAM** available

### One-Command Setup
```powershell
# Clone and setup in one go
git clone https://github.com/YOUR_USERNAME/ObjectDetection.git
cd ObjectDetection
.\setup.ps1
```

### Basic Usage
```powershell
# 🖼️ Detect objects in images
.\run.ps1 -SaveAnnotated -SaveJson -CountObjects

# 📷 Camera capture and detection
.\camera.ps1 -Capture -SaveAnnotated -SaveJson

# 🌐 Launch web interface
.\web.ps1 -OpenBrowser

# 🔄 Batch process multiple files
.\batch.ps1 -InputPath "input" -Mode images
```

## 📖 Usage Examples

<details>
<summary><b>🖼️ Image Detection</b></summary>

```powershell
# Process single image
.\run.ps1 -ImagePath "input/photo.jpg" -SaveAnnotated

# Use different model for better accuracy
.\run.ps1 -ModelPath "models/yolov8m.pt" -SaveAnnotated

# Custom confidence threshold
python main.py --image_path "input/photo.jpg" --conf_threshold 0.7 --save_annotated
```
</details>

<details>
<summary><b>📷 Camera Detection</b></summary>

```powershell
# Single photo capture
.\camera.ps1 -Capture -SaveAnnotated -SaveJson -CountObjects

# Live camera detection (press 'q' to quit)
.\camera.ps1 -Live -SaveAnnotated

# Use specific camera (if multiple cameras)
.\camera.ps1 -Capture -CameraIndex 1 -SaveAnnotated
```
</details>

<details>
<summary><b>🔄 Batch Processing</b></summary>

```powershell
# Process all images in directory
.\batch.ps1 -InputPath "my_photos" -Mode images

# Process video with frame extraction
.\batch.ps1 -InputPath "video.mp4" -Mode video -SaveFrames

# Batch process with performance model
.\batch.ps1 -InputPath "photos" -ModelPath "models/yolov8m.pt"
```
</details>

<details>
<summary><b>🌐 Web Interface</b></summary>

```powershell
# Launch local web interface
.\web.ps1 -OpenBrowser

# Start with network access (accessible from other devices)
.\web.ps1 -Host "0.0.0.0" -Port 5000

# Start in debug mode
.\web.ps1 -Debug -OpenBrowser
```
</details>

## 🎯 Model Performance

The platform supports multiple YOLOv8 model variants, automatically downloading and comparing performance:

| Model | Size | Speed | Accuracy | Best For |
|-------|------|-------|----------|----------|
| **YOLOv8n** | 6MB | ⚡ Very Fast | Good | Quick testing, low resources |
| **YOLOv8s** | 22MB | ⚡ Fast | Better | Balanced performance |
| **YOLOv8m** | 52MB | 🔄 Medium | Best | Production use, high accuracy |
| **YOLOv8l** | 87MB | 🐌 Slower | Excellent | Maximum accuracy needed |

### Model Management
```powershell
# Download and compare all models
.\train.ps1 -Action upgrade

# Compare performance on your images
python improve_model.py --demo --image "input/sample.jpg"

# Use specific model
.\run.ps1 -ModelPath "models/yolov8m.pt" -SaveAnnotated
```

## 📁 Project Structure

```
ObjectDetection/
├── 🔧 Automation Scripts
│   ├── setup.ps1              # Environment setup
│   ├── run.ps1                # Image detection
│   ├── camera.ps1             # Camera operations
│   ├── batch.ps1              # Batch processing
│   ├── train.ps1              # Model management
│   └── web.ps1                # Web interface
├── 🐍 Core Python Scripts
│   ├── main.py                # Detection engine
│   ├── web_interface.py       # Flask web app
│   ├── batch_process.py       # Batch processing
│   ├── config_manager.py      # Configuration management
│   ├── train_model.py         # Training utilities
│   └── improve_model.py       # Performance analysis
├── 📁 Data Directories
│   ├── input/                 # Input images/videos
│   ├── output/                # Detection results
│   ├── models/                # YOLO models (auto-downloaded)
│   ├── configs/               # Configuration presets
│   └── templates/             # Web interface templates
└── 📚 Documentation
    ├── README.md              # This file
    ├── CONTRIBUTING.md        # Contribution guide
    ├── CHANGELOG.md           # Version history
    └── LICENSE                # MIT license
```

## ⚙️ Configuration Management

The platform includes a powerful configuration system with preset profiles:

```powershell
# List available presets
python config_manager.py --list

# Create common presets
python config_manager.py --create-common
```

### Available Presets
- **🚀 Fast Processing** - Optimized for speed (YOLOv8n, low confidence)
- **🎯 High Accuracy** - Maximum precision (YOLOv8m, high confidence)  
- **📱 Mobile Friendly** - Lightweight for low-resource devices
- **🔒 Security Camera** - Optimized for surveillance scenarios

## 🌐 Web Interface Features

Launch the modern web interface for non-technical users:

```powershell
.\web.ps1 -OpenBrowser
```

**Features:**
- 📤 **Drag & Drop Upload** - Easy file handling
- 📷 **Camera Integration** - Browser-based camera access
- 🎛️ **Model Selection** - Choose different YOLO models
- ⚙️ **Adjustable Settings** - Confidence thresholds, output options
- 📊 **Real-time Results** - Instant detection visualization
- 📱 **Mobile Responsive** - Works on phones and tablets

## 🔧 Advanced Configuration

### Custom Model Training
```powershell
# Prepare training environment
.\train.ps1 -Action prepare

# Train custom model (after data preparation)
.\train.ps1 -Action train -ClassNames "cat,dog,bird" -ProjectName "pets"
```

### Performance Optimization
```powershell
# Benchmark different models
python improve_model.py --batch_dir "input"

# GPU acceleration (if CUDA available)
python main.py --device cuda --image_path "input/sample.jpg"
```

## 🛠️ Troubleshooting

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
<summary><b>🔧 PowerShell Execution Issues</b></summary>

```powershell
# Enable script execution (run as Administrator)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Run with bypass (alternative)
powershell.exe -ExecutionPolicy Bypass -File ".\setup.ps1"
```
</details>

<details>
<summary><b>📷 Camera Not Working</b></summary>

```powershell
# Test camera access
python -c "import cv2; cap = cv2.VideoCapture(0); print('Camera available:', cap.isOpened()); cap.release()"

# Try different camera index
.\camera.ps1 -Capture -CameraIndex 1

# Check camera permissions in Windows Settings > Privacy & Security > Camera
```
</details>

<details>
<summary><b>🚀 Performance Issues</b></summary>

**Slow Detection:**
- Use lighter model: `.\run.ps1 -ModelPath "models/yolov8n.pt"`
- Reduce image size before processing
- Close unnecessary applications
- Enable GPU if available: `python main.py --device cuda`

**High Memory Usage:**
- Use nano model (YOLOv8n) instead of larger models
- Process images individually instead of batch
- Restart application periodically for long sessions
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
