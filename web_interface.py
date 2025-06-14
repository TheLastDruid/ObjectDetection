#!/usr/bin/env python3
"""
Web Interface for Object Detection
Simple Flask web app for easy usage
"""

import os
import json
import cv2
import base64
import numpy as np
from io import BytesIO
from PIL import Image
from flask import Flask, render_template, request, jsonify, send_file, flash, redirect, url_for, Response
from werkzeug.utils import secure_filename
from pathlib import Path
from datetime import datetime
from ultralytics import YOLO
import tempfile
import threading
import time
import torch

app = Flask(__name__)
app.secret_key = 'object_detection_secret_key'

# Flask optimization settings
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 300  # Cache static files for 5 minutes
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Configuration
UPLOAD_FOLDER = 'web_uploads'
OUTPUT_FOLDER = 'web_output'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff', 'webp', 'mp4', 'avi', 'mov', 'mkv'}

# Create directories
Path(UPLOAD_FOLDER).mkdir(exist_ok=True)
Path(OUTPUT_FOLDER).mkdir(exist_ok=True)

# Global model storage with optimization
models = {}
device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(f"🚀 Using device: {device}")

# Global variables for live camera
live_camera_active = False
live_camera_thread = None
live_frame = None
live_detections = None

# Performance optimization settings
FRAME_SKIP = 2  # Process every 2nd frame for better performance
MAX_FRAME_SIZE = (640, 480)  # Limit frame size for faster processing
JPEG_QUALITY = 70  # Reduce quality for faster streaming

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def load_model(model_path):
    """Load YOLO model with caching and optimization"""
    if model_path not in models:
        try:
            model = YOLO(model_path)
            model.to(device)
            
            # Optimize model for inference
            if device == 'cuda':
                try:
                    model.model.half()  # Use half precision for speed
                    print(f"✅ Loaded model: {model_path} (GPU optimized)")
                except:
                    print(f"✅ Loaded model: {model_path} (GPU)")
            else:
                print(f"✅ Loaded model: {model_path} (CPU)")
                
            models[model_path] = model
        except Exception as e:
            print(f"❌ Error loading model {model_path}: {e}")
            return None
    return models[model_path]

def get_available_models():
    """Get list of available models"""
    model_files = []
    
    # Check models directory first (preferred location)
    models_dir = Path('models')
    if models_dir.exists():
        for model_file in models_dir.glob('yolov8*.pt'):
            if model_file.exists():  # Ensure file actually exists
                model_files.append(str(model_file))
    
    # Only check current directory if no models found in models directory
    if not model_files:
        for model_file in Path('.').glob('yolov8*.pt'):
            if model_file.exists():  # Ensure file actually exists
                model_files.append(str(model_file))
    
    return sorted(model_files)

@app.route('/')
def index():
    """Main page"""
    available_models = get_available_models()
    return render_template('index.html', models=available_models)

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload and detection with optimization"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file selected'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'File type not supported'}), 400
    
    # Get parameters
    model_path = request.form.get('model', 'models/yolov8m.pt')
    confidence = float(request.form.get('confidence', 0.25))
    
    try:
        # Save uploaded file
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = Path(UPLOAD_FOLDER) / f"{timestamp}_{filename}"
        file.save(file_path)
        
        # Optimize image for faster processing
        img = cv2.imread(str(file_path))
        if img is not None:
            height, width = img.shape[:2]
            # Resize large images for faster processing
            max_size = 1024
            if width > max_size or height > max_size:
                scale = min(max_size/width, max_size/height)
                new_width = int(width * scale)
                new_height = int(height * scale)
                img = cv2.resize(img, (new_width, new_height))
                cv2.imwrite(str(file_path), img)
        
        # Load model
        model = load_model(model_path)
        if model is None:
            return jsonify({'error': f'Could not load model: {model_path}'}), 500
        
        # Run detection with optimized settings
        results = model(str(file_path), 
                       conf=confidence, 
                       iou=0.5,
                       verbose=False,
                       device=device)
        result = results[0]
        
        # Generate annotated image
        annotated_img = result.plot()
        
        # Convert to base64 for web display with optimized quality
        encode_params = [cv2.IMWRITE_JPEG_QUALITY, 85]
        _, buffer = cv2.imencode('.jpg', annotated_img, encode_params)
        img_base64 = base64.b64encode(buffer).decode('utf-8')
        
        # Prepare detection data (simplified for speed)
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
    """Capture from camera and detect with optimization"""
    try:
        # Get parameters
        model_path = request.form.get('model', 'models/yolov8m.pt')
        confidence = float(request.form.get('confidence', 0.25))
        camera_index = int(request.form.get('camera_index', 0))
        
        # Load model
        model = load_model(model_path)
        if model is None:
            return jsonify({'error': f'Could not load model: {model_path}'}), 500
        
        # Capture from camera with optimization
        cap = cv2.VideoCapture(camera_index)
        if not cap.isOpened():
            return jsonify({'error': f'Could not open camera {camera_index}'}), 500
        
        # Set optimal capture settings
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, MAX_FRAME_SIZE[0])
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, MAX_FRAME_SIZE[1])
        
        # Warm up camera
        for _ in range(3):
            cap.read()
        
        ret, frame = cap.read()
        cap.release()
        
        if not ret:
            return jsonify({'error': 'Failed to capture frame'}), 500
        
        # Resize if needed for faster processing
        height, width = frame.shape[:2]
        if width > MAX_FRAME_SIZE[0] or height > MAX_FRAME_SIZE[1]:
            scale = min(MAX_FRAME_SIZE[0]/width, MAX_FRAME_SIZE[1]/height)
            new_width = int(width * scale)
            new_height = int(height * scale)
            frame = cv2.resize(frame, (new_width, new_height))
        
        # Run detection with optimized settings
        results = model(frame, 
                       conf=confidence, 
                       iou=0.5,
                       verbose=False,
                       device=device)
        result = results[0]
        
        # Generate annotated image
        annotated_img = result.plot()
        
        # Convert to base64 with optimized quality
        encode_params = [cv2.IMWRITE_JPEG_QUALITY, 85]
        _, buffer = cv2.imencode('.jpg', annotated_img, encode_params)
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

def generate_frames(camera_index=0, model_path='models/yolov8m.pt', confidence=0.25):
    """Generate frames for live camera stream with performance optimizations"""
    global live_camera_active, live_frame, live_detections
    
    # Load model
    model = load_model(model_path)
    if model is None:
        return
    
    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        return
    
    # Optimize camera settings for speed
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, MAX_FRAME_SIZE[0])
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, MAX_FRAME_SIZE[1])
    cap.set(cv2.CAP_PROP_FPS, 30)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # Reduce buffer for latest frame
    
    frame_count = 0
    
    try:
        while live_camera_active:
            ret, frame = cap.read()
            if not ret:
                break
            
            frame_count += 1
            
            # Skip frames for better performance
            if frame_count % FRAME_SKIP == 0:
                # Resize frame for faster processing
                height, width = frame.shape[:2]
                if width > MAX_FRAME_SIZE[0] or height > MAX_FRAME_SIZE[1]:
                    scale = min(MAX_FRAME_SIZE[0]/width, MAX_FRAME_SIZE[1]/height)
                    new_width = int(width * scale)
                    new_height = int(height * scale)
                    frame = cv2.resize(frame, (new_width, new_height))
                
                # Run detection with optimized settings
                results = model(frame, 
                              conf=confidence, 
                              iou=0.5,  # Higher IOU for faster NMS
                              verbose=False,
                              device=device)
                result = results[0]
                
                # Generate annotated image
                annotated_frame = result.plot()
                
                # Store current frame and detections for other routes
                live_frame = annotated_frame.copy()
                
                # Prepare detection data (simplified)
                detections = []
                if result.boxes is not None:
                    for box in result.boxes:
                        class_id = int(box.cls[0])
                        confidence_score = float(box.conf[0])
                        class_name = model.names[class_id]
                        
                        detections.append({
                            'class': class_name,
                            'confidence': round(confidence_score, 2)  # Reduced precision
                        })
                
                live_detections = detections
                
                # Encode frame to JPEG with optimized quality
                encode_params = [cv2.IMWRITE_JPEG_QUALITY, JPEG_QUALITY]
                _, buffer = cv2.imencode('.jpg', annotated_frame, encode_params)
                frame_bytes = buffer.tobytes()
                
                # Yield frame in multipart format
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
            else:
                # For skipped frames, just encode the raw frame
                encode_params = [cv2.IMWRITE_JPEG_QUALITY, JPEG_QUALITY]
                _, buffer = cv2.imencode('.jpg', frame, encode_params)
                frame_bytes = buffer.tobytes()
                
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
            
            time.sleep(0.03)  # ~30 FPS cap
            
    finally:
        cap.release()

@app.route('/camera_stream')
def camera_stream():
    """Video streaming route"""
    camera_index = int(request.args.get('camera_index', 0))
    model_path = request.args.get('model', 'models/yolov8m.pt')
    confidence = float(request.args.get('confidence', 0.25))
    
    return Response(generate_frames(camera_index, model_path, confidence),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/start_live_detection', methods=['POST'])
def start_live_detection():
    """Start live camera detection"""
    global live_camera_active, live_camera_thread
    
    if live_camera_active:
        return jsonify({'success': False, 'error': 'Live detection already active'}), 400
    
    try:
        camera_index = int(request.form.get('camera_index', 0))
        model_path = request.form.get('model', 'models/yolov8m.pt')
        confidence = float(request.form.get('confidence', 0.25))
        
        # Test camera access
        import cv2
        cap = cv2.VideoCapture(camera_index)
        if not cap.isOpened():
            cap.release()
            return jsonify({'success': False, 'error': f'Cannot access camera {camera_index}. Please check camera connection and permissions.'}), 400
        cap.release()
        
        # Test model loading
        model = load_model(model_path)
        if model is None:
            return jsonify({'success': False, 'error': f'Cannot load model {model_path}. Please check if the model file exists.'}), 400
        
        live_camera_active = True
        
        return jsonify({
            'success': True,
            'message': 'Live detection started',
            'stream_url': f'/camera_stream?camera_index={camera_index}&model={model_path}&confidence={confidence}'
        })
        
    except ValueError as e:
        return jsonify({'success': False, 'error': f'Invalid parameter values: {str(e)}'}), 400
    except Exception as e:
        live_camera_active = False
        return jsonify({'success': False, 'error': f'Failed to start live detection: {str(e)}'}), 500

@app.route('/stop_live_detection', methods=['POST'])
def stop_live_detection():
    """Stop live camera detection"""
    global live_camera_active, live_camera_thread
    
    live_camera_active = False
    
    if live_camera_thread and live_camera_thread.is_alive():
        live_camera_thread.join(timeout=2)
    
    return jsonify({'success': True, 'message': 'Live detection stopped'})

@app.route('/live_detection_status')
def live_detection_status():
    """Get current live detection status and data"""
    global live_camera_active, live_detections
    
    return jsonify({
        'active': live_camera_active,
        'detections': live_detections if live_detections else [],
        'objects_count': len(live_detections) if live_detections else 0
    })

@app.route('/capture_live_frame', methods=['POST'])
def capture_live_frame():
    """Capture current live frame"""
    global live_frame, live_detections
    
    if not live_camera_active or live_frame is None:
        return jsonify({'error': 'No live detection active'}), 400
    
    try:
        # Save the current frame
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"live_capture_{timestamp}.jpg"
        output_path = Path(OUTPUT_FOLDER) / filename
        
        cv2.imwrite(str(output_path), live_frame)
        
        # Convert to base64 for response
        _, buffer = cv2.imencode('.jpg', live_frame)
        img_base64 = base64.b64encode(buffer).decode('utf-8')
        
        return jsonify({
            'success': True,
            'image': img_base64,
            'filename': filename,
            'detections': live_detections if live_detections else [],
            'objects_count': len(live_detections) if live_detections else 0
        })
        
    except Exception as e:
        return jsonify({'error': f'Failed to capture frame: {str(e)}'}), 500

@app.route('/camera_feed')
def camera_feed():
    """Alternative route name for camera stream (for compatibility)"""
    return camera_stream()

@app.route('/get_live_detections')
def get_live_detections():
    """Get current live detection results"""
    global live_detections
    
    try:
        return jsonify({
            'success': True,
            'detections': live_detections if live_detections else []
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/get_available_cameras')
def get_available_cameras():
    """Get list of available cameras"""
    import cv2
    
    cameras = []
    for i in range(10):  # Check first 10 camera indices
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            cameras.append({
                'index': i,
                'name': f'Camera {i}',
                'id': f'camera_{i}'
            })
            cap.release()
        else:
            break  # Stop checking if camera doesn't exist
    
    return jsonify({
        'success': True,
        'cameras': cameras
    })

# Debug routes for camera testing
@app.route('/test_camera')
def test_camera():
    """Test camera access"""
    import cv2
    
    try:
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            return jsonify({'success': False, 'error': 'Cannot open camera'})
        
        ret, frame = cap.read()
        cap.release()
        
        if not ret:
            return jsonify({'success': False, 'error': 'Cannot read from camera'})
        
        return jsonify({
            'success': True, 
            'message': f'Camera working! Frame size: {frame.shape}'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/debug_live_status')
def debug_live_status():
    """Debug live detection status"""
    global live_camera_active, live_frame, live_detections
    
    return jsonify({
        'live_camera_active': live_camera_active,
        'live_frame_available': live_frame is not None,
        'live_detections_count': len(live_detections) if live_detections else 0,
        'available_models': get_available_models()
    })

def main():
    """Run the web application with optimizations"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Fast Object Detection Web Interface")
    parser.add_argument("--host", default="127.0.0.1", help="Host to bind to")
    parser.add_argument("--port", type=int, default=5000, help="Port to bind to")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    parser.add_argument("--threaded", action="store_true", default=True, help="Enable threading")
    args = parser.parse_args()
    
    print(f"🚀 Starting Fast Object Detection Web Interface")
    print(f"🔗 Access at: http://{args.host}:{args.port}")
    print(f"🎯 Device: {device}")
    print(f"⚡ Optimizations: Frame skipping, GPU acceleration, Model caching")
    print(f"📱 Features: File Upload, Live Camera, Performance Optimized")
      # Pre-load the fastest model for better first-time performance
    print("🔄 Pre-loading YOLOv8n model...")
    load_model('models/yolov8n.pt')
    print("✅ Ready to serve!")
    
    app.run(host=args.host, port=args.port, debug=args.debug, threaded=args.threaded)

if __name__ == "__main__":
    main()
