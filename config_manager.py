#!/usr/bin/env python3
"""
Configuration Management for Object Detection
Save and load detection settings, manage presets
"""

import json
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List

class ConfigManager:
    def __init__(self, config_dir="configs"):
        """Initialize configuration manager"""
        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(exist_ok=True)
        self.default_config_path = self.config_dir / "default.json"
        self.presets_dir = self.config_dir / "presets"
        self.presets_dir.mkdir(exist_ok=True)
        
        # Create default configuration if it doesn't exist
        if not self.default_config_path.exists():
            self.create_default_config()
    
    def create_default_config(self):
        """Create default configuration file"""
        default_config = {
            "model": {
                "path": "yolov8n.pt",
                "confidence": 0.25,
                "iou_threshold": 0.45,
                "max_detections": 300
            },
            "camera": {
                "index": 0,
                "resolution": [640, 480],
                "fps": 30
            },
            "output": {
                "save_annotated": True,
                "save_json": True,
                "count_objects": True,
                "output_dir": "output"
            },
            "video": {
                "frame_interval": 30,
                "save_frames": False,
                "output_fps": 30
            },
            "batch": {
                "parallel_processing": False,
                "max_workers": 4
            },
            "display": {
                "show_confidence": True,
                "show_labels": True,
                "bbox_thickness": 2,
                "font_scale": 0.8
            }
        }
        
        self.save_config(default_config, "default")
        return default_config
    
    def load_config(self, config_name="default"):
        """Load configuration from file"""
        if config_name == "default":
            config_path = self.default_config_path
        else:
            config_path = self.presets_dir / f"{config_name}.json"
        
        if not config_path.exists():
            print(f"❌ Configuration '{config_name}' not found")
            return self.create_default_config()
        
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
            print(f"✅ Loaded configuration: {config_name}")
            return config
        except Exception as e:
            print(f"❌ Error loading configuration: {e}")
            return self.create_default_config()
    
    def save_config(self, config, config_name="default"):
        """Save configuration to file"""
        # Add metadata
        config["metadata"] = {
            "created": datetime.now().isoformat(),
            "name": config_name,
            "version": "1.0"
        }
        
        if config_name == "default":
            config_path = self.default_config_path
        else:
            config_path = self.presets_dir / f"{config_name}.json"
        
        try:
            with open(config_path, 'w') as f:
                json.dump(config, f, indent=2)
            print(f"✅ Saved configuration: {config_name}")
            return True
        except Exception as e:
            print(f"❌ Error saving configuration: {e}")
            return False
    
    def list_presets(self):
        """List all available configuration presets"""
        presets = []
        
        # Add default config
        if self.default_config_path.exists():
            presets.append("default")
        
        # Add preset configs
        for preset_file in self.presets_dir.glob("*.json"):
            presets.append(preset_file.stem)
        
        return presets
    
    def delete_preset(self, preset_name):
        """Delete a configuration preset"""
        if preset_name == "default":
            print("❌ Cannot delete default configuration")
            return False
        
        preset_path = self.presets_dir / f"{preset_name}.json"
        
        if not preset_path.exists():
            print(f"❌ Preset '{preset_name}' not found")
            return False
        
        try:
            preset_path.unlink()
            print(f"✅ Deleted preset: {preset_name}")
            return True
        except Exception as e:
            print(f"❌ Error deleting preset: {e}")
            return False
    
    def create_preset(self, preset_name, base_config=None):
        """Create a new configuration preset"""
        if base_config is None:
            base_config = self.load_config("default")
        
        # Remove metadata before saving as new preset
        if "metadata" in base_config:
            del base_config["metadata"]
        
        return self.save_config(base_config, preset_name)
    
    def get_model_configs(self):
        """Get predefined model configurations"""
        return {
            "fast": {
                "path": "yolov8n.pt",
                "confidence": 0.25,
                "description": "Fastest inference, smaller model"
            },
            "balanced": {
                "path": "yolov8s.pt",
                "confidence": 0.25,
                "description": "Good balance of speed and accuracy"
            },
            "accurate": {
                "path": "yolov8m.pt",
                "confidence": 0.25,
                "description": "Better accuracy, slower inference"
            },
            "best": {
                "path": "yolov8l.pt",
                "confidence": 0.25,
                "description": "Best accuracy, slowest inference"
            }
        }
    
    def create_common_presets(self):
        """Create common configuration presets"""
        # High Accuracy Preset
        high_accuracy = self.load_config("default")
        high_accuracy["model"]["path"] = "yolov8m.pt"
        high_accuracy["model"]["confidence"] = 0.15
        high_accuracy["model"]["iou_threshold"] = 0.3
        self.save_config(high_accuracy, "high_accuracy")
        
        # Fast Processing Preset
        fast_processing = self.load_config("default")
        fast_processing["model"]["path"] = "yolov8n.pt"
        fast_processing["model"]["confidence"] = 0.4
        fast_processing["camera"]["resolution"] = [320, 240]
        fast_processing["video"]["frame_interval"] = 10
        self.save_config(fast_processing, "fast_processing")
        
        # Security Camera Preset
        security = self.load_config("default")
        security["model"]["path"] = "yolov8s.pt"
        security["model"]["confidence"] = 0.35
        security["camera"]["resolution"] = [1280, 720]
        security["video"]["frame_interval"] = 60
        security["output"]["save_annotated"] = True
        self.save_config(security, "security_camera")
        
        # Mobile/Laptop Preset
        mobile = self.load_config("default")
        mobile["model"]["path"] = "yolov8n.pt"
        mobile["model"]["confidence"] = 0.3
        mobile["camera"]["resolution"] = [480, 360]
        mobile["video"]["frame_interval"] = 15
        self.save_config(mobile, "mobile_friendly")
        
        print("✅ Created common presets: high_accuracy, fast_processing, security_camera, mobile_friendly")

def main():
    """Command line interface for configuration management"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Configuration Management")
    parser.add_argument("--list", action="store_true", help="List all presets")
    parser.add_argument("--show", type=str, help="Show configuration details")
    parser.add_argument("--create", type=str, help="Create new preset")
    parser.add_argument("--delete", type=str, help="Delete preset")
    parser.add_argument("--create-common", action="store_true", help="Create common presets")
    parser.add_argument("--models", action="store_true", help="Show model configurations")
    
    args = parser.parse_args()
    
    config_manager = ConfigManager()
    
    if args.list:
        presets = config_manager.list_presets()
        print("\n📋 Available Configuration Presets:")
        print("=" * 40)
        for preset in presets:
            config = config_manager.load_config(preset)
            model_path = config.get("model", {}).get("path", "unknown")
            confidence = config.get("model", {}).get("confidence", "unknown")
            print(f"  🔧 {preset}")
            print(f"     Model: {model_path}")
            print(f"     Confidence: {confidence}")
            print()
    
    elif args.show:
        config = config_manager.load_config(args.show)
        print(f"\n🔧 Configuration: {args.show}")
        print("=" * 40)
        print(json.dumps(config, indent=2))
    
    elif args.create:
        print(f"Creating new preset: {args.create}")
        config_manager.create_preset(args.create)
    
    elif args.delete:
        config_manager.delete_preset(args.delete)
    
    elif args.create_common:
        config_manager.create_common_presets()
    
    elif args.models:
        models = config_manager.get_model_configs()
        print("\n🔧 Available Model Configurations:")
        print("=" * 40)
        for name, config in models.items():
            print(f"  {name.upper()}: {config['path']}")
            print(f"    {config['description']}")
            print()
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
