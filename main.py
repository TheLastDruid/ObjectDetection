

import os
import cv2
import torch
from ultralytics import YOLO
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import json
import argparse
from datetime import datetime

class ObjectDetector:
    """
    A class to perform object detection using YOLOv8 models.

    Handles loading models, running inference on images,
    drawing bounding boxes, and saving/displaying results.
    Supports both CPU and GPU inference.
    """

    def __init__(self, model_path='yolov8n.pt', conf_threshold=0.25, iou_threshold=0.7):
        """
        Initializes the ObjectDetector.

        Args:
            model_path (str): Path to the YOLOv8 model weights file (e.g., 'yolov8n.pt').
                              If the model is not found locally (within the container's accessible paths),
                              ultralytics will attempt to download it.
            conf_threshold (float): Confidence threshold for detections (0.0 to 1.0).
                                    Detections with confidence below this will be filtered.
            iou_threshold (float): IoU (Intersection over Union) threshold for NMS (Non-Maximum Suppression).
                                   Used to remove duplicate bounding boxes.
        """
        self.conf_threshold = conf_threshold
        self.iou_threshold = iou_threshold
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        print(f"Using device: {self.device}")

        # If a model path is specified that exists within the container (e.g., from mounted volume),
        # ultralytics will load it directly. Otherwise, it will try to download from Ultralytics Hub.
        try:
            self.model = YOLO(model_path)
            self.model.to(self.device)
            print(f"Model '{model_path}' loaded successfully.")
        except Exception as e:
            print(f"Error loading model '{model_path}': {e}")
            print("Attempting to download default 'yolov8n.pt' model if not found.")
            # This will download 'yolov8n.pt' if it's not present locally within the container
            self.model = YOLO('yolov8n.pt')
            self.model.to(self.device)
            print("Default 'yolov8n.pt' model ensured (downloaded if needed).")

    def detect_objects(self, image_path):
        """
        Runs object detection on a single image.

        Args:
            image_path (str): Path to the input image file (relative to container's /app).

        Returns:
            ultralytics.engine.results.Results: Detection results object.
            PIL.Image.Image: Original image loaded as a PIL Image.
            dict: Structured dictionary of detection data.
        """
        if not os.path.exists(image_path):
            print(f"Error: Image not found at {image_path}. Please ensure it's mounted correctly.")
            return None, None, {}

        # Load image using PIL for consistency with drawing later
        img_pil = Image.open(image_path).convert("RGB")
        img_np = np.array(img_pil)

        print(f"Running inference on {image_path}...")
        results = self.model.predict(
            source=img_np, # Pass numpy array directly to avoid path issues
            conf=self.conf_threshold,
            iou=self.iou_threshold,
            device=self.device,
            verbose=False
        )

        if results and len(results) > 0:
            result = results[0]
            detections_data = self._parse_detections(result, image_path) # Pass image_path here
            print(f"Detected {len(detections_data['detections'])} objects.")
            return result, img_pil, detections_data
        else:
            print("No detections found.")
            # Still return original image and an empty detections list for consistency
            return None, img_pil, {"image_path": image_path, "detections": []}

    def _parse_detections(self, result, original_image_path):
        """
        Parses the raw YOLOv8 detection results into a structured dictionary.

        Args:
            result (ultralytics.engine.results.Results): The raw detection result object.
            original_image_path (str): The path to the original image (used for reporting).

        Returns:
            dict: A dictionary containing image info and a list of detections.
        """
        detections = []
        names = result.names
        boxes = result.boxes

        for *xyxy, conf, cls in boxes.data:
            x1, y1, x2, y2 = map(int, xyxy)
            class_id = int(cls)
            class_name = names[class_id]
            confidence = float(conf)

            detections.append({
                "box_coordinates": [x1, y1, x2, y2],
                "class_id": class_id,
                "class_name": class_name,
                "confidence": confidence
            })
        return {
            "image_path": original_image_path, # Use the path passed to the method
            "image_width": result.orig_shape[1],
            "image_height": result.orig_shape[0],
            "detections": detections
        }

    def draw_boxes(self, pil_image, detections_data):
        """
        Draws bounding boxes, labels, and confidence scores on a PIL Image.
        (No changes needed here from previous version, as it operates on PIL objects directly)
        """
        draw = ImageDraw.Draw(pil_image)
        try:
            # Using a more robust font loading for Linux compatibility
            # This path is common for many Linux distros.
            # You might need to install 'fontconfig' on your host system if fonts are missing.
            font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
            if not os.path.exists(font_path):
                # Fallback if specific font not found or path is different
                font_path = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
                if not os.path.exists(font_path):
                    font = ImageFont.load_default()
                    print("Warning: Common truetype fonts not found, using default font.")
                else:
                    font = ImageFont.truetype(font_path, size=20)
            else:
                font = ImageFont.truetype(font_path, size=20)
        except Exception:
            font = ImageFont.load_default()
            print("Warning: Error loading truetype font, using default font.")


        colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (0, 255, 255), (255, 0, 255)]

        for det in detections_data['detections']:
            x1, y1, x2, y2 = det['box_coordinates']
            class_name = det['class_name']
            confidence = det['confidence']
            class_id = det['class_id']

            color = colors[class_id % len(colors)]

            draw.rectangle([x1, y1, x2, y2], outline=color, width=3)

            label = f"{class_name} ({confidence:.2f})"
            
            text_bbox = draw.textbbox((0,0), label, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]
            
            draw.rectangle([x1, y1 - text_height - 5, x1 + text_width + 5, y1], fill=color)
            draw.text((x1 + 2, y1 - text_height - 3), label, fill=(255, 255, 255), font=font)

        return pil_image

    def save_image(self, image, output_path):
        """
        Saves the annotated image to a specified path.
        (No changes needed here as it operates on PIL objects and standard paths)
        """
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        image.save(output_path)
        print(f"Annotated image saved to {output_path}")

    def display_image(self, image):
        """
        Displays the image using OpenCV.
        """
        img_cv2 = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        try:
            cv2.imshow("Detected Objects", img_cv2)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        except Exception as e:
            print(f"Could not display image: {e}")
            print("Consider using --save_annotated to save the image.")

    def capture_from_camera(self, camera_index=0):
        """
        Captures a single frame from the camera.
        
        Args:
            camera_index (int): Camera index (0 for default camera)
            
        Returns:
            PIL.Image.Image: Captured image as PIL Image, or None if capture failed
        """
        cap = cv2.VideoCapture(camera_index)
        
        if not cap.isOpened():
            print(f"Error: Could not open camera {camera_index}")
            return None
            
        print("Camera opened successfully. Taking photo...")
        
        # Let camera warm up
        for _ in range(5):
            cap.read()
            
        ret, frame = cap.read()
        cap.release()
        
        if ret:
            # Convert BGR to RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(frame_rgb)
            print("Photo captured successfully!")
            return pil_image
        else:
            print("Error: Could not capture frame from camera")
            return None

    def detect_objects_from_frame(self, frame):
        """
        Runs object detection on a camera frame (numpy array).
        
        Args:
            frame (numpy.ndarray): Camera frame in BGR format
            
        Returns:
            ultralytics.engine.results.Results: Detection results object.
            PIL.Image.Image: Original frame as PIL Image.
            dict: Structured dictionary of detection data.
        """
        # Convert BGR to RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(frame_rgb)
        
        results = self.model.predict(
            source=frame_rgb,
            conf=self.conf_threshold,
            iou=self.iou_threshold,
            device=self.device,
            verbose=False
        )
        
        if results and len(results) > 0:
            result = results[0]
            detections_data = self._parse_detections(result, "camera_frame")
            return result, img_pil, detections_data
        else:
            return None, img_pil, {"image_path": "camera_frame", "detections": []}

    def live_camera_detection(self, camera_index=0, save_detections=False, output_dir="output"):
        """
        Runs live object detection on camera feed.
        
        Args:
            camera_index (int): Camera index (0 for default camera)
            save_detections (bool): Whether to save detected frames
            output_dir (str): Directory to save detected frames
        """
        cap = cv2.VideoCapture(camera_index)
        
        if not cap.isOpened():
            print(f"Error: Could not open camera {camera_index}")
            return
            
        print("Starting live camera detection...")
        print("Press 'q' to quit, 's' to save current frame, 'c' to capture and save with timestamp")
        
        frame_count = 0
        
        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    print("Error: Could not read frame from camera")
                    break
                
                # Run detection
                result, img_pil, detections_data = self.detect_objects_from_frame(frame)
                
                # Draw bounding boxes on the frame
                if detections_data['detections']:
                    annotated_img = self.draw_boxes(img_pil.copy(), detections_data)
                    display_frame = cv2.cvtColor(np.array(annotated_img), cv2.COLOR_RGB2BGR)
                    
                    # Add detection info to frame
                    info_text = f"Objects: {len(detections_data['detections'])}"
                    cv2.putText(display_frame, info_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                else:
                    display_frame = frame
                    cv2.putText(display_frame, "No objects detected", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                
                # Add instructions
                cv2.putText(display_frame, "Press 'q' to quit, 's' to save, 'c' to capture", (10, display_frame.shape[0] - 20), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
                
                cv2.imshow("Live Object Detection", display_frame)
                
                key = cv2.waitKey(1) & 0xFF
                
                if key == ord('q'):
                    print("Quitting live detection...")
                    break
                elif key == ord('s') and detections_data['detections']:
                    # Save current frame with detections
                    if save_detections:
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        output_path = os.path.join(output_dir, f"live_detection_{timestamp}.jpg")
                        annotated_img = self.draw_boxes(img_pil.copy(), detections_data)
                        self.save_image(annotated_img, output_path)
                        print(f"Frame saved to {output_path}")
                elif key == ord('c'):
                    # Capture and save frame regardless of detections
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    output_path = os.path.join(output_dir, f"camera_capture_{timestamp}.jpg")
                    if detections_data['detections']:
                        annotated_img = self.draw_boxes(img_pil.copy(), detections_data)
                        self.save_image(annotated_img, output_path)
                    else:
                        self.save_image(img_pil, output_path)
                    print(f"Frame captured and saved to {output_path}")
                    
                    # Also save JSON report if there are detections
                    if detections_data['detections']:
                        json_path = os.path.join(output_dir, f"camera_capture_{timestamp}_report.json")
                        detections_data['timestamp'] = timestamp
                        with open(json_path, 'w') as f:
                            json.dump(detections_data, f, indent=4)
                        print(f"Detection report saved to {json_path}")
                
                frame_count += 1
                
        except KeyboardInterrupt:
            print("\nInterrupted by user")
        finally:
            cap.release()
            cv2.destroyAllWindows()
            print("Camera released and windows closed")


    def generate_json_report(self, detections_data, output_dir, original_filename):
        """
        Generates and saves a JSON report of detections.
        """
        output_filename = os.path.join(output_dir, f"{os.path.splitext(original_filename)[0]}_report.json")
        os.makedirs(os.path.dirname(output_filename), exist_ok=True) # Ensure output dir exists
        with open(output_filename, 'w') as f:
            json.dump(detections_data, f, indent=4)
        print(f"JSON report saved to {output_filename}")

    def count_objects(self, detections_data):
        """
        Counts objects by category.
        """
        counts = {}
        for det in detections_data['detections']:
            class_name = det['class_name']
            counts[class_name] = counts.get(class_name, 0) + 1
        return counts

def main():
    parser = argparse.ArgumentParser(description="Run YOLOv8 object detection on images or camera.")
    parser.add_argument("--image_path", type=str, default="input/sample.jpg",
                        help="Path to the input image or a folder of images.")
    parser.add_argument("--output_dir", type=str, default="output",
                        help="Directory to save annotated images and reports.")
    parser.add_argument("--model", type=str, default=os.getenv("YOLO_MODEL_PATH", "yolov8n.pt"),
                        help="Path to YOLOv8 model weights (e.g., yolov8n.pt, yolov8s.pt, custom_model.pt).")
    parser.add_argument("--conf", type=float, default=0.5,
                        help="Confidence threshold for detections (0.0 to 1.0).")
    parser.add_argument("--iou", type=float, default=0.7,
                        help="IoU threshold for Non-Maximum Suppression (NMS).")
    parser.add_argument("--save_annotated", action="store_true",
                        help="Save the annotated image(s).")
    parser.add_argument("--display", action="store_true",
                        help="Display the annotated image(s) after processing.")
    parser.add_argument("--save_json", action="store_true",
                        help="Save a JSON report of detections.")
    parser.add_argument("--count_objects", action="store_true",
                        help="Print object counts by category.")
    
    # Camera-related arguments
    parser.add_argument("--camera", action="store_true",
                        help="Capture a single photo from camera instead of using image file.")
    parser.add_argument("--live_camera", action="store_true",
                        help="Start live camera detection mode.")
    parser.add_argument("--camera_index", type=int, default=0,
                        help="Camera index to use (0 for default camera).")

    args = parser.parse_args()

    detector = ObjectDetector(model_path=args.model,
                              conf_threshold=args.conf,
                              iou_threshold=args.iou)

    # Ensure output directory exists
    os.makedirs(args.output_dir, exist_ok=True)

    # Handle camera modes
    if args.live_camera:
        print("Starting live camera detection mode...")
        detector.live_camera_detection(
            camera_index=args.camera_index,
            save_detections=args.save_annotated,
            output_dir=args.output_dir
        )
        return
    
    if args.camera:
        print(f"Capturing photo from camera {args.camera_index}...")
        captured_image = detector.capture_from_camera(args.camera_index)
        
        if captured_image is None:
            print("Failed to capture image from camera")
            return
            
        # Save the captured image
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        captured_path = os.path.join(args.output_dir, f"camera_capture_{timestamp}.jpg")
        captured_image.save(captured_path)
        print(f"Captured image saved to {captured_path}")
        
        # Run detection on captured image
        # Convert PIL to numpy for detection
        img_np = np.array(captured_image)
        
        results = detector.model.predict(
            source=img_np,
            conf=detector.conf_threshold,
            iou=detector.iou_threshold,
            device=detector.device,
            verbose=False
        )
        
        if results and len(results) > 0:
            result = results[0]
            detections_data = detector._parse_detections(result, captured_path)
            print(f"Detected {len(detections_data['detections'])} objects.")
            
            # Process the captured image like a regular image
            if detections_data['detections']:
                annotated_image = detector.draw_boxes(captured_image.copy(), detections_data)
                
                if args.save_annotated:
                    output_image_path = os.path.join(args.output_dir, f"camera_capture_{timestamp}_detected.jpg")
                    detector.save_image(annotated_image, output_image_path)
                
                if args.display:
                    detector.display_image(annotated_image)
                
                if args.save_json:
                    json_path = os.path.join(args.output_dir, f"camera_capture_{timestamp}_report.json")
                    detections_data['timestamp'] = timestamp
                    with open(json_path, 'w') as f:
                        json.dump(detections_data, f, indent=4)
                    print(f"JSON report saved to {json_path}")
                
                if args.count_objects:
                    counts = detector.count_objects(detections_data)
                    print("\nObject Counts:")
                    if counts:
                        for obj_name, count in counts.items():
                            print(f"- {obj_name}: {count}")
                    else:
                        print("No objects detected to count.")
            else:
                print("No objects detected in captured image.")
                if args.display:
                    detector.display_image(captured_image)
        
        return

    # Original file-based processing
    if os.path.isdir(args.image_path):
        print(f"Processing images in folder: {args.image_path}")
        image_files = [os.path.join(args.image_path, f) for f in os.listdir(args.image_path)
                       if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff'))]
        if not image_files:
            print(f"No image files found in {args.image_path}. Please ensure your input folder contains images.")
            return

        for img_file in image_files:
            process_single_image(detector, img_file, args)
            print("-" * 50)

    elif os.path.isfile(args.image_path):
        print(f"Processing single image: {args.image_path}")
        process_single_image(detector, args.image_path, args)
    else:
        print(f"Invalid input path: {args.image_path}. Please provide a valid image file or directory, or use --camera or --live_camera for camera input.")


def process_single_image(detector, current_image_path, args):
    """Helper function to process a single image based on main arguments."""
    base_filename = os.path.basename(current_image_path)
    name_without_ext = os.path.splitext(base_filename)[0]

    result, original_pil_img, detections_data = detector.detect_objects(current_image_path)

    if original_pil_img:
        annotated_image = detector.draw_boxes(original_pil_img.copy(), detections_data)

        if args.save_annotated:
            # Construct output path relative to container's output_dir
            output_image_path = os.path.join(args.output_dir, f"{name_without_ext}_detected.jpg")
            detector.save_image(annotated_image, output_image_path)

        if args.display:
            detector.display_image(annotated_image)

        if args.save_json:
            detector.generate_json_report(detections_data, args.output_dir, base_filename)

        if args.count_objects:
            counts = detector.count_objects(detections_data)
            print("\nObject Counts:")
            if counts:
                for obj_name, count in counts.items():
                    print(f"- {obj_name}: {count}")
            else:
                print("No objects detected to count.")


if __name__ == "__main__":
    main()