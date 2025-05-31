#!/usr/bin/env python3
"""
Model Improvement Demo
======================

Demonstrates how different YOLOv8 models perform on the same images
to show recognition improvements
"""

import os
import cv2
from ultralytics import YOLO
from pathlib import Path
import time
import json
from datetime import datetime

class ModelComparison:
    def __init__(self):
        self.models = {
            'yolov8n.pt': {'name': 'Nano', 'size': '6MB', 'description': 'Fastest'},
            'yolov8s.pt': {'name': 'Small', 'size': '22MB', 'description': 'Balanced'},
            'yolov8m.pt': {'name': 'Medium', 'size': '52MB', 'description': 'Better Accuracy'},
            'yolov8l.pt': {'name': 'Large', 'size': '87MB', 'description': 'High Accuracy'},
            'yolov8x.pt': {'name': 'XLarge', 'size': '131MB', 'description': 'Maximum Accuracy'}
        }
        
        self.available_models = []
        self.check_available_models()
    
    def check_available_models(self):
        """Check which models are available locally"""
        print("🔍 Checking available models...")
        
        for model_file in self.models.keys():
            # Check in current directory
            if os.path.exists(model_file):
                self.available_models.append(model_file)
                print(f"  ✅ {model_file} found")
            # Check in models directory
            elif os.path.exists(f"models/{model_file}"):
                self.available_models.append(f"models/{model_file}")
                print(f"  ✅ models/{model_file} found")
        
        if not self.available_models:
            print("  ⚠️  No models found locally. Will download as needed.")
    
    def download_model(self, model_name):
        """Download a model if not available"""
        print(f"📥 Downloading {model_name}...")
        try:
            model = YOLO(model_name)
            # Move to models directory if it exists
            if os.path.exists("models") and os.path.exists(model_name):
                os.rename(model_name, f"models/{model_name}")
                return f"models/{model_name}"
            return model_name
        except Exception as e:
            print(f"❌ Failed to download {model_name}: {e}")
            return None
    
    def test_model_on_image(self, model_path, image_path, conf_threshold=0.25):
        """Test a single model on an image"""
        try:
            print(f"  🧪 Testing {os.path.basename(model_path)}...")
            
            start_time = time.time()
            model = YOLO(model_path)
            load_time = time.time() - start_time
            
            start_time = time.time()
            results = model(image_path, conf=conf_threshold, verbose=False)
            inference_time = time.time() - start_time
            
            # Extract detection info
            detections = []
            if results[0].boxes is not None:
                boxes = results[0].boxes
                for i in range(len(boxes)):
                    detection = {
                        'class': model.names[int(boxes.cls[i])],
                        'confidence': float(boxes.conf[i]),
                        'bbox': boxes.xyxy[i].tolist()
                    }
                    detections.append(detection)
            
            return {
                'model': os.path.basename(model_path),
                'detections': detections,
                'detection_count': len(detections),
                'load_time': load_time,
                'inference_time': inference_time,
                'total_time': load_time + inference_time
            }
            
        except Exception as e:
            print(f"    ❌ Error testing {model_path}: {e}")
            return None
    
    def compare_models_on_image(self, image_path, models_to_test=None, conf_threshold=0.25):
        """Compare multiple models on a single image"""
        if not os.path.exists(image_path):
            print(f"❌ Image not found: {image_path}")
            return
        
        print(f"\n🖼️  Testing models on: {image_path}")
        print("=" * 60)
        
        # Use available models if none specified
        if models_to_test is None:
            models_to_test = self.available_models
            
            # If no models available, download some basic ones
            if not models_to_test:
                basic_models = ['yolov8n.pt', 'yolov8s.pt']
                for model in basic_models:
                    downloaded = self.download_model(model)
                    if downloaded:
                        models_to_test.append(downloaded)
        
        results = []
        
        for model_path in models_to_test:
            if not os.path.exists(model_path):
                # Try to download
                model_name = os.path.basename(model_path)
                downloaded = self.download_model(model_name)
                if downloaded:
                    model_path = downloaded
                else:
                    continue
            
            result = self.test_model_on_image(model_path, image_path, conf_threshold)
            if result:
                results.append(result)
        
        # Display results
        self.display_comparison_results(results)
        
        return results
    
    def display_comparison_results(self, results):
        """Display comparison results in a formatted table"""
        if not results:
            print("❌ No results to display")
            return
        
        print(f"\n📊 DETECTION COMPARISON RESULTS")
        print("=" * 80)
        print(f"{'Model':<15} {'Objects':<8} {'Best Detection':<25} {'Confidence':<12} {'Time (s)':<10}")
        print("-" * 80)
        
        for result in sorted(results, key=lambda x: x['detection_count'], reverse=True):
            model_name = result['model'].replace('.pt', '').upper()
            
            if result['detections']:
                # Find highest confidence detection
                best_detection = max(result['detections'], key=lambda x: x['confidence'])
                best_class = best_detection['class']
                best_conf = best_detection['confidence']
                best_desc = f"{best_class}"
            else:
                best_desc = "No objects detected"
                best_conf = 0.0
            
            print(f"{model_name:<15} {result['detection_count']:<8} {best_desc:<25} {best_conf:<12.3f} {result['total_time']:<10.2f}")
        
        # Show detailed detections for best performing model
        best_model = max(results, key=lambda x: x['detection_count'])
        if best_model['detections']:
            print(f"\n🎯 DETAILED DETECTIONS ({best_model['model']}):")
            for i, det in enumerate(best_model['detections'], 1):
                print(f"  {i}. {det['class']} - {det['confidence']:.3f} confidence")
    
    def test_all_available_models(self, image_path, conf_threshold=0.25):
        """Test all available models on an image"""
        return self.compare_models_on_image(image_path, None, conf_threshold)
    
    def batch_test_images(self, images_dir, output_file="model_comparison_results.json"):
        """Test all images in a directory with all available models"""
        images_dir = Path(images_dir)
        if not images_dir.exists():
            print(f"❌ Directory not found: {images_dir}")
            return
        
        print(f"📁 Batch testing images in: {images_dir}")
        
        all_results = {}
        image_files = list(images_dir.glob("*.jpg")) + list(images_dir.glob("*.png"))
        
        for img_path in image_files:
            print(f"\n📸 Processing: {img_path.name}")
            results = self.test_all_available_models(str(img_path))
            all_results[str(img_path)] = results
        
        # Save results to JSON
        with open(output_file, 'w') as f:
            json.dump(all_results, f, indent=2, default=str)
        
        print(f"\n💾 Results saved to: {output_file}")
        return all_results
    
    def demonstrate_improvement(self, image_path):
        """Demonstrate how upgrading models improves detection"""
        print("\n🎯 DEMONSTRATING MODEL IMPROVEMENT")
        print("=" * 50)
        print("This shows how using larger/better models can detect more objects")
        print("and with higher confidence scores.\n")
        
        # Test with different models in order of capability
        model_progression = []
        for model_file in ['yolov8n.pt', 'yolov8s.pt', 'yolov8m.pt']:
            model_path = f"models/{model_file}" if os.path.exists(f"models/{model_file}") else model_file
            if os.path.exists(model_path):
                model_progression.append(model_path)
            else:
                # Try to download
                downloaded = self.download_model(model_file)
                if downloaded:
                    model_progression.append(downloaded)
        
        if not model_progression:
            print("❌ No models available for demonstration")
            return
        
        results = self.compare_models_on_image(image_path, model_progression)
        
        print(f"\n💡 IMPROVEMENT ANALYSIS:")
        if len(results) >= 2:
            worst_model = min(results, key=lambda x: x['detection_count'])
            best_model = max(results, key=lambda x: x['detection_count'])
            
            improvement = best_model['detection_count'] - worst_model['detection_count']
            if improvement > 0:
                print(f"  📈 Detection improvement: +{improvement} objects")
                print(f"  🥇 Best model: {best_model['model']} ({best_model['detection_count']} objects)")
                print(f"  🥉 Basic model: {worst_model['model']} ({worst_model['detection_count']} objects)")
            else:
                print(f"  ℹ️  All models detected similar number of objects")
                print(f"  💡 Try images with more complex scenes for better comparison")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="YOLOv8 Model Improvement Demo")
    parser.add_argument("--image", default="input/sample.jpg", help="Image to test")
    parser.add_argument("--batch_dir", help="Directory of images to batch test")
    parser.add_argument("--conf", type=float, default=0.25, help="Confidence threshold")
    parser.add_argument("--demo", action="store_true", help="Run improvement demonstration")
    
    args = parser.parse_args()
    
    comparator = ModelComparison()
    
    if args.batch_dir:
        comparator.batch_test_images(args.batch_dir)
    elif args.demo:
        comparator.demonstrate_improvement(args.image)
    else:
        comparator.test_all_available_models(args.image, args.conf)

if __name__ == "__main__":
    main()
