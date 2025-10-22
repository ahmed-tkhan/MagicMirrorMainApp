"""
Magic Mirror Main Application
Central UI control application for Magic Mirror system
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sys
import config
from notification_manager import NotificationManager
from video_control import VideoControlManager
from camera_stream import CameraStreamManager


class MagicMirrorApp:
    """Main application class for Magic Mirror Control Center"""
    
    def __init__(self, root: tk.Tk):
        """
        Initialize the Magic Mirror application
        
        Args:
            root: Root tkinter window
        """
        self.root = root
        self.root.title(config.APP_TITLE)
        self.root.geometry(f"{config.APP_WIDTH}x{config.APP_HEIGHT}")
        self.root.configure(bg="#1a1a1a")
        
        # Set minimum window size
        self.root.minsize(1000, 600)
        
        # Initialize managers
        self.notification_manager = None
        self.video_control_manager = None
        self.camera_stream_manager = None
        
        # TODO: Initialize Motion Detection Manager
        # - Create MotionDetectionManager class to handle advanced motion tracking
        # - Implement modular motion detection with configurable sensitivity
        # - Add camera jiggle compensation using stabilization algorithms
        # - Create motion box tracking with object detection boundaries
        # - Support multiple simultaneous camera motion detection
        self.motion_detection_manager = None
        
        # TODO: Initialize Video Processing Pipeline
        # - Create VideoProcessingPipeline for advanced video analysis
        # - Implement dual-rate processing (high FPS for motion, low FPS for GUI)
        # - Add background subtraction for motion detection
        # - Implement optical flow for motion tracking
        # - Add noise reduction and camera shake compensation
        self.video_processing_pipeline = None
        
        # Create UI
        self._create_ui()
        
        # Setup cleanup on close
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)
        
        # Start periodic tasks
        self._start_periodic_tasks()
    
    def _create_ui(self):
        """Create the main user interface"""
        # Create menu bar
        self._create_menu_bar()
        
        # Create header
        self._create_header()
        
        # Create main content area with three panels
        self._create_main_panels()
        
        # Create status bar
        self._create_status_bar()
    
    def _create_menu_bar(self):
        """Create application menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Settings", command=self._show_settings)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self._on_closing)
        
        # Tools menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="Test Motion Detection", command=self._test_motion_detection)
        tools_menu.add_command(label="Clear Notifications", command=self._clear_notifications)
        tools_menu.add_separator()
        tools_menu.add_command(label="Test USB Cameras", command=self._test_usb_cameras)
        tools_menu.add_command(label="Switch Camera", command=self._show_camera_switch_dialog)
        
        # TODO: Add Motion Detection Tools Menu Items
        # - "Motion Detection Settings" for sensitivity and threshold adjustment
        # - "Calibrate Camera Stabilization" for wind/vibration compensation setup
        # - "Motion Detection Debug View" to show bounding boxes and detection data
        # - "Export Motion Events" to save motion detection logs and statistics
        
        # TODO: Add Children's Content Menu Items
        # - "Manage Kids Videos" to add/remove/organize children's content
        # - "Create Video Playlist" for scheduled content on mirror display
        # - "Mirror Display Controls" for remote control of HDMI output
        # - "Parental Controls" for content filtering and time restrictions
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="Documentation", command=self._show_documentation)
        help_menu.add_command(label="About", command=self._show_about)
    
    def _create_header(self):
        """Create application header"""
        header_frame = tk.Frame(self.root, bg="#2c3e50", height=80)
        header_frame.pack(fill=tk.X, side=tk.TOP)
        header_frame.pack_propagate(False)
        
        # Title
        title_label = tk.Label(
            header_frame,
            text="✨ Magic Mirror Control Center",
            font=("Arial", 20, "bold"),
            bg="#2c3e50",
            fg="white"
        )
        title_label.pack(side=tk.LEFT, padx=20, pady=20)
        
        # Subtitle
        subtitle_label = tk.Label(
            header_frame,
            text="Central Control for USB Camera and HDMI Display System",
            font=("Arial", 11),
            bg="#2c3e50",
            fg="#bdc3c7"
        )
        subtitle_label.pack(side=tk.LEFT, padx=(0, 20), pady=20)
    
    def _create_main_panels(self):
        """Create main content panels"""
        # Main container
        main_container = tk.Frame(self.root, bg="#1a1a1a")
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create three-column layout
        # Left panel - Notifications (30%)
        left_panel = tk.Frame(main_container, bg="#34495e", width=400)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 5))
        
        # Middle panel - Video Controls (25%)
        middle_panel = tk.Frame(main_container, bg="#34495e", width=300)
        middle_panel.pack(side=tk.LEFT, fill=tk.BOTH, padx=5)
        
        # Right panel - Camera Stream (45%)
        right_panel = tk.Frame(main_container, bg="#34495e")
        right_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        # Initialize managers with their respective panels
        self.notification_manager = NotificationManager(left_panel)
        self.video_control_manager = VideoControlManager(
            middle_panel,
            on_video_change=self._on_video_changed
        )
        self.camera_stream_manager = CameraStreamManager(right_panel)
        
        # TODO: Initialize Advanced Managers
        # self.motion_detection_manager = MotionDetectionManager(
        #     cameras=self.camera_stream_manager,
        #     notification_callback=self._on_motion_detected,
        #     motion_threshold=config.MOTION_SENSITIVITY
        # )
        # self.video_processing_pipeline = VideoProcessingPipeline(
        #     stabilization_enabled=True,
        #     noise_reduction=True,
        #     dual_rate_processing=True
        # )
    
    def _create_status_bar(self):
        """Create status bar at bottom of window"""
        status_frame = tk.Frame(self.root, bg="#2c3e50", height=30)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        status_frame.pack_propagate(False)
        
        # Status text
        self.status_label = tk.Label(
            status_frame,
            text="Ready",
            font=("Arial", 9),
            bg="#2c3e50",
            fg="white",
            anchor="w"
        )
        self.status_label.pack(side=tk.LEFT, padx=10)
        
        # Connection indicator
        self.connection_indicator = tk.Label(
            status_frame,
            text="● USB Cameras: Ready",
            font=("Arial", 9),
            bg="#2c3e50",
            fg="#27ae60",
            anchor="e"
        )
        self.connection_indicator.pack(side=tk.RIGHT, padx=10)
    
    def _on_video_changed(self, video_name: str):
        """
        Callback when video selection changes
        
        Args:
            video_name: Name of the selected video source
        """
        self.status_label.config(text=f"Camera source changed to: {video_name}")
        print(f"[Main App] Camera changed to: {video_name}")
        
        # Get camera index and switch camera stream
        if self.video_control_manager and self.camera_stream_manager:
            camera_index = self.video_control_manager.get_current_camera_index()
            self.camera_stream_manager.switch_camera(camera_index)
        
        # Add notification about video change
        self.notification_manager.add_notification(
            "Camera Source Changed",
            f"Now viewing: {video_name}",
            "INFO"
        )
    
    def _start_periodic_tasks(self):
        """Start periodic background tasks"""
        # Simulate motion detection check (placeholder)
        self._check_motion_detection()
    
    def _check_motion_detection(self):
        """
        Check for motion detection events (placeholder)
        This would normally poll the Raspberry Pi or receive webhooks
        """
        # TODO: Implement Real Motion Detection Processing
        # - Integrate with motion_detection_manager for real-time analysis
        # - Process high-FPS video stream from cameras for motion detection
        # - Apply camera stabilization to reduce false positives from wind/vibration
        # - Generate motion bounding boxes around detected movement
        # - Filter out small movements below threshold to reduce noise
        # - Send motion events to notification system with confidence scores
        
        # TODO: Add Motion Detection State Management
        # - Track motion detection state per camera (active/inactive)
        # - Implement cooldown periods to prevent spam notifications
        # - Store recent motion events for pattern analysis
        # - Update GUI motion indicator boolean (green/gray) in real-time
        
        # Schedule next check
        self.root.after(config.MOTION_CHECK_INTERVAL, self._check_motion_detection)
    
    def _test_motion_detection(self):
        """Test motion detection notification"""
        import random
        camera_names = ["Front Door", "Back Yard", "Garage", "Living Room"]
        selected_camera = random.choice(camera_names)
        
        self.notification_manager.simulate_motion_detection(selected_camera)
        self.status_label.config(text=f"Simulated motion detection from {selected_camera}")
    
    def _clear_notifications(self):
        """Clear all notifications"""
        if self.notification_manager:
            self.notification_manager.clear_all_notifications()
            self.status_label.config(text="All notifications cleared")
    
    def _test_usb_cameras(self):
        """Test available USB cameras"""
        self.status_label.config(text="Testing USB cameras...")
        
        def test_cameras():
            import cv2
            available_cameras = []
            for i in range(4):  # Test first 4 camera indices
                cap = cv2.VideoCapture(i)
                if cap.isOpened():
                    available_cameras.append(i)
                    cap.release()
                
            camera_list = ", ".join(str(i) for i in available_cameras) if available_cameras else "None"
            self.status_label.config(text=f"Available USB cameras: {camera_list}")
            
            messagebox.showinfo(
                "USB Camera Test",
                f"Available USB cameras at indices: {camera_list}\n\n"
                f"Total cameras found: {len(available_cameras)}\n\n"
                "You can select cameras using the dropdown or quick buttons."
            )
        
        self.root.after(100, test_cameras)
    
    def _show_camera_switch_dialog(self):
        """Show camera switching dialog"""
        messagebox.showinfo(
            "Camera Switching",
            "To switch cameras:\n\n"
            "1. Use the dropdown menu in Video Control Panel\n"
            "2. Click the USB camera quick buttons\n"
            "3. Use Tools > Test USB Cameras to see available cameras\n\n"
            "Camera switching is automatic when you select a new source."
        )
    
    def _show_settings(self):
        """Show settings dialog"""
        messagebox.showinfo(
            "Settings",
            "Settings dialog would appear here.\n\n"
            "Edit config.py to change application settings:\n"
            "- USB camera indices and mappings\n"
            "- Camera resolution settings\n"
            "- HDMI display configuration\n"
            "- Motion detection sensitivity\n"
            "- Notification preferences"
        )
    
    def _show_documentation(self):
        """Show documentation"""
        messagebox.showinfo(
            "Documentation",
            "Magic Mirror Control Center\n\n"
            "Features:\n"
            "• Motion detection notifications\n"
            "• USB camera selection and control\n"
            "• Live camera stream display via USB\n"
            "• HDMI display output support\n\n"
            "For more information, see README.md"
        )
    
    def _show_about(self):
        """Show about dialog"""
        messagebox.showinfo(
            "About",
            f"{config.APP_TITLE}\n\n"
            "Version 1.0.0\n\n"
            "A Python GUI application for controlling\n"
            "Magic Mirror system with motion detection,\n"
            "USB camera selection, and HDMI display output.\n\n"
            "© 2025 Magic Mirror Project"
        )
    
    # TODO: Add Motion Detection Event Handler
    def _on_motion_detected(self, camera_id: str, motion_data: dict):
        """
        Handle motion detection events from cameras
        
        Args:
            camera_id: ID of camera that detected motion
            motion_data: Dictionary containing motion detection data including:
                        - bounding_boxes: List of motion areas
                        - confidence_score: Motion detection confidence
                        - timestamp: When motion was detected
                        - stabilized_frame: Camera-shake compensated frame
        """
        # TODO: Process motion detection data
        # - Update motion indicator boolean in camera stream
        # - Send notification with motion details
        # - Log motion event for analysis
        # - Update GUI with motion visualization
        pass
    
    def _on_closing(self):
        """Handle application closing"""
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            # Cleanup resources
            if self.camera_stream_manager:
                self.camera_stream_manager.cleanup()
            
            # TODO: Cleanup Advanced Managers
            # if self.motion_detection_manager:
            #     self.motion_detection_manager.cleanup()
            # if self.video_processing_pipeline:
            #     self.video_processing_pipeline.cleanup()
            
            self.root.destroy()
            sys.exit(0)
    
    def run(self):
        """Run the application"""
        self.root.mainloop()


def main():
    """Main entry point"""
    try:
        # Create root window
        root = tk.Tk()
        
        # Create and run application
        app = MagicMirrorApp(root)
        app.run()
        
    except Exception as e:
        print(f"Error starting application: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
