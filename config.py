"""
Magic Mirror Main Application Configuration
"""

# Application Settings
APP_TITLE = "Magic Mirror Control Center"
APP_WIDTH = 1200
APP_HEIGHT = 800

# USB Camera Settings
DEFAULT_CAMERA_INDEX = 0  # Default USB webcam (change if you have multiple cameras)
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480

# Additional Camera Indices (for multiple USB cameras)
CAMERA_INDICES = {
    "Camera 1 - Front Door": 0,
    "Camera 2 - Teams Cam": 1
}

# Motion Detection Settings
MOTION_CHECK_INTERVAL = 5000  # milliseconds
MOTION_NOTIFICATION_DURATION = 10000  # milliseconds
MOTION_SENSITIVITY = 0.3  # Motion detection sensitivity (0.1 = very sensitive, 0.9 = less sensitive)

# TODO: Add Advanced Motion Detection Configuration
# - Multiple sensitivity levels for different cameras
# - Camera-specific motion detection zones (exclude certain areas)
# - Motion detection schedule (active hours per camera)
# - Background learning rate for motion detection algorithms
# - Noise reduction and stabilization parameters
MOTION_CONFIDENCE_THRESHOLD = 0.7  # Minimum confidence for motion notifications
MOTION_MIN_AREA = 500  # Minimum pixel area for motion detection
MOTION_MAX_OBJECTS = 10  # Maximum number of motion objects to track
MOTION_STABILIZATION_ENABLED = True  # Enable camera shake compensation
MOTION_BACKGROUND_LEARNING_RATE = 0.01  # Background model learning rate

# TODO: Add Camera-Specific Motion Settings
MOTION_ZONES = {
    0: {"enabled": True, "zones": [(0, 0, 640, 480)]},  # Camera 0 full frame
    1: {"enabled": True, "zones": [(100, 100, 540, 380)]}  # Camera 1 excluding edges
}

MOTION_SCHEDULES = {
    0: {"active_hours": "06:00-22:00", "sensitivity_day": 0.3, "sensitivity_night": 0.2},
    1: {"active_hours": "24/7", "sensitivity_day": 0.4, "sensitivity_night": 0.3}
}

# Video Selection Options
VIDEO_OPTIONS = [
    "Camera 1 - Front Door",
    "Camera 2 - Teams Cam",
    "Camera 3 - Garage",
    "Camera 4 - Living Room"
]

# HDMI Display Settings
HDMI_DISPLAY_MODE = "extended"  # "extended" or "mirrored"
HDMI_RESOLUTION = "1920x1080"  # HDMI output resolution

# TODO: Add Children's Content and Mirror Display Configuration
# - Kids video library paths and organization
# - Age-appropriate content filtering settings
# - Scheduled content playback for different times of day
# - Mirror display control and picture-in-picture settings
KIDS_CONTENT_PATH = "videos/kids"  # Path to children's video library
KIDS_CONTENT_AGE_GROUPS = ["3-5", "6-8", "9-12"]  # Age group classifications
KIDS_CONTENT_CATEGORIES = ["educational", "cartoons", "stories", "music", "games"]

# Content scheduling
KIDS_CONTENT_SCHEDULE = {
    "morning": {"time": "07:00-09:00", "content": "morning_routine"},
    "learning": {"time": "09:00-12:00", "content": "educational"},
    "quiet_time": {"time": "13:00-15:00", "content": "stories"},
    "play_time": {"time": "15:00-17:00", "content": "cartoons"},
    "bedtime": {"time": "19:00-21:00", "content": "bedtime_stories"}
}

# Mirror display settings
MIRROR_DISPLAY_DEFAULT_MODE = "camera"  # "camera", "kids_content", "pip"
PIP_CAMERA_SIZE = (320, 240)  # Picture-in-picture camera feed size
PIP_CAMERA_POSITION = "top_right"  # "top_left", "top_right", "bottom_left", "bottom_right"
MIRROR_AUDIO_SOURCE = "kids_content"  # "camera", "kids_content", "mixed"

# TODO: Add Advanced Video Processing Configuration
# - Dual-rate streaming settings (GUI vs motion detection)
# - Video codec and quality settings for different use cases
# - Buffer sizes and memory management
# - Hardware acceleration settings
GUI_DISPLAY_FPS = 15  # Lower FPS for GUI efficiency
MOTION_DETECTION_FPS = 30  # Higher FPS for accurate motion detection
VIDEO_BUFFER_SIZE = 30  # Number of frames to buffer
HARDWARE_ACCELERATION = True  # Use GPU acceleration when available
VIDEO_COMPRESSION_QUALITY = 85  # JPEG compression quality for streaming

# Notification Settings
MAX_NOTIFICATIONS = 10
NOTIFICATION_FADE_TIME = 500  # milliseconds

# TODO: Add Enhanced Notification Configuration
# - Motion notification cooldown periods per camera
# - Notification sound settings and audio files
# - External notification service integration (email, SMS, push)
# - Notification grouping and summarization settings
NOTIFICATION_COOLDOWN_PERIODS = {
    "motion": 30,  # seconds between similar motion notifications
    "camera_error": 300,  # seconds between camera error notifications
    "system": 60  # seconds between system notifications
}

NOTIFICATION_SOUNDS = {
    "motion": "sounds/motion_detected.wav",
    "alert": "sounds/alert.wav", 
    "info": "sounds/info_chime.wav",
    "error": "sounds/error.wav"
}

NOTIFICATION_EXTERNAL_SERVICES = {
    "email_enabled": False,
    "email_recipients": [],
    "sms_enabled": False,
    "sms_numbers": [],
    "push_notifications": False
}

# Motion notification specific settings
MOTION_NOTIFICATION_INCLUDE_THUMBNAIL = True
MOTION_NOTIFICATION_MAX_PER_HOUR = 20  # Prevent notification spam
MOTION_NOTIFICATION_GROUP_SIMILAR = True  # Group similar notifications

# Logging
LOG_FILE = "magic_mirror.log"
LOG_LEVEL = "INFO"

# TODO: Add Comprehensive System Configuration
# - Performance monitoring and optimization settings
# - System health checks and automatic recovery
# - Data storage and retention policies
# - Security and access control settings

# Performance settings
PERFORMANCE_MONITORING = True
SYSTEM_HEALTH_CHECK_INTERVAL = 300  # seconds
AUTO_RECOVERY_ENABLED = True
MEMORY_USAGE_LIMIT = 80  # percentage
CPU_USAGE_LIMIT = 70  # percentage

# Data retention
MOTION_EVENT_RETENTION_DAYS = 30
NOTIFICATION_HISTORY_RETENTION_DAYS = 7
VIDEO_RECORDING_RETENTION_DAYS = 14  # If recording feature is implemented
LOG_RETENTION_DAYS = 30

# Security settings
ACCESS_CONTROL_ENABLED = False  # Enable user authentication
ALLOWED_CAMERA_INDICES = [0, 1, 2, 3]  # Restrict camera access
NETWORK_INTERFACE_MONITORING = True  # Monitor network interfaces
CAMERA_PRIVACY_MODE = False  # Disable cameras when not needed

# TODO: Add Feature Flags for Development
# - Enable/disable specific features during development
# - A/B testing configuration for UI improvements
# - Debug modes for different subsystems
FEATURE_FLAGS = {
    "motion_detection": True,
    "kids_content": True,
    "mirror_display": True,
    "picture_in_picture": True,
    "advanced_notifications": True,
    "motion_analytics": False,  # Future feature
    "facial_recognition": False,  # Future feature
    "voice_control": False,  # Future feature
    "cloud_integration": False  # Future feature
}

DEBUG_MODES = {
    "motion_detection_debug": False,  # Show motion detection overlay
    "performance_debug": False,  # Show performance metrics
    "notification_debug": False,  # Log all notification events
    "camera_debug": False  # Show camera diagnostic info
}
