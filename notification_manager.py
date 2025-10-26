"""
Notification Manager for Magic Mirror Application
Handles motion detection notifications and alert display
"""

import tkinter as tk
from tkinter import ttk
from datetime import datetime
from typing import List, Dict
import config
import threading
import os
import time
try:
    import winsound  # For Windows notification sounds
except ImportError:
    winsound = None


class NotificationManager:
    """Manages notifications for motion detection and other alerts"""
    
    def __init__(self, parent_frame: tk.Frame):
        """
        Initialize the notification manager
        
        Args:
            parent_frame: Parent tkinter frame for notification display
        """
        self.parent_frame = parent_frame
        self.notifications: List[Dict] = []
        self.notification_widgets: List[tk.Frame] = []
        
        # TODO: Add Advanced Motion Notification Features
        # - Motion detection confidence scoring
        # - Motion pattern analysis and classification
        # - Smart notification filtering to reduce spam
        # - Motion event clustering and summarization
        self.motion_confidence_threshold = 0.7
        self.notification_cooldown = {}  # Per-camera cooldown tracking
        self.motion_patterns = {}  # Store motion patterns for analysis
        
        # TODO: Add Notification Enhancement Features
        # - Rich notifications with motion thumbnails
        # - Motion event timeline and history
        # - Notification sound alerts with different tones
        # - Integration with external notification services
        self.notification_sounds = True
        self.motion_thumbnails = []
        self.notification_history = []
        
        # Create notification display area
        self._create_ui()
    
    def _create_ui(self):
        """Create the notification UI components"""
        # Title
        title_label = tk.Label(
            self.parent_frame,
            text="📢 Motion Detection Notifications",
            font=("Arial", 14, "bold"),
            bg="#2c3e50",
            fg="white"
        )
        title_label.pack(fill=tk.X, padx=5, pady=5)
        
        # Scrollable notification list
        self.notification_canvas = tk.Canvas(
            self.parent_frame,
            bg="#34495e",
            highlightthickness=0
        )
        self.notification_scrollbar = ttk.Scrollbar(
            self.parent_frame,
            orient="vertical",
            command=self.notification_canvas.yview
        )
        self.notification_frame = tk.Frame(
            self.notification_canvas,
            bg="#34495e"
        )
        
        self.notification_frame.bind(
            "<Configure>",
            lambda e: self.notification_canvas.configure(
                scrollregion=self.notification_canvas.bbox("all")
            )
        )
        
        self.notification_canvas.create_window(
            (0, 0),
            window=self.notification_frame,
            anchor="nw"
        )
        self.notification_canvas.configure(yscrollcommand=self.notification_scrollbar.set)
        
        self.notification_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.notification_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Add placeholder notification
        self.add_notification(
            "System Ready",
            "USB camera system initialized and ready",
            "INFO"
        )
    
    def add_notification(self, title: str, message: str, notification_type: str = "INFO"):
        """
        Add a new notification to the display
        
        Args:
            title: Notification title
            message: Notification message
            notification_type: Type of notification (INFO, WARNING, ALERT, ERROR)
        """
        timestamp = datetime.now().strftime("%H:%M:%S")  # Just time, not date
        
        notification_data = {
            "title": title,
            "message": message,
            "type": notification_type,
            "timestamp": timestamp
        }
        
        # TODO: Add smart notification filtering
        # - Check if similar notification was recently sent
        # - Apply confidence threshold for motion notifications
        # - Group related notifications to prevent spam
        # - Prioritize notifications based on type and urgency
        
        # Add to list
        self.notifications.append(notification_data)
        
        # TODO: Store in notification history for pattern analysis
        self.notification_history.append(notification_data)
        
        # Limit number of notifications
        if len(self.notifications) > config.MAX_NOTIFICATIONS:
            self.notifications.pop(0)
            if self.notification_widgets:
                self.notification_widgets.pop(0).destroy()
        
        # Create notification widget
        self._create_notification_widget(notification_data)
        
        # Play notification sound
        self._play_notification_sound(notification_type)
    
    def _create_notification_widget(self, notification_data: Dict):
        """Create a visual widget for a notification"""
        # Color scheme based on type
        color_scheme = {
            "INFO": {"bg": "#3498db", "fg": "white"},
            "WARNING": {"bg": "#f39c12", "fg": "white"},
            "ALERT": {"bg": "#e74c3c", "fg": "white"},
            "ERROR": {"bg": "#c0392b", "fg": "white"}
        }
        
        colors = color_scheme.get(notification_data["type"], color_scheme["INFO"])
        
        # Create notification frame
        notif_frame = tk.Frame(
            self.notification_frame,
            bg=colors["bg"],
            relief=tk.RAISED,
            borderwidth=2
        )
        notif_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Notification header with title and type
        header_frame = tk.Frame(notif_frame, bg=colors["bg"])
        header_frame.pack(fill=tk.X, padx=10, pady=(10, 5))
        
        title_label = tk.Label(
            header_frame,
            text=f"{notification_data['title']} [{notification_data['type']}]",
            font=("Arial", 11, "bold"),
            bg=colors["bg"],
            fg=colors["fg"],
            anchor="w"
        )
        title_label.pack(side=tk.LEFT)
        
        # Timestamp
        time_label = tk.Label(
            header_frame,
            text=notification_data["timestamp"],
            font=("Arial", 9),
            bg=colors["bg"],
            fg=colors["fg"],
            anchor="e"
        )
        time_label.pack(side=tk.RIGHT)
        
        # Message
        message_label = tk.Label(
            notif_frame,
            text=notification_data["message"],
            font=("Arial", 10),
            bg=colors["bg"],
            fg=colors["fg"],
            wraplength=350,
            justify=tk.LEFT,
            anchor="w"
        )
        message_label.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        # TODO: Add motion detection specific enhancements
        # - Motion thumbnail preview (small image of detected motion)
        # - Confidence score display with progress bar
        # - Motion area count and size information
        # - Quick action buttons (view full recording, dismiss similar)
        if notification_data.get("type") == "MOTION":
            # Placeholder for motion-specific UI enhancements
            motion_info_frame = tk.Frame(notif_frame, bg=colors["bg"])
            motion_info_frame.pack(fill=tk.X, padx=10, pady=(0, 5))
            
            # TODO: Add confidence indicator
            confidence_label = tk.Label(
                motion_info_frame,
                text=f"Confidence: {notification_data.get('confidence', 'N/A')}%",
                font=("Arial", 8),
                bg=colors["bg"],
                fg=colors["fg"]
            )
            confidence_label.pack(side=tk.LEFT)
            
            # TODO: Add motion area count
            areas_label = tk.Label(
                motion_info_frame,
                text=f"Motion Areas: {notification_data.get('motion_areas', 'N/A')}",
                font=("Arial", 8),
                bg=colors["bg"],
                fg=colors["fg"]
            )
            areas_label.pack(side=tk.RIGHT)
        
        # Dismiss button
        dismiss_btn = tk.Button(
            notif_frame,
            text="✕ Dismiss",
            command=lambda: self._dismiss_notification(notif_frame, notification_data),
            bg="#2c3e50",
            fg="white",
            font=("Arial", 8),
            relief=tk.FLAT,
            cursor="hand2"
        )
        dismiss_btn.pack(anchor="e", padx=10, pady=(0, 10))
        
        self.notification_widgets.append(notif_frame)
    
    def _dismiss_notification(self, widget: tk.Frame, notification_data: Dict):
        """Dismiss a notification"""
        if notification_data in self.notifications:
            self.notifications.remove(notification_data)
        if widget in self.notification_widgets:
            self.notification_widgets.remove(widget)
        widget.destroy()
    
    def clear_all_notifications(self):
        """Clear all notifications"""
        self.notifications.clear()
        for widget in self.notification_widgets:
            widget.destroy()
        self.notification_widgets.clear()
    
    def simulate_motion_detection(self, camera_name: str):
        """
        Simulate a motion detection event (placeholder for real implementation)
        
        Args:
            camera_name: Name of the camera that detected motion
        """
        # TODO: Replace with real motion detection integration
        # - Receive motion data from motion detection manager
        # - Include confidence score, bounding boxes, and frame thumbnail
        # - Apply smart filtering to prevent notification spam
        # - Store motion patterns for behavior analysis
        
        import random
        confidence = random.randint(70, 95)
        motion_areas = random.randint(1, 3)
        
        self.add_motion_notification(
            camera_name,
            confidence=confidence,
            motion_areas=motion_areas,
            thumbnail_path=None  # TODO: Include actual motion thumbnail
        )
    
    def add_motion_notification(self, camera_name: str, confidence: float = None, 
                              motion_areas: int = None, thumbnail_path: str = None):
        """
        Add a motion detection notification with enhanced details
        
        Args:
            camera_name: Name of camera that detected motion
            confidence: Motion detection confidence score (0-100)
            motion_areas: Number of motion areas detected
            thumbnail_path: Path to motion thumbnail image
        """
        # TODO: Implement smart notification logic
        # - Check cooldown period for this camera
        # - Compare with recent similar notifications
        # - Apply confidence threshold filtering
        # - Generate appropriate notification urgency level
        
        # Create user-friendly message about motion areas
        if motion_areas == 1:
            areas_description = "1 moving object detected"
        elif motion_areas > 1:
            areas_description = f"{motion_areas} separate moving objects detected"
        else:
            areas_description = "Motion detected"
        
        confidence_text = f"Detection confidence: {confidence:.0f}%" if confidence else ""
        
        notification_data = {
            "title": f"Motion Detected - {camera_name}",
            "message": f"{areas_description}. {confidence_text} Check camera feed for details.",
            "type": "MOTION",  # Custom type for motion notifications
            "confidence": confidence,
            "motion_areas": motion_areas,
            "thumbnail_path": thumbnail_path,
            "camera_name": camera_name
        }
        
        # Add the notification
        self.add_notification(
            notification_data["title"],
            notification_data["message"],
            "ALERT"
        )
        
        # TODO: Trigger notification sound
        # TODO: Send to external notification services
        # TODO: Update motion detection analytics
    
    def _play_notification_sound(self, notification_type: str):
        """
        Play enhanced notification sound based on type
        
        Args:
            notification_type: Type of notification (INFO, WARNING, ALERT, ERROR, MOTION)
        """
        def play_sound():
            try:
                if winsound:
                    if notification_type in ["ALERT", "MOTION"]:
                        # Enhanced motion detection alert sequence
                        # Play a distinctive 3-beep sequence for motion alerts
                        for i in range(3):
                            winsound.Beep(1000, 200)  # 1000Hz for 200ms
                            if i < 2:  # Don't pause after the last beep
                                time.sleep(0.1)  # 100ms pause between beeps
                        
                        # Follow with system exclamation for emphasis
                        time.sleep(0.3)  # 300ms pause
                        winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS | winsound.SND_ASYNC)
                        
                    elif notification_type == "ERROR":
                        # Urgent low-pitched error sequence
                        winsound.Beep(400, 500)  # Low pitch, longer duration
                        time.sleep(0.2)
                        winsound.Beep(400, 500)
                        time.sleep(0.1)
                        winsound.PlaySound("SystemHand", winsound.SND_ALIAS | winsound.SND_ASYNC)
                        
                    elif notification_type == "WARNING":
                        # Medium pitch warning sequence
                        winsound.Beep(750, 300)
                        time.sleep(0.15)
                        winsound.Beep(750, 300)
                        time.sleep(0.1)
                        winsound.PlaySound("SystemAsterisk", winsound.SND_ALIAS | winsound.SND_ASYNC)
                        
                    else:
                        # Gentle info notification
                        winsound.Beep(600, 150)  # Single gentle beep
                        time.sleep(0.1)
                        winsound.PlaySound("SystemDefault", winsound.SND_ALIAS | winsound.SND_ASYNC)
                        
                else:
                    # Enhanced fallback for non-Windows systems
                    if notification_type in ["ALERT", "MOTION"]:
                        # Triple beep for motion/alerts
                        for i in range(3):
                            print(f"\a", end="", flush=True)
                            time.sleep(0.2)
                    elif notification_type == "ERROR":
                        # Double long beep for errors
                        for i in range(2):
                            print(f"\a", end="", flush=True)
                            time.sleep(0.5)
                    else:
                        # Single beep for others
                        print(f"\a")
                        
            except Exception as e:
                print(f"[Notification] Enhanced sound error: {e}")
                # Fallback to simple beep
                try:
                    if winsound:
                        winsound.Beep(800, 300)
                    else:
                        print(f"\a")
                except:
                    pass
        
        # Play sound in separate thread to avoid blocking UI
        threading.Thread(target=play_sound, daemon=True).start()
    
    def analyze_motion_patterns(self):
        """Analyze motion patterns for behavioral insights"""
        # TODO: Implement motion pattern analysis
        # - Identify recurring motion times and locations
        # - Detect unusual motion patterns that may indicate issues
        # - Generate motion activity reports for different time periods
        # - Provide insights for optimizing camera placement and sensitivity
        pass
    
    def export_motion_events(self, start_date: str, end_date: str):
        """Export motion events for external analysis"""
        # TODO: Implement motion event export
        # - Filter motion events by date range
        # - Include motion thumbnails and metadata
        # - Export in multiple formats (CSV, JSON, PDF report)
        # - Include motion detection statistics and summaries
        pass
