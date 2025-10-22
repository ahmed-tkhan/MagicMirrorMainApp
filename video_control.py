"""
Video Control Manager for Magic Mirror Application
Handles local video source selection and USB camera control
"""

import tkinter as tk
from tkinter import ttk
from typing import Callable, Optional
import config


class VideoControlManager:
    """Manages video selection and control for USB cameras"""
    
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
        self.current_camera_index = config.DEFAULT_CAMERA_INDEX
        self.is_playing = False
        
        # TODO: Add Children's Content Management
        # - Video playlist for kids content on mirror display
        # - Content filtering and parental controls
        # - Scheduled content playback (morning cartoons, bedtime stories)
        # - Interactive dialog selection for different age groups
        self.kids_playlist = []
        self.current_kids_video = None
        self.mirror_display_active = False
        
        # TODO: Add Mirror Display Control
        # - HDMI output management for mirror display
        # - Separate controls for camera stream vs kids content
        # - Picture-in-picture mode for camera + content
        # - Remote control integration for mirror interaction
        self.hdmi_controller = None
        self.pip_mode = False
        
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
        
        # TODO: Add Children's Content Controls
        # - Kids video selection dropdown
        # - Playlist management buttons
        # - Content scheduling interface
        # - Mirror display mode toggle
    
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
            camera_index = config.CAMERA_INDICES.get(video_option, i)
            btn = tk.Button(
                quick_select_frame,
                text=f"USB {camera_index}",
                command=lambda v=video_option, idx=camera_index: self._select_video(v, idx),
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
        
        # TODO: Add Children's Content Section
        kids_content_frame = tk.LabelFrame(
            parent,
            text="Children's Content & Mirror Display",
            font=("Arial", 11, "bold"),
            bg="#34495e",
            fg="white",
            relief=tk.GROOVE,
            borderwidth=2
        )
        kids_content_frame.pack(fill=tk.X, padx=5, pady=10)
        
        # TODO: Kids video selection
        tk.Label(
            kids_content_frame,
            text="Kids Video Library:",
            font=("Arial", 10),
            bg="#34495e",
            fg="white"
        ).pack(anchor="w", padx=10, pady=(10, 5))
        
        # TODO: Implement kids video dropdown with age-appropriate content
        self.kids_video_var = tk.StringVar(value="Select Kids Video...")
        kids_video_options = [
            "Morning Cartoons Playlist",
            "Educational Videos (Ages 3-5)",
            "Educational Videos (Ages 6-8)", 
            "Bedtime Stories Collection",
            "Interactive Learning Games",
            "Custom Playlist 1"
        ]
        
        kids_dropdown = ttk.Combobox(
            kids_content_frame,
            textvariable=self.kids_video_var,
            values=kids_video_options,
            state="readonly",
            font=("Arial", 10),
            width=30
        )
        kids_dropdown.pack(padx=10, pady=(0, 10), fill=tk.X)
        
        # TODO: Mirror display controls
        mirror_controls_frame = tk.Frame(kids_content_frame, bg="#34495e")
        mirror_controls_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # TODO: Implement mirror display toggle and PIP mode
        self.mirror_display_btn = tk.Button(
            mirror_controls_frame,
            text="📺 Activate Mirror Display",
            command=self._toggle_mirror_display,
            bg="#9b59b6",
            fg="white",
            font=("Arial", 10, "bold"),
            relief=tk.RAISED,
            borderwidth=2,
            cursor="hand2",
            width=20
        )
        self.mirror_display_btn.pack(side=tk.LEFT, padx=5)
        
        self.pip_mode_btn = tk.Button(
            mirror_controls_frame,
            text="🖼️ Picture-in-Picture",
            command=self._toggle_pip_mode,
            bg="#e67e22",
            fg="white",
            font=("Arial", 10, "bold"),
            relief=tk.RAISED,
            borderwidth=2,
            cursor="hand2",
            width=20
        )
        self.pip_mode_btn.pack(side=tk.LEFT, padx=5)
    
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
        
        # Connection status
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
            text="Ready - Select USB camera to begin",
            font=("Arial", 10),
            bg="#34495e",
            fg="white"
        )
        self.status_label.pack(side=tk.LEFT)
        
        # USB Camera info
        info_frame = tk.Frame(status_frame, bg="#34495e")
        info_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        tk.Label(
            info_frame,
            text=f"Current USB Camera: {config.DEFAULT_CAMERA_INDEX}",
            font=("Arial", 9),
            bg="#34495e",
            fg="#bdc3c7"
        ).pack(anchor="w")
    
    def _on_video_selected(self, event):
        """Handle video selection from dropdown"""
        selected_video = self.video_var.get()
        camera_index = config.CAMERA_INDICES.get(selected_video, 0)
        self._select_video(selected_video, camera_index)
    
    def _select_video(self, video_name: str, camera_index: int = None):
        """
        Select a video source
        
        Args:
            video_name: Name of the video source to select
            camera_index: USB camera index to use
        """
        self.current_video = video_name
        self.video_var.set(video_name)
        
        if camera_index is not None:
            self.current_camera_index = camera_index
        
        # Update status
        self.status_label.config(text=f"Selected: {video_name} (USB {self.current_camera_index})")
        
        # Call callback if provided
        if self.on_video_change:
            self.on_video_change(video_name)
        
        print(f"[Video Control] Selected video source: {video_name} (USB Camera {self.current_camera_index})")
    
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
        self.status_label.config(text="Refreshing USB camera stream...")
        print("[Video Control] Refreshing USB camera stream")
        # Placeholder for actual stream refresh logic
        self.parent_frame.after(1000, lambda: self.status_label.config(
            text=f"Stream refreshed: {self.current_video or 'No camera selected'}"
        ))
    
    def get_current_camera_index(self):
        """Get the currently selected camera index"""
        return self.current_camera_index
    
    def send_camera_command(self, command: str, params: dict = None):
        """
        Send a command to control USB camera (placeholder for future expansion)
        
        Args:
            command: Command to send
            params: Command parameters
        """
        # Placeholder for future USB camera control commands
        print(f"[Video Control] USB Camera command: {command}")
        if params:
            print(f"[Video Control] Parameters: {params}")
        
        # Future implementation could include:
        # - Camera switching via USB hub control
        # - PTZ camera control via USB serial
        # - Camera settings adjustment
    
    # TODO: Add Children's Content Control Methods
    def _toggle_mirror_display(self):
        """Toggle mirror display on/off for children's content"""
        # TODO: Implement HDMI display control
        # - Switch HDMI output between camera feed and kids content
        # - Manage display resolution and refresh rate
        # - Handle display mode switching (extend/mirror/duplicate)
        # - Control audio output routing to mirror speakers
        self.mirror_display_active = not self.mirror_display_active
        if self.mirror_display_active:
            self.mirror_display_btn.config(text="📺 Deactivate Mirror Display", bg="#e74c3c")
            print("[Video Control] Mirror display activated for kids content")
        else:
            self.mirror_display_btn.config(text="📺 Activate Mirror Display", bg="#9b59b6")
            print("[Video Control] Mirror display deactivated")
    
    def _toggle_pip_mode(self):
        """Toggle picture-in-picture mode (camera + kids content)"""
        # TODO: Implement picture-in-picture functionality
        # - Combine camera stream with kids video content
        # - Allow repositioning and resizing of camera feed
        # - Manage audio mixing between sources
        # - Provide manual override controls for parents
        self.pip_mode = not self.pip_mode
        if self.pip_mode:
            self.pip_mode_btn.config(text="🖼️ Exit PIP Mode", bg="#c0392b")
            print("[Video Control] Picture-in-picture mode enabled")
        else:
            self.pip_mode_btn.config(text="🖼️ Picture-in-Picture", bg="#e67e22")
            print("[Video Control] Picture-in-picture mode disabled")
    
    def load_kids_content_library(self):
        """Load and organize children's video content"""
        # TODO: Implement kids content management
        # - Scan local video files for appropriate content
        # - Organize by age group, category, and duration
        # - Create playlists for different times of day
        # - Implement content filtering based on parental settings
        # - Support multiple video formats (MP4, AVI, MKV)
        pass
    
    def create_kids_playlist(self, age_group: str, category: str):
        """Create playlist for specific age group and category"""
        # TODO: Implement dynamic playlist creation
        # - Filter content by age appropriateness
        # - Consider time of day (morning cartoons vs bedtime stories)
        # - Allow manual playlist editing by parents
        # - Support scheduled content playback
        # - Include educational content progression
        pass
    
    def schedule_kids_content(self, schedule: dict):
        """Schedule children's content for specific times"""
        # TODO: Implement content scheduling
        # - Morning routine videos (wake up, breakfast, getting ready)
        # - Educational content during learning hours
        # - Quiet time/rest videos for afternoons
        # - Bedtime stories and lullabies for evenings
        # - Weekend special content and longer movies
        pass
