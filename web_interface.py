#!/usr/bin/env python3
"""
Web Interface for Object Detection
Simple Flask web app for easy usage
"""

import os
import json
import cv2
import base64
from io import BytesIO
from PIL import Image
from flask import Flask, render_template, request, jsonify, send_file, flash, redirect, url_for
from werkzeug.utils import secure_filename
from pathlib import Path
from datetime import datetime
from ultralytics import YOLO
import tempfile

app = Flask(__name__)
app.secret_key = 'object_detection_secret_key'

# Configuration
UPLOAD_FOLDER = 'web_uploads'
OUTPUT_FOLDER = 'web_output'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff', 'webp', 'mp4', 'avi', 'mov', 'mkv'}

# Create directories
Path(UPLOAD_FOLDER).mkdir(exist_ok=True)
Path(OUTPUT_FOLDER).mkdir(exist_ok=True)

# Global model storage
models = {}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def load_model(model_path):
    """Load YOLO model with caching"""
    if model_path not in models:
        try:
            models[model_path] = YOLO(model_path)
            print(f"✅ Loaded model: {model_path}")
        except Exception as e:
            print(f"❌ Error loading model {model_path}: {e}")
            return None
    return models[model_path]

def get_available_models():
    """Get list of available models"""
    model_files = []
    
    # Check current directory
    for model_file in Path('.').glob('yolov8*.pt'):
        model_files.append(str(model_file))
    
    # Check models directory
    models_dir = Path('models')
    if models_dir.exists():
        for model_file in models_dir.glob('yolov8*.pt'):
            model_files.append(str(model_file))
    
    return sorted(model_files)

@app.route('/')
def index():
    """Main page"""
    available_models = get_available_models()
    return render_template('index.html', models=available_models)

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload and detection"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file selected'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'File type not supported'}), 400
    
    # Get parameters
    model_path = request.form.get('model', 'yolov8n.pt')
    confidence = float(request.form.get('confidence', 0.25))
    
    try:
        # Save uploaded file
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = Path(UPLOAD_FOLDER) / f"{timestamp}_{filename}"
        file.save(file_path)
        
        # Load model
        model = load_model(model_path)
        if model is None:
            return jsonify({'error': f'Could not load model: {model_path}'}), 500
        
        # Run detection
        results = model(str(file_path), conf=confidence)
        result = results[0]
        
        # Generate annotated image
        annotated_img = result.plot()
        
        # Convert to base64 for web display
        _, buffer = cv2.imencode('.jpg', annotated_img)
        img_base64 = base64.b64encode(buffer).decode('utf-8')
        
        # Prepare detection data
        detections = []
        if result.boxes is not None:
            for box in result.boxes:
                class_id = int(box.cls[0])
                confidence_score = float(box.conf[0])
                class_name = model.names[class_id]
                bbox = box.xyxy[0].tolist()
                
                detections.append({
                    'class': class_name,
                    'confidence': round(confidence_score, 3),
                    'bbox': {
                        'x1': round(bbox[0], 1), 'y1': round(bbox[1], 1),
                        'x2': round(bbox[2], 1), 'y2': round(bbox[3], 1)
                    }
                })
        
        # Save results
        output_path = Path(OUTPUT_FOLDER) / f"{timestamp}_{filename}_detected.jpg"
        cv2.imwrite(str(output_path), annotated_img)
        
        return jsonify({
            'success': True,
            'image': img_base64,
            'detections': detections,
            'objects_count': len(detections),
            'model_used': model_path,
            'confidence_threshold': confidence
        })
        
    except Exception as e:
        return jsonify({'error': f'Detection failed: {str(e)}'}), 500
    
    finally:
        # Clean up uploaded file
        if file_path.exists():
            file_path.unlink()

@app.route('/camera')
def camera_page():
    """Camera detection page"""
    available_models = get_available_models()
    return render_template('camera.html', models=available_models)

@app.route('/camera_capture', methods=['POST'])
def camera_capture():
    """Capture from camera and detect"""
    try:
        # Get parameters
        model_path = request.form.get('model', 'yolov8n.pt')
        confidence = float(request.form.get('confidence', 0.25))
        camera_index = int(request.form.get('camera_index', 0))
        
        # Load model
        model = load_model(model_path)
        if model is None:
            return jsonify({'error': f'Could not load model: {model_path}'}), 500
        
        # Capture from camera
        cap = cv2.VideoCapture(camera_index)
        if not cap.isOpened():
            return jsonify({'error': f'Could not open camera {camera_index}'}), 500
        
        ret, frame = cap.read()
        cap.release()
        
        if not ret:
            return jsonify({'error': 'Failed to capture frame'}), 500
        
        # Run detection
        results = model(frame, conf=confidence)
        result = results[0]
        
        # Generate annotated image
        annotated_img = result.plot()
        
        # Convert to base64
        _, buffer = cv2.imencode('.jpg', annotated_img)
        img_base64 = base64.b64encode(buffer).decode('utf-8')
        
        # Prepare detection data
        detections = []
        if result.boxes is not None:
            for box in result.boxes:
                class_id = int(box.cls[0])
                confidence_score = float(box.conf[0])
                class_name = model.names[class_id]
                bbox = box.xyxy[0].tolist()
                
                detections.append({
                    'class': class_name,
                    'confidence': round(confidence_score, 3),
                    'bbox': {
                        'x1': round(bbox[0], 1), 'y1': round(bbox[1], 1),
                        'x2': round(bbox[2], 1), 'y2': round(bbox[3], 1)
                    }
                })
        
        return jsonify({
            'success': True,
            'image': img_base64,
            'detections': detections,
            'objects_count': len(detections),
            'model_used': model_path,
            'confidence_threshold': confidence
        })
        
    except Exception as e:
        return jsonify({'error': f'Camera capture failed: {str(e)}'}), 500

@app.route('/models')
def models_page():
    """Models management page"""
    available_models = get_available_models()
    model_info = []
    
    for model_path in available_models:
        model_file = Path(model_path)
        size_mb = round(model_file.stat().st_size / (1024 * 1024), 1) if model_file.exists() else 0
        
        model_info.append({
            'path': model_path,
            'name': model_file.name,
            'size_mb': size_mb,
            'loaded': model_path in models
        })
    
    return render_template('models.html', models=model_info)

def create_templates():
    """Create HTML templates"""
    templates_dir = Path('templates')
    templates_dir.mkdir(exist_ok=True)
    
    # Main page template
    index_html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Object Detection Web Interface</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.1.3/css/bootstrap.min.css" rel="stylesheet">
    <style>
        .drop-zone {
            border: 2px dashed #ccc;
            border-radius: 10px;
            padding: 40px;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        .drop-zone:hover {
            border-color: #007bff;
            background-color: #f8f9fa;
        }
        .result-image {
            max-width: 100%;
            height: auto;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        .detection-card {
            border-left: 4px solid #007bff;
        }
    </style>
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container">
            <a class="navbar-brand" href="/">🎯 Object Detection</a>
            <div class="navbar-nav">
                <a class="nav-link" href="/">Upload</a>
                <a class="nav-link" href="/camera">Camera</a>
                <a class="nav-link" href="/models">Models</a>
            </div>
        </div>
    </nav>

    <div class="container my-5">
        <div class="row">
            <div class="col-md-6">
                <h2>Upload Image for Detection</h2>
                <form id="uploadForm" enctype="multipart/form-data">
                    <div class="mb-3">
                        <label for="model" class="form-label">Model</label>
                        <select id="model" name="model" class="form-select">
                            {% for model in models %}
                            <option value="{{ model }}">{{ model }}</option>
                            {% endfor %}
                        </select>
                    </div>
                    
                    <div class="mb-3">
                        <label for="confidence" class="form-label">Confidence Threshold</label>
                        <input type="range" id="confidence" name="confidence" class="form-range" min="0.1" max="1.0" step="0.05" value="0.25">
                        <small class="text-muted">Value: <span id="confidenceValue">0.25</span></small>
                    </div>
                    
                    <div class="drop-zone mb-3" onclick="document.getElementById('fileInput').click()">
                        <input type="file" id="fileInput" name="file" accept="image/*,video/*" style="display: none;">
                        <i class="fas fa-cloud-upload-alt fa-3x mb-3"></i>
                        <p>Click to select or drag and drop an image/video file</p>
                        <small class="text-muted">Supported: JPG, PNG, MP4, AVI, etc.</small>
                    </div>
                    
                    <button type="submit" class="btn btn-primary">🔍 Detect Objects</button>
                </form>
            </div>
            
            <div class="col-md-6">
                <div id="results" style="display: none;">
                    <h3>Detection Results</h3>
                    <img id="resultImage" class="result-image mb-3">
                    <div id="detectionInfo"></div>
                </div>
                
                <div id="loading" style="display: none;">
                    <div class="text-center">
                        <div class="spinner-border" role="status">
                            <span class="visually-hidden">Processing...</span>
                        </div>
                        <p class="mt-2">Processing image...</p>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.1.3/js/bootstrap.bundle.min.js"></script>
    <script>
        // Update confidence value display
        document.getElementById('confidence').addEventListener('input', function() {
            document.getElementById('confidenceValue').textContent = this.value;
        });

        // Handle form submission
        document.getElementById('uploadForm').addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            const file = document.getElementById('fileInput').files[0];
            
            if (!file) {
                alert('Please select a file first');
                return;
            }
            
            document.getElementById('loading').style.display = 'block';
            document.getElementById('results').style.display = 'none';
            
            fetch('/upload', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById('loading').style.display = 'none';
                
                if (data.success) {
                    document.getElementById('resultImage').src = 'data:image/jpeg;base64,' + data.image;
                    
                    let infoHtml = `
                        <div class="card detection-card">
                            <div class="card-body">
                                <h5 class="card-title">📊 Detection Summary</h5>
                                <p><strong>Objects Found:</strong> ${data.objects_count}</p>
                                <p><strong>Model Used:</strong> ${data.model_used}</p>
                                <p><strong>Confidence:</strong> ${data.confidence_threshold}</p>
                            </div>
                        </div>
                    `;
                    
                    if (data.detections.length > 0) {
                        infoHtml += '<div class="mt-3"><h6>🎯 Detected Objects:</h6>';
                        data.detections.forEach(det => {
                            infoHtml += `
                                <div class="alert alert-success">
                                    <strong>${det.class}</strong> - ${(det.confidence * 100).toFixed(1)}% confidence
                                </div>
                            `;
                        });
                        infoHtml += '</div>';
                    }
                    
                    document.getElementById('detectionInfo').innerHTML = infoHtml;
                    document.getElementById('results').style.display = 'block';
                } else {
                    alert('Error: ' + data.error);
                }
            })
            .catch(error => {
                document.getElementById('loading').style.display = 'none';
                alert('Error: ' + error);
            });
        });
    </script>
</body>
</html>'''    
    with open(templates_dir / 'index.html', 'w', encoding='utf-8') as f:
        f.write(index_html)
    
    # Camera page template
    camera_html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Camera Detection</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.1.3/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container">
            <a class="navbar-brand" href="/">🎯 Object Detection</a>
            <div class="navbar-nav">
                <a class="nav-link" href="/">Upload</a>
                <a class="nav-link active" href="/camera">Camera</a>
                <a class="nav-link" href="/models">Models</a>
            </div>
        </div>
    </nav>

    <div class="container my-5">
        <div class="row">
            <div class="col-md-6">
                <h2>Camera Detection</h2>
                <form id="cameraForm">
                    <div class="mb-3">
                        <label for="model" class="form-label">Model</label>
                        <select id="model" name="model" class="form-select">
                            {% for model in models %}
                            <option value="{{ model }}">{{ model }}</option>
                            {% endfor %}
                        </select>
                    </div>
                    
                    <div class="mb-3">
                        <label for="confidence" class="form-label">Confidence Threshold</label>
                        <input type="range" id="confidence" name="confidence" class="form-range" min="0.1" max="1.0" step="0.05" value="0.25">
                        <small class="text-muted">Value: <span id="confidenceValue">0.25</span></small>
                    </div>
                    
                    <div class="mb-3">
                        <label for="camera_index" class="form-label">Camera Index</label>
                        <input type="number" id="camera_index" name="camera_index" class="form-control" value="0" min="0" max="9">
                    </div>
                    
                    <button type="submit" class="btn btn-primary">📷 Capture & Detect</button>
                </form>
            </div>
            
            <div class="col-md-6">
                <div id="results" style="display: none;">
                    <h3>Detection Results</h3>
                    <img id="resultImage" class="img-fluid mb-3">
                    <div id="detectionInfo"></div>
                </div>
                
                <div id="loading" style="display: none;">
                    <div class="text-center">
                        <div class="spinner-border" role="status">
                            <span class="visually-hidden">Capturing...</span>
                        </div>
                        <p class="mt-2">Capturing from camera...</p>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.1.3/js/bootstrap.bundle.min.js"></script>
    <script>
        document.getElementById('confidence').addEventListener('input', function() {
            document.getElementById('confidenceValue').textContent = this.value;
        });

        document.getElementById('cameraForm').addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            
            document.getElementById('loading').style.display = 'block';
            document.getElementById('results').style.display = 'none';
            
            fetch('/camera_capture', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById('loading').style.display = 'none';
                
                if (data.success) {
                    document.getElementById('resultImage').src = 'data:image/jpeg;base64,' + data.image;
                    
                    let infoHtml = `
                        <div class="card">
                            <div class="card-body">
                                <h5 class="card-title">📊 Detection Summary</h5>
                                <p><strong>Objects Found:</strong> ${data.objects_count}</p>
                                <p><strong>Model Used:</strong> ${data.model_used}</p>
                                <p><strong>Confidence:</strong> ${data.confidence_threshold}</p>
                            </div>
                        </div>
                    `;
                    
                    if (data.detections.length > 0) {
                        infoHtml += '<div class="mt-3"><h6>🎯 Detected Objects:</h6>';
                        data.detections.forEach(det => {
                            infoHtml += `
                                <div class="alert alert-success">
                                    <strong>${det.class}</strong> - ${(det.confidence * 100).toFixed(1)}% confidence
                                </div>
                            `;
                        });
                        infoHtml += '</div>';
                    }
                    
                    document.getElementById('detectionInfo').innerHTML = infoHtml;
                    document.getElementById('results').style.display = 'block';
                } else {
                    alert('Error: ' + data.error);
                }
            })
            .catch(error => {
                document.getElementById('loading').style.display = 'none';
                alert('Error: ' + error);
            });
        });
    </script>
</body>
</html>'''
    
    with open(templates_dir / 'camera.html', 'w', encoding='utf-8') as f:
        f.write(camera_html)
    
    # Models page template
    models_html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Models Management</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.1.3/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container">
            <a class="navbar-brand" href="/">🎯 Object Detection</a>
            <div class="navbar-nav">
                <a class="nav-link" href="/">Upload</a>
                <a class="nav-link" href="/camera">Camera</a>
                <a class="nav-link active" href="/models">Models</a>
            </div>
        </div>
    </nav>

    <div class="container my-5">
        <h2>Available Models</h2>
        <div class="row">
            {% for model in models %}
            <div class="col-md-6 mb-3">
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">{{ model.name }}</h5>
                        <p class="card-text">
                            <strong>Path:</strong> {{ model.path }}<br>
                            <strong>Size:</strong> {{ model.size_mb }} MB<br>
                            <strong>Status:</strong> 
                            {% if model.loaded %}
                                <span class="badge bg-success">Loaded</span>
                            {% else %}
                                <span class="badge bg-secondary">Not Loaded</span>
                            {% endif %}
                        </p>
                    </div>
                </div>
            </div>
            {% endfor %}
        </div>
    </div>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.1.3/js/bootstrap.bundle.min.js"></script>
</body>
</html>'''
    
    with open(templates_dir / 'models.html', 'w', encoding='utf-8') as f:
        f.write(models_html)

def main():
    """Run the web application"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Object Detection Web Interface")
    parser.add_argument("--host", default="127.0.0.1", help="Host to bind to")
    parser.add_argument("--port", type=int, default=5000, help="Port to bind to")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    
    args = parser.parse_args()
    
    # Create templates
    create_templates()
    
    print(f"🌐 Starting Object Detection Web Interface")
    print(f"🔗 Access at: http://{args.host}:{args.port}")
    print(f"📱 Features: File Upload, Camera Capture, Model Management")
    
    app.run(host=args.host, port=args.port, debug=args.debug)

if __name__ == "__main__":
    main()
