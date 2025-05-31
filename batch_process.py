#!/usr/bin/env python3
"""
Batch processing script for object detection
Processes multiple images or videos at once
"""

import os
import sys
import argparse
import cv2
import json
import time
from pathlib import Path
from datetime import datetime
from ultralytics import YOLO

class BatchProcessor:
    def __init__(self, model_path="yolov8n.pt", confidence=0.25):
        """Initialize batch processor with YOLO model"""
        self.model = YOLO(model_path)
        self.model_path = model_path
        self.confidence = confidence
        self.supported_image_formats = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp'}
        self.supported_video_formats = {'.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv'}
        
    def process_images_batch(self, input_dir, output_dir, save_annotated=True, save_json=True):
        """Process all images in a directory"""
        input_path = Path(input_dir)
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        # Find all image files
        image_files = []
        for ext in self.supported_image_formats:
            image_files.extend(input_path.glob(f"*{ext}"))
            image_files.extend(input_path.glob(f"*{ext.upper()}"))
        
        if not image_files:
            print(f"❌ No image files found in {input_dir}")
            return
        
        print(f"📁 Found {len(image_files)} images to process")
        print(f"🎯 Using model: {self.model_path}")
        print(f"📤 Output directory: {output_dir}")
        print("-" * 50)
        
        results_summary = []
        start_time = time.time()
        
        for i, img_file in enumerate(image_files, 1):
            print(f"🔍 Processing {i}/{len(image_files)}: {img_file.name}")
            
            try:
                # Run detection
                results = self.model(str(img_file), conf=self.confidence)
                result = results[0]
                
                # Prepare file names
                base_name = img_file.stem
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                
                # Save annotated image
                if save_annotated:
                    annotated_path = output_path / f"{base_name}_detected.jpg"
                    annotated_img = result.plot()
                    cv2.imwrite(str(annotated_path), annotated_img)
                
                # Prepare detection data
                detection_data = {
                    "timestamp": timestamp,
                    "source_file": str(img_file),
                    "model_used": self.model_path,
                    "confidence_threshold": self.confidence,
                    "objects_detected": len(result.boxes) if result.boxes is not None else 0,
                    "detections": []
                }
                
                # Process each detection
                if result.boxes is not None:
                    for box in result.boxes:
                        class_id = int(box.cls[0])
                        confidence = float(box.conf[0])
                        class_name = self.model.names[class_id]
                        bbox = box.xyxy[0].tolist()
                        
                        detection_data["detections"].append({
                            "class": class_name,
                            "confidence": confidence,
                            "bbox": {
                                "x1": bbox[0], "y1": bbox[1],
                                "x2": bbox[2], "y2": bbox[3]
                            }
                        })
                
                # Save JSON report
                if save_json:
                    json_path = output_path / f"{base_name}_report.json"
                    with open(json_path, 'w') as f:
                        json.dump(detection_data, f, indent=2)
                
                # Add to summary
                results_summary.append({
                    "file": img_file.name,
                    "objects_found": detection_data["objects_detected"],
                    "top_detection": detection_data["detections"][0]["class"] if detection_data["detections"] else "None"
                })
                
                print(f"   ✅ Found {detection_data['objects_detected']} objects")
                
            except Exception as e:
                print(f"   ❌ Error processing {img_file.name}: {str(e)}")
                results_summary.append({
                    "file": img_file.name,
                    "objects_found": 0,
                    "error": str(e)
                })
        
        # Save batch summary
        end_time = time.time()
        total_time = end_time - start_time
        
        batch_summary = {
            "timestamp": datetime.now().isoformat(),
            "total_images": len(image_files),
            "processing_time_seconds": total_time,
            "average_time_per_image": total_time / len(image_files),
            "model_used": self.model_path,
            "confidence_threshold": self.confidence,
            "results": results_summary
        }
        
        summary_path = output_path / f"batch_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(summary_path, 'w') as f:
            json.dump(batch_summary, f, indent=2)
        
        # Print summary
        print("-" * 50)
        print(f"🎉 Batch processing complete!")
        print(f"📊 Processed {len(image_files)} images in {total_time:.1f} seconds")
        print(f"⚡ Average: {total_time/len(image_files):.2f} seconds per image")
        print(f"📄 Summary saved to: {summary_path}")
        
        return batch_summary

def main():
    parser = argparse.ArgumentParser(description="Batch Object Detection")
    parser.add_argument("--input", type=str, required=True, help="Input directory (for images) or file path (for video)")
    parser.add_argument("--output", type=str, default="output", help="Output directory")
    parser.add_argument("--model", type=str, default="yolov8n.pt", help="Model path")
    parser.add_argument("--confidence", type=float, default=0.25, help="Confidence threshold")
    parser.add_argument("--mode", choices=["images", "video"], default="images", help="Processing mode")
    parser.add_argument("--no-annotated", action="store_true", help="Skip saving annotated images")
    parser.add_argument("--no-json", action="store_true", help="Skip saving JSON reports")
    
    args = parser.parse_args()
    
    processor = BatchProcessor(args.model, args.confidence)
    
    if args.mode == "images":
        processor.process_images_batch(
            args.input, 
            args.output,
            save_annotated=not args.no_annotated,
            save_json=not args.no_json
        )

if __name__ == "__main__":
    main()
