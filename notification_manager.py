"""
Notification Manager for Magic Mirror Application
Handles motion detection notifications and alert display
"""

import tkinter as tk
from tkinter import ttk
from datetime import datetime
from typing import List, Dict
import config


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
            "Motion detection system initialized and ready",
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
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        notification_data = {
            "title": title,
            "message": message,
            "type": notification_type,
            "timestamp": timestamp
        }
        
        # Add to list
        self.notifications.append(notification_data)
        
        # Limit number of notifications
        if len(self.notifications) > config.MAX_NOTIFICATIONS:
            self.notifications.pop(0)
            if self.notification_widgets:
                self.notification_widgets.pop(0).destroy()
        
        # Create notification widget
        self._create_notification_widget(notification_data)
    
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
        self.add_notification(
            f"Motion Detected - {camera_name}",
            f"Motion was detected by {camera_name} at the current time. "
            f"Please check the camera feed for details.",
            "ALERT"
        )
