"""
Motion Detection Manager for Magic Mirror Application
H        # Notification control - only send ONE notification per motion event
        self.motion_notification_sent = False  # Track if notification was sent for current motion
        self.last_notification_time = 0
        
        # Motion state change callbacks for video recording, etc.
        self.motion_state_callbacks = []
        
        # Performance monitorings advanced motion detection with bounding boxes and camera stabilization
"""

import cv2
import numpy as np
from typing import List, Dict, Tuple, Optional, Callable
import threading
import time
from datetime import datetime
import config


class MotionDetectionManager:
    """Manages advanced motion detection with bounding boxes and stabilization"""
    
    def __init__(self, notification_callback: Optional[Callable] = None):
        """
        Initialize the motion detection manager
        
        Args:
            notification_callback: Callback function for motion detection events
        """
        self.notification_callback = notification_callback
        self.is_active = False
        self.detection_thread = None
        
        # Motion detection parameters
        self.background_subtractor = cv2.createBackgroundSubtractorMOG2(
            history=500,
            varThreshold=16,  # Lower threshold for better sensitivity
            detectShadows=True
        )
        
        # Motion detection settings
        self.min_contour_area = 200  # Much lower minimum area for higher sensitivity
        self.max_objects = config.MOTION_MAX_OBJECTS
        self.confidence_threshold = 0.02  # Even lower threshold for maximum sensitivity
        
        # Remove human detection - focus on motion only
        self.human_detection_enabled = False
        
        # Stabilization for camera jiggle compensation
        self.stabilization_enabled = config.MOTION_STABILIZATION_ENABLED
        self.prev_frame = None
        self.motion_history = []
        
        # Current motion state with inertia
        self.current_motion_boxes = []
        self.current_confidence = 0.0
        self.motion_detected = False
        self.last_motion_time = None
        self.last_no_motion_time = None
        
        # Inertia settings
        self.motion_detection_delay = 2.0  # 2 seconds to confirm motion
        self.motion_clear_delay = 10.0     # 10 seconds to clear motion (inertia)
        self.motion_start_time = None      # When motion first detected
        self.no_motion_start_time = None   # When no motion first detected
        
        # Notification control - only send ONE notification per motion event
        self.motion_notification_sent = False  # Track if notification was sent for current motion
        self.last_notification_time = 0
        
        # Performance tracking
        self.frame_count = 0
        self.fps_counter = 0
        self.last_fps_time = time.time()
        
        print("[Motion Detection] Initialized with advanced algorithms")
    
    def start_detection(self):
        """Start motion detection processing"""
        if self.is_active:
            return
        
        self.is_active = True
        print("[Motion Detection] Started motion detection")
        
    def stop_detection(self):
        """Stop motion detection processing"""
        if not self.is_active:
            return
        
        self.is_active = False
        print("[Motion Detection] Stopped motion detection")
    
    def process_frame(self, frame: np.ndarray) -> Tuple[np.ndarray, Dict]:
        """
        Process a frame for motion detection
        
        Args:
            frame: Input video frame (BGR format)
            
        Returns:
            tuple: (processed_frame_with_boxes, motion_data)
        """
        if not self.is_active:
            return frame, self._get_empty_motion_data()
        
        try:
            # Performance tracking
            self._update_fps_counter()
            
            # Apply stabilization if enabled
            if self.stabilization_enabled:
                frame = self._stabilize_frame(frame)
            
            # Convert to grayscale for motion detection
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Apply Gaussian blur to reduce noise
            blurred = cv2.GaussianBlur(gray_frame, (15, 15), 0)  # Reduced blur for more sensitivity
            
            # Background subtraction
            fg_mask = self.background_subtractor.apply(blurred)
            
            # Morphological operations to clean up the mask (reduced for sensitivity)
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 2))
            fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_OPEN, kernel)
            fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_CLOSE, kernel)
            
            # Find contours
            contours, _ = cv2.findContours(fg_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            # Process contours and generate bounding boxes
            motion_boxes = self._process_contours(contours)
            
            # Calculate confidence score
            confidence = self._calculate_confidence(motion_boxes, fg_mask)
            
            # Enhanced motion detection logic with inertia
            motion_detected = self._determine_motion_state_with_inertia(motion_boxes, confidence)
            
            # Update motion state
            self._update_motion_state(motion_boxes, confidence, motion_detected)
            
            # Draw bounding boxes on frame
            processed_frame = self._draw_motion_boxes(frame.copy(), motion_boxes, confidence)
            
            # Create motion data
            motion_data = {
                'boxes': motion_boxes,
                'confidence': confidence,
                'motion_detected': self.motion_detected,
                'timestamp': datetime.now(),
                'frame_count': self.frame_count,
                'fps': self.fps_counter
            }
            
            # Trigger notification ONLY ONCE when motion is first confirmed
            if self.motion_detected and self.notification_callback and not self.motion_notification_sent:
                print(f"[Motion Detection] Sending SINGLE notification for motion event")
                self._trigger_motion_notification(motion_data)
                self.motion_notification_sent = True  # Mark notification as sent for this motion event
                self.last_notification_time = time.time()
            
            return processed_frame, motion_data
            
        except Exception as e:
            print(f"[Motion Detection] Error processing frame: {e}")
            return frame, self._get_empty_motion_data()
    
    def _stabilize_frame(self, frame: np.ndarray) -> np.ndarray:
        """
        Apply basic frame stabilization to compensate for camera jiggle
        
        Args:
            frame: Input frame
            
        Returns:
            Stabilized frame
        """
        if self.prev_frame is None:
            self.prev_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            return frame
        
        try:
            # Convert current frame to grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Calculate optical flow for stabilization
            # Detect corners in previous frame
            corners = cv2.goodFeaturesToTrack(
                self.prev_frame,
                maxCorners=200,
                qualityLevel=0.01,
                minDistance=30,
                blockSize=3
            )
            
            if corners is not None and len(corners) > 10:
                # Calculate optical flow
                new_corners, status, _ = cv2.calcOpticalFlowPyrLK(
                    self.prev_frame, gray, corners, None
                )
                
                # Filter good points
                good_old = corners[status == 1]
                good_new = new_corners[status == 1]
                
                if len(good_old) > 10:
                    # Calculate transformation matrix
                    transform = cv2.estimateAffinePartial2D(good_old, good_new)[0]
                    
                    if transform is not None:
                        # Apply inverse transformation to stabilize
                        h, w = frame.shape[:2]
                        stabilized = cv2.warpAffine(frame, transform, (w, h))
                        
                        self.prev_frame = gray
                        return stabilized
            
            self.prev_frame = gray
            return frame
            
        except Exception as e:
            print(f"[Motion Detection] Stabilization error: {e}")
            self.prev_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            return frame
    
    def _process_contours(self, contours: List) -> List[Dict]:
        """
        Process contours to generate motion bounding boxes
        
        Args:
            contours: List of detected contours
            
        Returns:
            List of motion box dictionaries
        """
        motion_boxes = []
        
        # Sort contours by area (largest first)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)
        
        for contour in contours[:self.max_objects]:
            area = cv2.contourArea(contour)
            
            if area > self.min_contour_area:
                # Get bounding rectangle
                x, y, w, h = cv2.boundingRect(contour)
                
                # More lenient filtering for higher sensitivity
                aspect_ratio = w / h if h > 0 else 0
                if w < 10 or h < 10 or aspect_ratio > 10 or aspect_ratio < 0.1:
                    continue
                
                # Calculate motion properties
                motion_box = {
                    'x': x,
                    'y': y,
                    'width': w,
                    'height': h,
                    'area': area,
                    'center': (x + w // 2, y + h // 2),
                    'confidence': min(area / (w * h), 1.0)  # Density-based confidence
                }
                
                motion_boxes.append(motion_box)
        
        return motion_boxes
    
    def _determine_motion_state_with_inertia(self, motion_boxes: List[Dict], confidence: float) -> bool:
        """
        Determine if legitimate motion is detected with inertia logic
        
        Args:
            motion_boxes: Detected motion boxes
            confidence: Motion confidence score
            
        Returns:
            True if motion should be considered detected
        """
        current_time = time.time()
        
        # Basic motion detection - more sensitive thresholds
        has_significant_motion = len(motion_boxes) > 0 and confidence > self.confidence_threshold
        
        # Additional check for total motion area (reduced threshold)
        if has_significant_motion and motion_boxes:
            total_area = sum(box['area'] for box in motion_boxes)
            if total_area < 300:  # Reduced from 500 for higher sensitivity
                has_significant_motion = False
        
        # Inertia logic for motion detection
        if has_significant_motion:
            # Motion detected in current frame
            if self.motion_start_time is None:
                self.motion_start_time = current_time
                print(f"[Motion Detection] Motion activity started - Confidence: {confidence:.3f}")
            
            # Reset no-motion timer
            self.no_motion_start_time = None
            
            # Confirm motion after delay
            if not self.motion_detected and (current_time - self.motion_start_time) >= self.motion_detection_delay:
                print(f"[Motion Detection] Motion CONFIRMED after {self.motion_detection_delay}s - Confidence: {confidence:.3f}")
                self.motion_notification_sent = False  # Reset notification flag for new motion event
                return True
            elif self.motion_detected:
                # Motion already detected, keep it active
                return True
        else:
            # No motion detected in current frame
            if self.no_motion_start_time is None and self.motion_detected:
                self.no_motion_start_time = current_time
                print(f"[Motion Detection] No motion activity started - will clear in {self.motion_clear_delay}s")
            
            # Reset motion start timer
            self.motion_start_time = None
            
            # Clear motion after delay (inertia)
            if self.motion_detected and self.no_motion_start_time:
                if (current_time - self.no_motion_start_time) >= self.motion_clear_delay:
                    print(f"[Motion Detection] Motion CLEARED after {self.motion_clear_delay}s of inactivity")
                    self.no_motion_start_time = None
                    self.motion_notification_sent = False  # Reset for next motion event
                    return False
                else:
                    # Still in inertia period, keep motion active
                    return True
        
        return self.motion_detected
    
    def _calculate_confidence(self, motion_boxes: List[Dict], fg_mask: np.ndarray) -> float:
        """
        Calculate overall motion detection confidence
        
        Args:
            motion_boxes: List of detected motion boxes
            fg_mask: Foreground mask from background subtraction
            
        Returns:
            Confidence score (0.0 to 1.0)
        """
        if not motion_boxes:
            return 0.0
        
        # Calculate confidence based on motion area and intensity
        total_area = sum(box['area'] for box in motion_boxes)
        frame_area = fg_mask.shape[0] * fg_mask.shape[1]
        area_ratio = min(total_area / frame_area, 1.0)
        
        # Calculate average intensity in motion areas
        motion_intensity = np.sum(fg_mask) / (frame_area * 255)
        
        # Combine metrics for overall confidence
        confidence = (area_ratio * 0.6 + motion_intensity * 0.4)
        
        return min(confidence, 1.0)
    
    def _update_motion_state(self, motion_boxes: List[Dict], confidence: float, motion_detected: bool):
        """
        Update internal motion state
        
        Args:
            motion_boxes: Current motion boxes
            confidence: Motion confidence score
            motion_detected: Whether motion is detected (from inertia logic)
        """
        self.current_motion_boxes = motion_boxes
        self.current_confidence = confidence
        
        # Update motion detection state (controlled by inertia logic)
        prev_motion_state = self.motion_detected
        self.motion_detected = motion_detected
        
        # Log state changes
        if prev_motion_state != self.motion_detected:
            if self.motion_detected:
                print(f"[Motion Detection] STATE CHANGE: Motion ACTIVE - Confidence: {confidence:.3f}, Boxes: {len(motion_boxes)}")
            else:
                print(f"[Motion Detection] STATE CHANGE: Motion INACTIVE")
        
        # Update motion history for pattern analysis
        self.motion_history.append({
            'timestamp': time.time(),
            'boxes': len(motion_boxes),
            'confidence': confidence,
            'detected': self.motion_detected,
            'raw_motion': len(motion_boxes) > 0  # Raw motion without inertia
        })
        
        # Keep only recent history (last 100 frames)
        if len(self.motion_history) > 100:
            self.motion_history.pop(0)
        
        # Notify registered callbacks of motion state changes
        if prev_motion_state != self.motion_detected:
            self._notify_motion_state_callbacks(prev_motion_state, self.motion_detected)
    
    def add_motion_state_callback(self, callback: Callable[[bool, bool], None]):
        """
        Add a callback for motion state changes
        
        Args:
            callback: Function to call when motion state changes
                     Parameters: (previous_state, current_state)
        """
        if callback not in self.motion_state_callbacks:
            self.motion_state_callbacks.append(callback)
            print(f"[Motion Detection] Added motion state callback: {callback.__name__}")
    
    def remove_motion_state_callback(self, callback: Callable[[bool, bool], None]):
        """
        Remove a motion state callback
        
        Args:
            callback: Function to remove from callbacks
        """
        if callback in self.motion_state_callbacks:
            self.motion_state_callbacks.remove(callback)
            print(f"[Motion Detection] Removed motion state callback: {callback.__name__}")
    
    def _notify_motion_state_callbacks(self, previous_state: bool, current_state: bool):
        """
        Notify all registered callbacks of motion state changes
        
        Args:
            previous_state: Previous motion detection state
            current_state: Current motion detection state
        """
        for callback in self.motion_state_callbacks:
            try:
                callback(previous_state, current_state)
            except Exception as e:
                print(f"[Motion Detection] Error in motion state callback {callback.__name__}: {e}")
    
    def _draw_motion_boxes(self, frame: np.ndarray, motion_boxes: List[Dict], confidence: float) -> np.ndarray:
        """
        Draw motion detection bounding boxes on frame
        
        Args:
            frame: Input frame
            motion_boxes: List of motion boxes to draw
            confidence: Overall confidence score
            
        Returns:
            Frame with motion boxes drawn
        """
        # Draw motion bounding boxes with bright, distinct colors
        for i, box in enumerate(motion_boxes):
            x, y, w, h = box['x'], box['y'], box['width'], box['height']
            box_confidence = box['confidence']
            
            # Use bright colors for better visibility
            if box_confidence > 0.8:
                color = (0, 255, 255)  # Bright yellow for high confidence
            elif box_confidence > 0.5:
                color = (255, 255, 0)  # Cyan for medium confidence
            else:
                color = (255, 0, 255)  # Magenta for low confidence
            
            # Draw bounding rectangle with thicker lines
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 3)
            
            # Draw motion number and confidence
            label = f"MOTION-{i+1}: {box_confidence:.2f}"
            cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
            
            # Draw center point
            center = box['center']
            cv2.circle(frame, center, 4, color, -1)
        
        # Draw enhanced motion status with inertia info
        current_time = time.time()
        status_text = "MOTION DETECTED" if self.motion_detected else "NO MOTION"
        
        # Add inertia information
        inertia_info = ""
        if self.motion_start_time and not self.motion_detected:
            remaining = self.motion_detection_delay - (current_time - self.motion_start_time)
            if remaining > 0:
                inertia_info = f" (Confirming: {remaining:.1f}s)"
        elif self.no_motion_start_time and self.motion_detected:
            remaining = self.motion_clear_delay - (current_time - self.no_motion_start_time)
            if remaining > 0:
                inertia_info = f" (Clearing in: {remaining:.1f}s)"
        
        full_status = f"{status_text}{inertia_info}"
        # Note: "Boxes" = separate moving objects/areas detected in the frame
        confidence_text = f"Confidence: {confidence:.3f} | Moving Objects: {len(motion_boxes)}"
        fps_text = f"FPS: {self.fps_counter:.1f}"
        
        # Enhanced status background - larger for more info
        cv2.rectangle(frame, (10, 10), (500, 100), (0, 0, 0), -1)
        cv2.rectangle(frame, (10, 10), (500, 100), (255, 255, 255), 2)
        
        # Status text with better colors and larger font
        status_color = (0, 255, 0) if self.motion_detected else (128, 128, 128)
        cv2.putText(frame, full_status, (20, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.7, status_color, 2)
        cv2.putText(frame, confidence_text, (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        cv2.putText(frame, fps_text, (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        return frame
    
    def _trigger_motion_notification(self, motion_data: Dict):
        """
        Trigger motion detection notification
        
        Args:
            motion_data: Motion detection data
        """
        print(f"[Motion Detection] Triggering notification - Confidence: {motion_data['confidence']:.3f}, "
              f"Motion boxes: {len(motion_data['boxes'])}")
        
        if self.notification_callback:
            try:
                camera_id = "USB Camera"  # This would be passed from camera manager
                self.notification_callback(camera_id, motion_data)
            except Exception as e:
                print(f"[Motion Detection] Notification error: {e}")
    
    def _update_fps_counter(self):
        """Update FPS counter for performance monitoring"""
        self.frame_count += 1
        current_time = time.time()
        
        if current_time - self.last_fps_time >= 1.0:
            self.fps_counter = self.frame_count / (current_time - self.last_fps_time)
            self.frame_count = 0
            self.last_fps_time = current_time
    
    def _get_empty_motion_data(self) -> Dict:
        """Get empty motion data structure"""
        return {
            'boxes': [],
            'confidence': 0.0,
            'motion_detected': False,
            'timestamp': datetime.now(),
            'frame_count': 0,
            'fps': 0.0
        }
    
    def get_motion_status(self) -> Dict:
        """
        Get current motion detection status
        
        Returns:
            Dictionary with current motion state
        """
        return {
            'motion_detected': self.motion_detected,
            'confidence': self.current_confidence,
            'motion_boxes': len(self.current_motion_boxes),
            'last_motion_time': self.last_motion_time,
            'is_active': self.is_active,
            'fps': self.fps_counter
        }
    
    def update_sensitivity(self, sensitivity: float):
        """
        Update motion detection sensitivity
        
        Args:
            sensitivity: New sensitivity value (0.1 to 0.9)
        """
        self.background_subtractor.setVarThreshold(sensitivity * 100)
        print(f"[Motion Detection] Updated sensitivity to {sensitivity}")
    
    def cleanup(self):
        """Clean up motion detection resources"""
        self.stop_detection()
        self.background_subtractor = None
        print("[Motion Detection] Cleanup completed")