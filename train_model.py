#!/usr/bin/env python3
"""
YOLOv8 Model Training and Improvement System
===========================================

This script provides multiple approaches to improve object detection:
1. Fine-tune existing models on custom datasets
2. Train custom models for specific object classes
3. Data augmentation and dataset preparation
4. Model evaluation and comparison
"""

import os
import cv2
import yaml
import shutil
from pathlib import Path
from ultralytics import YOLO
import argparse
from datetime import datetime
import json

class ModelTrainer:
    """
    Class to handle YOLOv8 model training and improvement
    """
    
    def __init__(self, project_name="custom_training"):
        self.project_name = project_name
        self.project_dir = Path(f"training_projects/{project_name}")
        self.project_dir.mkdir(parents=True, exist_ok=True)
        
        # Create standard YOLO dataset structure
        self.dataset_dir = self.project_dir / "dataset"
        self.images_dir = self.dataset_dir / "images"
        self.labels_dir = self.dataset_dir / "labels"
        
        for split in ['train', 'val', 'test']:
            (self.images_dir / split).mkdir(parents=True, exist_ok=True)
            (self.labels_dir / split).mkdir(parents=True, exist_ok=True)
    
    def create_dataset_config(self, class_names, train_ratio=0.7, val_ratio=0.2):
        """
        Create dataset configuration file for YOLO training
        """
        config = {
            'path': str(self.dataset_dir.absolute()),
            'train': 'images/train',
            'val': 'images/val', 
            'test': 'images/test',
            'nc': len(class_names),
            'names': {i: name for i, name in enumerate(class_names)}
        }
        
        config_path = self.dataset_dir / "dataset.yaml"
        with open(config_path, 'w') as f:
            yaml.dump(config, f)
        
        print(f"📝 Dataset config created: {config_path}")
        return config_path
    
    def prepare_training_data(self, source_images_dir, source_labels_dir=None):
        """
        Prepare training data from source directory
        """
        print("📋 Preparing training data...")
        
        # If no labels provided, use label studio or manual annotation
        if source_labels_dir is None:
            print("⚠️  No labels directory provided. You'll need to annotate your images.")
            print("   Recommended tools:")
            print("   - LabelImg: https://github.com/tzutalin/labelImg")
            print("   - Label Studio: https://labelstud.io/")
            print("   - Roboflow: https://roboflow.com/")
            return False
        
        # Copy and organize images and labels
        # This is a simplified version - in practice you'd want more sophisticated data splitting
        
        return True
    
    def train_custom_model(self, base_model="yolov8n.pt", epochs=100, imgsz=640, batch=16):
        """
        Train a custom YOLOv8 model
        """
        print(f"🏋️ Starting training with {base_model}...")
        
        # Load base model
        model = YOLO(base_model)
        
        # Dataset config path
        dataset_config = self.dataset_dir / "dataset.yaml"
        
        if not dataset_config.exists():
            print("❌ Dataset config not found. Run create_dataset_config() first.")
            return None
        
        # Training arguments
        train_args = {
            'data': str(dataset_config),
            'epochs': epochs,
            'imgsz': imgsz,
            'batch': batch,
            'project': str(self.project_dir),
            'name': f'training_{datetime.now().strftime("%Y%m%d_%H%M%S")}',
            'save_period': 10,  # Save checkpoint every 10 epochs
            'device': 'cpu',  # Change to 'cuda' if GPU available
            'patience': 50,   # Early stopping patience
            'save': True,
            'plots': True,
        }
        
        try:
            # Start training
            results = model.train(**train_args)
            
            # Save training summary
            summary = {
                'base_model': base_model,
                'epochs': epochs,
                'final_weights': str(results.save_dir / 'weights' / 'best.pt'),
                'training_date': datetime.now().isoformat(),
                'dataset_path': str(dataset_config)
            }
            
            summary_path = self.project_dir / 'training_summary.json'
            with open(summary_path, 'w') as f:
                json.dump(summary, f, indent=2)
            
            print(f"✅ Training completed! Best weights saved to: {results.save_dir / 'weights' / 'best.pt'}")
            return results
            
        except Exception as e:
            print(f"❌ Training failed: {e}")
            return None
    
    def fine_tune_pretrained(self, base_model="yolov8s.pt", learning_rate=0.001, epochs=50):
        """
        Fine-tune a pretrained model with lower learning rate
        """
        print(f"🔧 Fine-tuning {base_model}...")
        
        model = YOLO(base_model)
        dataset_config = self.dataset_dir / "dataset.yaml"
        
        if not dataset_config.exists():
            print("❌ Dataset config not found.")
            return None
        
        # Fine-tuning with lower learning rate
        train_args = {
            'data': str(dataset_config),
            'epochs': epochs,
            'lr0': learning_rate,  # Lower learning rate for fine-tuning
            'project': str(self.project_dir),
            'name': f'finetune_{datetime.now().strftime("%Y%m%d_%H%M%S")}',
            'device': 'cpu',
            'patience': 25,
            'save': True,
            'plots': True,
        }
        
        try:
            results = model.train(**train_args)
            print(f"✅ Fine-tuning completed!")
            return results
        except Exception as e:
            print(f"❌ Fine-tuning failed: {e}")
            return None

class DatasetManager:
    """
    Utilities for dataset management and augmentation
    """
    
    @staticmethod
    def augment_images(source_dir, target_dir, augmentations_per_image=3):
        """
        Apply data augmentation to increase dataset size
        """
        print(f"🔄 Augmenting images from {source_dir}...")
        
        import albumentations as A
        
        # Define augmentation pipeline
        transform = A.Compose([
            A.HorizontalFlip(p=0.5),
            A.RandomBrightnessContrast(p=0.3),
            A.Rotate(limit=15, p=0.3),
            A.GaussNoise(p=0.2),
            A.Blur(blur_limit=3, p=0.2),
        ])
        
        # Process images
        source_path = Path(source_dir)
        target_path = Path(target_dir)
        target_path.mkdir(parents=True, exist_ok=True)
        
        for img_path in source_path.glob("*.jpg"):
            image = cv2.imread(str(img_path))
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            # Create augmented versions
            for i in range(augmentations_per_image):
                augmented = transform(image=image)['image']
                
                # Save augmented image
                aug_filename = f"{img_path.stem}_aug_{i}.jpg"
                aug_path = target_path / aug_filename
                
                augmented_bgr = cv2.cvtColor(augmented, cv2.COLOR_RGB2BGR)
                cv2.imwrite(str(aug_path), augmented_bgr)
        
        print(f"✅ Augmentation completed. Images saved to {target_dir}")

class ModelEvaluator:
    """
    Evaluate and compare different models
    """
    
    def __init__(self):
        self.results = {}
    
    def evaluate_model(self, model_path, test_images_dir, conf_threshold=0.25):
        """
        Evaluate a model on test images
        """
        print(f"📊 Evaluating model: {model_path}")
        
        model = YOLO(model_path)
        test_dir = Path(test_images_dir)
        
        total_detections = 0
        total_images = 0
        confidence_scores = []
        
        for img_path in test_dir.glob("*.jpg"):
            results = model(str(img_path), conf=conf_threshold)
            
            total_images += 1
            image_detections = len(results[0].boxes) if results[0].boxes is not None else 0
            total_detections += image_detections
            
            # Collect confidence scores
            if results[0].boxes is not None:
                confidences = results[0].boxes.conf.cpu().numpy()
                confidence_scores.extend(confidences)
        
        # Calculate metrics
        avg_detections_per_image = total_detections / total_images if total_images > 0 else 0
        avg_confidence = sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0
        
        evaluation_result = {
            'model_path': model_path,
            'total_images': total_images,
            'total_detections': total_detections,
            'avg_detections_per_image': avg_detections_per_image,
            'avg_confidence': avg_confidence,
            'confidence_threshold': conf_threshold
        }
        
        self.results[model_path] = evaluation_result
        
        print(f"  📈 Results:")
        print(f"     Total images processed: {total_images}")
        print(f"     Total detections: {total_detections}")
        print(f"     Average detections per image: {avg_detections_per_image:.2f}")
        print(f"     Average confidence: {avg_confidence:.3f}")
        
        return evaluation_result
    
    def compare_models(self, model_paths, test_images_dir):
        """
        Compare multiple models on the same test set
        """
        print("🔍 Comparing models...")
        
        for model_path in model_paths:
            self.evaluate_model(model_path, test_images_dir)
        
        # Print comparison
        print("\n📊 Model Comparison Summary:")
        print("=" * 80)
        print(f"{'Model':<30} {'Avg Detections':<15} {'Avg Confidence':<15}")
        print("-" * 80)
        
        for model_path, result in self.results.items():
            model_name = Path(model_path).name
            print(f"{model_name:<30} {result['avg_detections_per_image']:<15.2f} {result['avg_confidence']:<15.3f}")
        
        return self.results

def main():
    parser = argparse.ArgumentParser(description="YOLOv8 Model Training and Improvement")
    parser.add_argument("--action", choices=['train', 'finetune', 'evaluate', 'compare'], required=True,
                        help="Action to perform")
    parser.add_argument("--project_name", default="custom_training",
                        help="Name for the training project")
    parser.add_argument("--base_model", default="yolov8n.pt",
                        help="Base model to train from")
    parser.add_argument("--epochs", type=int, default=100,
                        help="Number of training epochs")
    parser.add_argument("--dataset_dir", 
                        help="Directory containing training dataset")
    parser.add_argument("--class_names", nargs='+',
                        help="List of class names for custom training")
    parser.add_argument("--test_images", 
                        help="Directory containing test images for evaluation")
    parser.add_argument("--models", nargs='+',
                        help="List of model paths for comparison")
    
    args = parser.parse_args()
    
    if args.action == 'train':
        if not args.class_names:
            print("❌ Class names required for training. Use --class_names")
            return
        
        trainer = ModelTrainer(args.project_name)
        config_path = trainer.create_dataset_config(args.class_names)
        
        if args.dataset_dir:
            trainer.prepare_training_data(args.dataset_dir)
        
        trainer.train_custom_model(args.base_model, args.epochs)
    
    elif args.action == 'finetune':
        trainer = ModelTrainer(args.project_name)
        trainer.fine_tune_pretrained(args.base_model, epochs=args.epochs)
    
    elif args.action == 'evaluate':
        if not args.models or not args.test_images:
            print("❌ Model path and test images directory required for evaluation")
            return
        
        evaluator = ModelEvaluator()
        for model_path in args.models:
            evaluator.evaluate_model(model_path, args.test_images)
    
    elif args.action == 'compare':
        if not args.models or not args.test_images:
            print("❌ Model paths and test images directory required for comparison")
            return
        
        evaluator = ModelEvaluator()
        evaluator.compare_models(args.models, args.test_images)

if __name__ == "__main__":
    main()
