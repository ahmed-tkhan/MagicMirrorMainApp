"""
Video Control Manager for Magic Mirror Application
Handles remote video selection and control for Raspberry Pi
"""

import tkinter as tk
from tkinter import ttk
from typing import Callable, Optional
import config


class VideoControlManager:
    """Manages video selection and control for Raspberry Pi"""
    
    def __init__(self, parent_frame: tk.Frame, on_video_change: Optional[Callable] = None):
        """
        Initialize the video control manager
        
        Args:
            parent_frame: Parent tkinter frame for video controls
            on_video_change: Callback function when video selection changes
        """
        self.parent_frame = parent_frame
        self.on_video_change = on_video_change
        self.current_video = None
        self.is_playing = False
        
        # Create video control UI
        self._create_ui()
    
    def _create_ui(self):
        """Create the video control UI components"""
        # Title
        title_label = tk.Label(
            self.parent_frame,
            text="🎥 Video Control Panel",
            font=("Arial", 14, "bold"),
            bg="#2c3e50",
            fg="white"
        )
        title_label.pack(fill=tk.X, padx=5, pady=5)
        
        # Control container
        control_frame = tk.Frame(self.parent_frame, bg="#34495e")
        control_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Video selection section
        self._create_video_selection(control_frame)
        
        # Playback controls section
        self._create_playback_controls(control_frame)
        
        # Stream quality controls
        self._create_quality_controls(control_frame)
        
        # Connection status
        self._create_status_display(control_frame)
    
    def _create_video_selection(self, parent: tk.Frame):
        """Create video source selection controls"""
        selection_frame = tk.LabelFrame(
            parent,
            text="Video Source Selection",
            font=("Arial", 11, "bold"),
            bg="#34495e",
            fg="white",
            relief=tk.GROOVE,
            borderwidth=2
        )
        selection_frame.pack(fill=tk.X, padx=5, pady=10)
        
        # Video source dropdown
        tk.Label(
            selection_frame,
            text="Select Camera:",
            font=("Arial", 10),
            bg="#34495e",
            fg="white"
        ).pack(anchor="w", padx=10, pady=(10, 5))
        
        self.video_var = tk.StringVar()
        self.video_var.set(config.VIDEO_OPTIONS[0])
        
        self.video_dropdown = ttk.Combobox(
            selection_frame,
            textvariable=self.video_var,
            values=config.VIDEO_OPTIONS,
            state="readonly",
            font=("Arial", 10),
            width=30
        )
        self.video_dropdown.pack(padx=10, pady=(0, 10), fill=tk.X)
        self.video_dropdown.bind("<<ComboboxSelected>>", self._on_video_selected)
        
        # Quick select buttons
        quick_select_frame = tk.Frame(selection_frame, bg="#34495e")
        quick_select_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        for i, video_option in enumerate(config.VIDEO_OPTIONS[:4]):
            btn = tk.Button(
                quick_select_frame,
                text=f"Cam {i+1}",
                command=lambda v=video_option: self._select_video(v),
                bg="#3498db",
                fg="white",
                font=("Arial", 9),
                relief=tk.RAISED,
                borderwidth=2,
                cursor="hand2",
                width=8
            )
            btn.pack(side=tk.LEFT, padx=2)
    
    def _create_playback_controls(self, parent: tk.Frame):
        """Create playback control buttons"""
        playback_frame = tk.LabelFrame(
            parent,
            text="Playback Controls",
            font=("Arial", 11, "bold"),
            bg="#34495e",
            fg="white",
            relief=tk.GROOVE,
            borderwidth=2
        )
        playback_frame.pack(fill=tk.X, padx=5, pady=10)
        
        # Control buttons container
        button_frame = tk.Frame(playback_frame, bg="#34495e")
        button_frame.pack(pady=10)
        
        # Play/Pause button
        self.play_pause_btn = tk.Button(
            button_frame,
            text="▶ Play",
            command=self._toggle_playback,
            bg="#27ae60",
            fg="white",
            font=("Arial", 12, "bold"),
            relief=tk.RAISED,
            borderwidth=3,
            cursor="hand2",
            width=12,
            height=2
        )
        self.play_pause_btn.pack(side=tk.LEFT, padx=5)
        
        # Stop button
        self.stop_btn = tk.Button(
            button_frame,
            text="⏹ Stop",
            command=self._stop_playback,
            bg="#e74c3c",
            fg="white",
            font=("Arial", 12, "bold"),
            relief=tk.RAISED,
            borderwidth=3,
            cursor="hand2",
            width=12,
            height=2
        )
        self.stop_btn.pack(side=tk.LEFT, padx=5)
        
        # Refresh button
        self.refresh_btn = tk.Button(
            button_frame,
            text="🔄 Refresh",
            command=self._refresh_stream,
            bg="#3498db",
            fg="white",
            font=("Arial", 12, "bold"),
            relief=tk.RAISED,
            borderwidth=3,
            cursor="hand2",
            width=12,
            height=2
        )
        self.refresh_btn.pack(side=tk.LEFT, padx=5)
    
    def _create_quality_controls(self, parent: tk.Frame):
        """Create video quality control settings"""
        quality_frame = tk.LabelFrame(
            parent,
            text="Stream Quality",
            font=("Arial", 11, "bold"),
            bg="#34495e",
            fg="white",
            relief=tk.GROOVE,
            borderwidth=2
        )
        quality_frame.pack(fill=tk.X, padx=5, pady=10)
        
        # Quality selection
        tk.Label(
            quality_frame,
            text="Video Quality:",
            font=("Arial", 10),
            bg="#34495e",
            fg="white"
        ).pack(anchor="w", padx=10, pady=(10, 5))
        
        self.quality_var = tk.StringVar(value="High")
        quality_options = ["Low (240p)", "Medium (480p)", "High (720p)", "Ultra (1080p)"]
        
        quality_dropdown = ttk.Combobox(
            quality_frame,
            textvariable=self.quality_var,
            values=quality_options,
            state="readonly",
            font=("Arial", 10),
            width=20
        )
        quality_dropdown.pack(padx=10, pady=(0, 10))
        quality_dropdown.current(2)
        
        # Frame rate control
        tk.Label(
            quality_frame,
            text="Frame Rate (FPS):",
            font=("Arial", 10),
            bg="#34495e",
            fg="white"
        ).pack(anchor="w", padx=10, pady=(5, 5))
        
        self.fps_var = tk.IntVar(value=30)
        fps_scale = tk.Scale(
            quality_frame,
            from_=5,
            to=60,
            variable=self.fps_var,
            orient=tk.HORIZONTAL,
            bg="#34495e",
            fg="white",
            font=("Arial", 9),
            highlightthickness=0,
            length=250
        )
        fps_scale.pack(padx=10, pady=(0, 10))
    
    def _create_status_display(self, parent: tk.Frame):
        """Create connection status display"""
        status_frame = tk.LabelFrame(
            parent,
            text="Connection Status",
            font=("Arial", 11, "bold"),
            bg="#34495e",
            fg="white",
            relief=tk.GROOVE,
            borderwidth=2
        )
        status_frame.pack(fill=tk.X, padx=5, pady=10)
        
        # Status indicator
        indicator_frame = tk.Frame(status_frame, bg="#34495e")
        indicator_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.status_indicator = tk.Label(
            indicator_frame,
            text="●",
            font=("Arial", 20),
            bg="#34495e",
            fg="#95a5a6"  # Gray for disconnected
        )
        self.status_indicator.pack(side=tk.LEFT, padx=(0, 10))
        
        self.status_label = tk.Label(
            indicator_frame,
            text="Disconnected - Ready to connect",
            font=("Arial", 10),
            bg="#34495e",
            fg="white"
        )
        self.status_label.pack(side=tk.LEFT)
        
        # Raspberry Pi info
        info_frame = tk.Frame(status_frame, bg="#34495e")
        info_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        tk.Label(
            info_frame,
            text=f"Raspberry Pi: {config.RASPI_HOST}:{config.RASPI_PORT}",
            font=("Arial", 9),
            bg="#34495e",
            fg="#bdc3c7"
        ).pack(anchor="w")
    
    def _on_video_selected(self, event):
        """Handle video selection from dropdown"""
        selected_video = self.video_var.get()
        self._select_video(selected_video)
    
    def _select_video(self, video_name: str):
        """
        Select a video source
        
        Args:
            video_name: Name of the video source to select
        """
        self.current_video = video_name
        self.video_var.set(video_name)
        
        # Update status
        self.status_label.config(text=f"Selected: {video_name}")
        
        # Call callback if provided
        if self.on_video_change:
            self.on_video_change(video_name)
        
        print(f"[Video Control] Selected video source: {video_name}")
    
    def _toggle_playback(self):
        """Toggle play/pause state"""
        self.is_playing = not self.is_playing
        
        if self.is_playing:
            self.play_pause_btn.config(text="⏸ Pause", bg="#f39c12")
            self.status_indicator.config(fg="#27ae60")  # Green
            self.status_label.config(text=f"Playing: {self.current_video or 'No video selected'}")
            print("[Video Control] Playback started")
        else:
            self.play_pause_btn.config(text="▶ Play", bg="#27ae60")
            self.status_indicator.config(fg="#f39c12")  # Orange
            self.status_label.config(text="Paused")
            print("[Video Control] Playback paused")
    
    def _stop_playback(self):
        """Stop playback"""
        self.is_playing = False
        self.play_pause_btn.config(text="▶ Play", bg="#27ae60")
        self.status_indicator.config(fg="#95a5a6")  # Gray
        self.status_label.config(text="Stopped")
        print("[Video Control] Playback stopped")
    
    def _refresh_stream(self):
        """Refresh the video stream"""
        self.status_label.config(text="Refreshing stream...")
        print("[Video Control] Refreshing stream")
        # Placeholder for actual stream refresh logic
        self.parent_frame.after(1000, lambda: self.status_label.config(
            text=f"Stream refreshed: {self.current_video or 'No video selected'}"
        ))
    
    def send_command_to_raspi(self, command: str, params: dict = None):
        """
        Send a command to the Raspberry Pi (placeholder)
        
        Args:
            command: Command to send
            params: Command parameters
        """
        # Placeholder for actual network communication
        print(f"[Video Control] Sending command to Raspberry Pi: {command}")
        if params:
            print(f"[Video Control] Parameters: {params}")
        
        # In real implementation, this would use requests library to communicate
        # with the Raspberry Pi
        # Example:
        # import requests
        # url = f"http://{config.RASPI_HOST}:{config.RASPI_PORT}{config.RASPI_CONTROL_ENDPOINT}"
        # response = requests.post(url, json={"command": command, "params": params})
        # return response.json()
