"""
Magic Mirror Main Application Configuration
"""

# Application Settings
APP_TITLE = "Magic Mirror Control Center"
APP_WIDTH = 1200
APP_HEIGHT = 800

# Raspberry Pi Connection Settings
RASPI_HOST = "192.168.1.100"  # Change to your Raspberry Pi IP
RASPI_PORT = 8080
RASPI_VIDEO_ENDPOINT = "/api/video"
RASPI_CONTROL_ENDPOINT = "/api/control"

# Camera Stream Settings
CAMERA_STREAM_URL = "http://192.168.1.100:8081/stream"  # Change to your camera stream URL
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480

# Motion Detection Settings
MOTION_CHECK_INTERVAL = 5000  # milliseconds
MOTION_NOTIFICATION_DURATION = 10000  # milliseconds

# Video Selection Options
VIDEO_OPTIONS = [
    "Camera 1 - Front Door",
    "Camera 2 - Back Yard",
    "Camera 3 - Garage",
    "Camera 4 - Living Room"
]

# Notification Settings
MAX_NOTIFICATIONS = 10
NOTIFICATION_FADE_TIME = 500  # milliseconds

# Logging
LOG_FILE = "magic_mirror.log"
LOG_LEVEL = "INFO"
