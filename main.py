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
        tools_menu.add_command(label="Connection Test", command=self._test_connection)
        
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
            text="Central Control for Raspberry Pi Camera System",
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
            text="● Raspberry Pi: Not Connected",
            font=("Arial", 9),
            bg="#2c3e50",
            fg="#95a5a6",
            anchor="e"
        )
        self.connection_indicator.pack(side=tk.RIGHT, padx=10)
    
    def _on_video_changed(self, video_name: str):
        """
        Callback when video selection changes
        
        Args:
            video_name: Name of the selected video source
        """
        self.status_label.config(text=f"Video source changed to: {video_name}")
        print(f"[Main App] Video changed to: {video_name}")
        
        # Add notification about video change
        self.notification_manager.add_notification(
            "Video Source Changed",
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
    
    def _test_connection(self):
        """Test connection to Raspberry Pi"""
        self.status_label.config(text="Testing connection to Raspberry Pi...")
        
        # Placeholder for actual connection test
        # In production, this would attempt to connect to the Raspberry Pi
        
        def update_status():
            # Simulate connection test result
            self.status_label.config(text="Connection test completed (placeholder)")
            messagebox.showinfo(
                "Connection Test",
                f"Connection test to {config.RASPI_HOST}:{config.RASPI_PORT}\n\n"
                "This is a placeholder implementation.\n"
                "In production, this would test the actual connection."
            )
        
        self.root.after(1000, update_status)
    
    def _show_settings(self):
        """Show settings dialog"""
        messagebox.showinfo(
            "Settings",
            "Settings dialog would appear here.\n\n"
            "Edit config.py to change application settings:\n"
            "- Raspberry Pi connection details\n"
            "- Camera stream URLs\n"
            "- Video quality settings\n"
            "- Notification preferences"
        )
    
    def _show_documentation(self):
        """Show documentation"""
        messagebox.showinfo(
            "Documentation",
            "Magic Mirror Control Center\n\n"
            "Features:\n"
            "• Motion detection notifications\n"
            "• Remote video selection and control\n"
            "• Live camera stream display\n"
            "• Audio/video relay from Raspberry Pi\n\n"
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
            "video selection, and camera streaming.\n\n"
            "© 2025 Magic Mirror Project"
        )
    
    def _on_closing(self):
        """Handle application closing"""
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            # Cleanup resources
            if self.camera_stream_manager:
                self.camera_stream_manager.cleanup()
            
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
