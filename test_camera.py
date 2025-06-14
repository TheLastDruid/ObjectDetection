import cv2
import time

def test_camera_stream():
    print("Testing camera streaming...")
    
    # Test basic camera access
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("❌ Cannot open camera")
        return False
    
    print("✅ Camera opened successfully")
    
    # Test reading frames
    ret, frame = cap.read()
    if not ret:
        print("❌ Cannot read frames from camera")
        cap.release()
        return False
    
    print(f"✅ Frame captured: {frame.shape}")
    
    # Test streaming for a few frames
    frame_count = 0
    start_time = time.time()
    
    while frame_count < 10:
        ret, frame = cap.read()
        if ret:
            frame_count += 1
            # Encode to JPEG
            _, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()
            print(f"Frame {frame_count}: {len(frame_bytes)} bytes")
        else:
            print(f"❌ Failed to read frame {frame_count}")
            break
    
    elapsed = time.time() - start_time
    fps = frame_count / elapsed
    print(f"✅ Captured {frame_count} frames in {elapsed:.2f}s ({fps:.1f} FPS)")
    
    cap.release()
    return True

if __name__ == "__main__":
    test_camera_stream()
