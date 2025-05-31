#!/usr/bin/env python3
"""Script to show available YOLOv8 models and their capabilities"""

from ultralytics import YOLO
import os

def show_available_models():
    print("🤖 Available YOLOv8 Models:")
    print("=" * 50)
    
    models = {
        'yolov8n.pt': {
            'name': 'YOLOv8 Nano',
            'size': '~6MB',
            'speed': 'Fastest',
            'accuracy': 'Good',
            'description': 'Lightweight, fast inference'
        },
        'yolov8s.pt': {
            'name': 'YOLOv8 Small', 
            'size': '~22MB',
            'speed': 'Fast',
            'accuracy': 'Better',
            'description': 'Balanced speed and accuracy'
        },
        'yolov8m.pt': {
            'name': 'YOLOv8 Medium',
            'size': '~52MB', 
            'speed': 'Medium',
            'accuracy': 'Very Good',
            'description': 'Good balance for most use cases'
        },
        'yolov8l.pt': {
            'name': 'YOLOv8 Large',
            'size': '~87MB',
            'speed': 'Slower',
            'accuracy': 'Excellent', 
            'description': 'High accuracy applications'
        },
        'yolov8x.pt': {
            'name': 'YOLOv8 Extra Large',
            'size': '~131MB',
            'speed': 'Slowest',
            'accuracy': 'Best',
            'description': 'Maximum accuracy'
        }
    }
    
    for model_file, info in models.items():
        print(f"📦 {info['name']} ({model_file})")
        print(f"   Size: {info['size']}")
        print(f"   Speed: {info['speed']}")
        print(f"   Accuracy: {info['accuracy']}")
        print(f"   Use Case: {info['description']}")
        print()

def show_detectable_classes():
    print("🎯 Standard COCO Dataset Classes (80 objects):")
    print("=" * 50)
    
    # Load a model to get class names
    model = YOLO('yolov8n.pt')
    class_names = model.names
    
    # Group classes by category for better display
    categories = {
        'People & Body Parts': [0],  # person
        'Vehicles': [1, 2, 3, 5, 6, 7],  # bicycle, car, motorcycle, bus, train, truck
        'Animals': [14, 15, 16, 17, 18, 19, 20, 21, 22, 23],  # bird, cat, dog, horse, sheep, cow, elephant, bear, zebra, giraffe
        'Furniture': [56, 57, 58, 59, 60],  # chair, couch, potted plant, bed, dining table
        'Electronics': [62, 63, 64, 65, 66, 67, 72, 73, 74, 75, 76],  # tv, laptop, mouse, remote, keyboard, cell phone, microwave, oven, toaster, sink, refrigerator
        'Sports': [32, 33, 34, 35, 36, 37, 38],  # sports ball, kite, baseball bat, baseball glove, skateboard, surfboard, tennis racket
        'Food & Drinks': [41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53],  # banana, apple, sandwich, orange, broccoli, carrot, hot dog, pizza, donut, cake, chair, couch, potted plant
        'Household Items': [68, 69, 70, 71, 77, 78, 79],  # book, clock, vase, scissors, teddy bear, hair drier, toothbrush
        'Transportation': [4, 8, 9],  # airplane, boat, traffic light
        'Tools & Equipment': [39, 40, 54, 55, 61]  # bottle, wine glass, umbrella, handbag, tie
    }
    
    for category, class_ids in categories.items():
        print(f"📂 {category}:")
        for class_id in class_ids:
            if class_id in class_names:
                print(f"   • {class_names[class_id]} (ID: {class_id})")
        print()
    
    print(f"Total: {len(class_names)} object classes supported")

if __name__ == "__main__":
    show_available_models()
    print("\n" + "="*70 + "\n")
    show_detectable_classes()
