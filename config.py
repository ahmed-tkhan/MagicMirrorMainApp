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

# Notification Settings
MAX_NOTIFICATIONS = 10
NOTIFICATION_FADE_TIME = 500  # milliseconds

# Logging
LOG_FILE = "magic_mirror.log"
LOG_LEVEL = "INFO"
