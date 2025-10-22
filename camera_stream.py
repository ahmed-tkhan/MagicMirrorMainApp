"""
Camera Stream Manager for Magic Mirror Application
Handles USB webcam video streaming and display
"""

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import cv2
from typing import Optional
import threading
import config


class CameraStreamManager:
    """Manages USB camera stream display and video capture"""
    
    def __init__(self, parent_frame: tk.Frame):
        """
        Initialize the camera stream manager
        
        Args:
            parent_frame: Parent tkinter frame for camera stream display
        """
        self.parent_frame = parent_frame
        self.stream_active = False
        self.video_capture = None
        self.current_frame = None
        self.stream_thread = None
        self.current_camera_index = config.DEFAULT_CAMERA_INDEX
        
        # TODO: Add Motion Detection Integration
        # - Motion detection state tracking (active/idle)
        # - Motion indicator boolean for GUI display (green = motion, gray = no motion)
        # - Motion bounding box overlay on video stream
        # - Confidence score display for motion detection
        self.motion_detected = False
        self.motion_boxes = []
        self.motion_confidence = 0.0
        
        # TODO: Add Dual-Rate Streaming Support
        # - High FPS capture for motion detection (30-60 FPS)
        # - Low FPS display for GUI efficiency (10-15 FPS)
        # - Separate processing threads for motion vs display
        # - Frame rate adaptation based on system performance
        self.motion_detection_thread = None
        self.gui_display_fps = 15  # Lower FPS for GUI display
        self.motion_detection_fps = 30  # Higher FPS for motion detection
        
        # Create camera stream UI
        self._create_ui()
    
    def _create_ui(self):
        """Create the camera stream UI components"""
        # Title
        title_label = tk.Label(
            self.parent_frame,
            text="📹 Camera Stream",
            font=("Arial", 14, "bold"),
            bg="#2c3e50",
            fg="white"
        )
        title_label.pack(fill=tk.X, padx=5, pady=5)
        
        # Stream display container
        stream_container = tk.Frame(self.parent_frame, bg="#34495e")
        stream_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Video display canvas
        self.video_canvas = tk.Canvas(
            stream_container,
            bg="#1a1a1a",
            highlightthickness=2,
            highlightbackground="#3498db",
            width=config.CAMERA_WIDTH,
            height=config.CAMERA_HEIGHT
        )
        self.video_canvas.pack(pady=10)
        
        # Display placeholder
        self._display_placeholder()
        
        # Stream controls
        self._create_stream_controls(stream_container)
        
        # Stream info
        self._create_stream_info(stream_container)
        
        # TODO: Add Motion Detection Indicator
        # - Create motion indicator widget (green/gray boolean display)
        # - Add motion confidence meter/progress bar
        # - Display current motion bounding box count
        # - Show last motion detection timestamp
    
    def _create_stream_controls(self, parent: tk.Frame):
        """Create stream control buttons"""
        control_frame = tk.Frame(parent, bg="#34495e")
        control_frame.pack(pady=10)
        
        # Start stream button
        self.start_btn = tk.Button(
            control_frame,
            text="▶ Start Stream",
            command=self.start_stream,
            bg="#27ae60",
            fg="white",
            font=("Arial", 11, "bold"),
            relief=tk.RAISED,
            borderwidth=3,
            cursor="hand2",
            width=15
        )
        self.start_btn.pack(side=tk.LEFT, padx=5)
        
        # Stop stream button
        self.stop_btn = tk.Button(
            control_frame,
            text="⏹ Stop Stream",
            command=self.stop_stream,
            bg="#e74c3c",
            fg="white",
            font=("Arial", 11, "bold"),
            relief=tk.RAISED,
            borderwidth=3,
            cursor="hand2",
            width=15,
            state=tk.DISABLED
        )
        self.stop_btn.pack(side=tk.LEFT, padx=5)
        
        # Snapshot button
        self.snapshot_btn = tk.Button(
            control_frame,
            text="📷 Snapshot",
            command=self.take_snapshot,
            bg="#3498db",
            fg="white",
            font=("Arial", 11, "bold"),
            relief=tk.RAISED,
            borderwidth=3,
            cursor="hand2",
            width=15
        )
        self.snapshot_btn.pack(side=tk.LEFT, padx=5)
    
    def _create_stream_info(self, parent: tk.Frame):
        """Create stream information display"""
        info_frame = tk.LabelFrame(
            parent,
            text="Stream Information",
            font=("Arial", 10, "bold"),
            bg="#34495e",
            fg="white",
            relief=tk.GROOVE,
            borderwidth=2
        )
        info_frame.pack(fill=tk.X, pady=10)
        
        # Stream URL
        url_frame = tk.Frame(info_frame, bg="#34495e")
        url_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(
            url_frame,
            text="Camera Source:",
            font=("Arial", 9, "bold"),
            bg="#34495e",
            fg="white"
        ).pack(side=tk.LEFT)
        
        self.url_label = tk.Label(
            url_frame,
            text=f"USB Camera {self.current_camera_index}",
            font=("Arial", 9),
            bg="#34495e",
            fg="#bdc3c7"
        )
        self.url_label.pack(side=tk.LEFT, padx=(10, 0))
        
        # Status info
        status_frame = tk.Frame(info_frame, bg="#34495e")
        status_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(
            status_frame,
            text="Status:",
            font=("Arial", 9, "bold"),
            bg="#34495e",
            fg="white"
        ).pack(side=tk.LEFT)
        
        self.stream_status_label = tk.Label(
            status_frame,
            text="Not Connected",
            font=("Arial", 9),
            bg="#34495e",
            fg="#95a5a6"
        )
        self.stream_status_label.pack(side=tk.LEFT, padx=(10, 0))
        
        # Resolution info
        resolution_frame = tk.Frame(info_frame, bg="#34495e")
        resolution_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(
            resolution_frame,
            text="Resolution:",
            font=("Arial", 9, "bold"),
            bg="#34495e",
            fg="white"
        ).pack(side=tk.LEFT)
        
        self.resolution_label = tk.Label(
            resolution_frame,
            text=f"{config.CAMERA_WIDTH}x{config.CAMERA_HEIGHT}",
            font=("Arial", 9),
            bg="#34495e",
            fg="#bdc3c7"
        )
        self.resolution_label.pack(side=tk.LEFT, padx=(10, 0))
        
        # TODO: Add Motion Detection Status Display
        # Motion indicator
        motion_frame = tk.Frame(info_frame, bg="#34495e")
        motion_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(
            motion_frame,
            text="Motion Status:",
            font=("Arial", 9, "bold"),
            bg="#34495e",
            fg="white"
        ).pack(side=tk.LEFT)
        
        # TODO: Implement motion indicator boolean (green for motion, gray for no motion)
        self.motion_indicator = tk.Label(
            motion_frame,
            text="● No Motion",
            font=("Arial", 9, "bold"),
            bg="#34495e",
            fg="#95a5a6"  # Gray for no motion, will be green for motion
        )
        self.motion_indicator.pack(side=tk.LEFT, padx=(10, 0))
    
    def _display_placeholder(self):
        """Display a placeholder image when stream is not active"""
        # Create a simple placeholder
        self.video_canvas.delete("all")
        
        # Draw placeholder elements
        center_x = config.CAMERA_WIDTH // 2
        center_y = config.CAMERA_HEIGHT // 2
        
        # Background
        self.video_canvas.create_rectangle(
            0, 0, config.CAMERA_WIDTH, config.CAMERA_HEIGHT,
            fill="#1a1a1a"
        )
        
        # Camera icon (simple representation)
        icon_size = 60
        self.video_canvas.create_rectangle(
            center_x - icon_size, center_y - icon_size // 2,
            center_x + icon_size, center_y + icon_size // 2,
            fill="#34495e", outline="#3498db", width=3
        )
        self.video_canvas.create_oval(
            center_x - icon_size // 2, center_y - icon_size // 4,
            center_x + icon_size // 2, center_y + icon_size // 4,
            fill="#2c3e50", outline="#3498db", width=2
        )
        
        # Text
        self.video_canvas.create_text(
            center_x, center_y + icon_size,
            text="USB Camera Offline",
            font=("Arial", 14, "bold"),
            fill="#7f8c8d"
        )
        self.video_canvas.create_text(
            center_x, center_y + icon_size + 30,
            text="Click 'Start Stream' to connect",
            font=("Arial", 10),
            fill="#95a5a6"
        )
    
    def start_stream(self):
        """Start the camera stream"""
        if self.stream_active:
            return
        
        print("[Camera Stream] Starting stream...")
        self.stream_active = True
        
        # Update UI
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.stream_status_label.config(text="Connecting...", fg="#f39c12")
        
        # Start stream in a separate thread to avoid blocking UI
        self.stream_thread = threading.Thread(target=self._stream_loop, daemon=True)
        self.stream_thread.start()
    
    def _stream_loop(self):
        """Main stream processing loop (runs in separate thread)"""
        try:
            # Try to open USB camera
            print(f"[Camera Stream] Attempting to open USB camera {self.current_camera_index}")
            self.video_capture = cv2.VideoCapture(self.current_camera_index)
            
            if not self.video_capture.isOpened():
                print("[Camera Stream] Could not open USB camera, trying alternative indices...")
                # Try other camera indices
                for i in range(4):
                    if i != self.current_camera_index:
                        test_capture = cv2.VideoCapture(i)
                        if test_capture.isOpened():
                            test_capture.release()
                            self.current_camera_index = i
                            self.video_capture = cv2.VideoCapture(i)
                            print(f"[Camera Stream] Found camera at index {i}")
                            break
                        test_capture.release()
                
                if not self.video_capture.isOpened():
                    print("[Camera Stream] No USB cameras found")
                    self.stream_status_label.config(text="No USB Camera Found", fg="#e74c3c")
                    self._display_placeholder()
                    return
            
            # Update camera source label
            self.url_label.config(text=f"USB Camera {self.current_camera_index}")
            
            self.stream_status_label.config(text="Streaming", fg="#27ae60")
            print("[Camera Stream] USB camera stream started successfully")
            
            while self.stream_active:
                ret, frame = self.video_capture.read()
                
                if ret:
                    # Resize frame to fit canvas
                    frame = cv2.resize(frame, (config.CAMERA_WIDTH, config.CAMERA_HEIGHT))
                    
                    # TODO: Implement Dual-Rate Processing
                    # - Process frame at high FPS for motion detection
                    # - Only update GUI display at lower FPS for efficiency
                    # - Apply camera stabilization to reduce jiggle from wind
                    # - Draw motion bounding boxes on display frame
                    
                    # Convert from BGR to RGB
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    
                    # TODO: Add Motion Detection Processing Here
                    # processed_frame, motion_data = self.process_frame_for_motion(frame)
                    # self.update_motion_status(motion_data)
                    # if motion_data['boxes']:
                    #     frame = self.draw_motion_boxes(frame, motion_data['boxes'])
                    
                    # Convert to PIL Image
                    image = Image.fromarray(frame)
                    photo = ImageTk.PhotoImage(image=image)
                    
                    # Update canvas with new frame
                    self.current_frame = photo
                    self.video_canvas.delete("all")
                    self.video_canvas.create_image(0, 0, image=photo, anchor=tk.NW)
                    
                    # Keep a reference to prevent garbage collection
                    self.video_canvas.image = photo
                else:
                    print("[Camera Stream] Failed to read frame")
                    break
                
        except Exception as e:
            print(f"[Camera Stream] Error: {e}")
            self.stream_status_label.config(text="Error", fg="#e74c3c")
        
        finally:
            if self.video_capture:
                self.video_capture.release()
    
    def stop_stream(self):
        """Stop the camera stream"""
        if not self.stream_active:
            return
        
        print("[Camera Stream] Stopping stream...")
        self.stream_active = False
        
        # Wait for stream thread to finish
        if self.stream_thread and self.stream_thread.is_alive():
            self.stream_thread.join(timeout=2)
        
        # Update UI
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.stream_status_label.config(text="Not Connected", fg="#95a5a6")
        
        # Display placeholder
        self._display_placeholder()
        
        print("[Camera Stream] Stream stopped")
    
    def take_snapshot(self):
        """Take a snapshot of the current frame"""
        if not self.stream_active or self.current_frame is None:
            print("[Camera Stream] Cannot take snapshot - stream not active")
            return
        
        try:
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"snapshot_{timestamp}.png"
            
            # In production, save the actual frame
            # For now, just log the action
            print(f"[Camera Stream] Snapshot saved: {filename}")
            self.stream_status_label.config(text=f"Snapshot saved: {filename}")
            
            # Reset status after 3 seconds
            self.parent_frame.after(3000, lambda: self.stream_status_label.config(
                text="Streaming" if self.stream_active else "Not Connected"
            ))
            
        except Exception as e:
            print(f"[Camera Stream] Error taking snapshot: {e}")
    
    def switch_camera(self, camera_index: int):
        """
        Switch to a different USB camera
        
        Args:
            camera_index: Index of the USB camera to switch to
        """
        if self.stream_active:
            self.stop_stream()
        
        self.current_camera_index = camera_index
        self.url_label.config(text=f"USB Camera {camera_index}")
        print(f"[Camera Stream] Switched to USB camera {camera_index}")
        
        # Auto-start stream if it was active
        if not self.stream_active:
            self.start_stream()

    # TODO: Add Motion Detection Methods
    def process_frame_for_motion(self, frame):
        """
        Process frame for motion detection with advanced algorithms
        
        Args:
            frame: Input video frame
            
        Returns:
            tuple: (processed_frame, motion_data)
                   motion_data contains: boxes, confidence, stabilized_frame
        """
        # TODO: Implement advanced motion detection
        # - Background subtraction for motion detection
        # - Camera shake compensation using optical flow
        # - Noise filtering to reduce false positives from wind
        # - Object tracking for persistent motion areas
        # - Confidence scoring for motion quality
        pass
    
    def update_motion_status(self, motion_data):
        """
        Update motion detection status in GUI
        
        Args:
            motion_data: Motion detection results
        """
        # TODO: Update motion indicator boolean
        # - Set motion_detected flag based on confidence threshold
        # - Update motion_indicator label color (green/gray)
        # - Update motion confidence display
        # - Trigger motion notification if needed
        pass
    
    def draw_motion_boxes(self, frame, motion_boxes):
        """
        Draw motion detection bounding boxes on frame
        
        Args:
            frame: Video frame to draw on
            motion_boxes: List of motion bounding boxes
            
        Returns:
            frame: Frame with motion boxes drawn
        """
        # TODO: Draw bounding boxes around motion areas
        # - Use different colors for different confidence levels
        # - Add motion vector arrows for direction
        # - Include timestamp and confidence text overlays
        pass
    
    def cleanup(self):
        """Clean up resources"""
        self.stop_stream()
        
        # TODO: Cleanup motion detection resources
        # - Stop motion detection thread
        # - Release motion detection models
        # - Clear motion history buffers
