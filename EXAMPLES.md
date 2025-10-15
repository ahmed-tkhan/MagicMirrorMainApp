# Usage Examples and API Reference

This document provides examples of how to use and extend the Magic Mirror application.

## Basic Usage

### Starting the Application

```bash
python3 main.py
```

### Monitoring Motion Detection

1. The notification panel (left side) automatically displays motion alerts
2. New notifications appear at the bottom
3. Each notification shows:
   - Title (e.g., "Motion Detected - Front Door")
   - Timestamp
   - Alert type (color-coded)
   - Message details
   - Dismiss button

### Controlling Video Sources

1. Select camera from dropdown menu
2. Use quick-select buttons (Cam 1-4) for fast switching
3. Click Play/Pause to control stream
4. Adjust quality and frame rate as needed
5. Click Refresh to reconnect to stream

### Viewing Camera Streams

1. Click "Start Stream" to begin viewing
2. Stream displays in real-time
3. Use "Snapshot" to capture current frame
4. Click "Stop Stream" when done

## Code Examples

### Adding Custom Notifications

```python
# In your integration code
from notification_manager import NotificationManager

# Create notification manager (normally done in main.py)
notification_mgr = NotificationManager(parent_frame)

# Add info notification
notification_mgr.add_notification(
    "System Update",
    "All cameras are online and functioning normally",
    "INFO"
)

# Add warning notification
notification_mgr.add_notification(
    "Low Battery",
    "Camera 3 battery is below 20%",
    "WARNING"
)

# Add alert notification
notification_mgr.add_notification(
    "Motion Detected",
    "Unusual activity detected at front door",
    "ALERT"
)

# Add error notification
notification_mgr.add_notification(
    "Connection Lost",
    "Unable to connect to Camera 2",
    "ERROR"
)
```

### Simulating Motion Events

```python
# Test motion detection
notification_mgr.simulate_motion_detection("Front Door")
notification_mgr.simulate_motion_detection("Back Yard")
```

### Controlling Video Playback

```python
from video_control import VideoControlManager

# Create video control manager
video_ctrl = VideoControlManager(parent_frame)

# Select a video source programmatically
video_ctrl._select_video("Camera 2 - Back Yard")

# Start playback
video_ctrl._toggle_playback()

# Stop playback
video_ctrl._stop_playback()

# Refresh stream
video_ctrl._refresh_stream()
```

### Managing Camera Streams

```python
from camera_stream import CameraStreamManager

# Create camera stream manager
camera_mgr = CameraStreamManager(parent_frame)

# Start streaming
camera_mgr.start_stream()

# Take a snapshot
camera_mgr.take_snapshot()

# Stop streaming
camera_mgr.stop_stream()
```

## Integration Examples

### Integrating with Motion Detection Service

```python
# Example: Polling-based motion detection
import requests
import time

def check_motion_detection():
    """Check for motion events from external service"""
    try:
        response = requests.get("http://your-motion-service/api/events")
        if response.status_code == 200:
            events = response.json()
            for event in events:
                notification_mgr.add_notification(
                    f"Motion Detected - {event['camera']}",
                    f"Motion detected at {event['timestamp']}",
                    "ALERT"
                )
    except Exception as e:
        print(f"Error checking motion: {e}")

# Call periodically
root.after(5000, check_motion_detection)
```

### Webhook-based Integration

```python
# Example: Flask webhook receiver
from flask import Flask, request
from threading import Thread

webhook_app = Flask(__name__)

@webhook_app.route('/webhook/motion', methods=['POST'])
def motion_webhook():
    """Receive motion detection webhooks"""
    data = request.json
    camera = data.get('camera', 'Unknown')
    timestamp = data.get('timestamp', 'Unknown')
    
    # Add notification
    notification_mgr.add_notification(
        f"Motion Detected - {camera}",
        f"Motion detected at {timestamp}",
        "ALERT"
    )
    
    return {"status": "received"}, 200

def run_webhook_server():
    """Run webhook server in background thread"""
    webhook_app.run(host='0.0.0.0', port=5000)

# Start webhook server
webhook_thread = Thread(target=run_webhook_server, daemon=True)
webhook_thread.start()
```

### Sending Commands to Raspberry Pi

```python
import requests
import config

def send_camera_command(command, camera_name):
    """Send command to Raspberry Pi"""
    try:
        url = f"http://{config.RASPI_HOST}:{config.RASPI_PORT}{config.RASPI_CONTROL_ENDPOINT}"
        payload = {
            "command": command,
            "params": {
                "camera": camera_name
            }
        }
        
        response = requests.post(url, json=payload, timeout=5)
        
        if response.status_code == 200:
            print(f"Command sent successfully: {command}")
            return response.json()
        else:
            print(f"Error sending command: {response.status_code}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"Connection error: {e}")
        return None

# Use it
result = send_camera_command("switch_camera", "Camera 1 - Front Door")
if result:
    print(f"Result: {result}")
```

### Custom Video Source Handler

```python
class CustomVideoHandler:
    """Custom video source handler"""
    
    def __init__(self, video_control_mgr):
        self.video_control = video_control_mgr
        self.video_control.on_video_change = self.handle_video_change
    
    def handle_video_change(self, video_name):
        """Handle video source change"""
        print(f"Video changed to: {video_name}")
        
        # Send command to Raspberry Pi
        send_camera_command("switch_camera", video_name)
        
        # Update stream URL
        camera_index = config.VIDEO_OPTIONS.index(video_name) + 1
        new_url = f"http://{config.RASPI_HOST}:{config.RASPI_PORT}/stream/{camera_index}"
        
        # Reconnect camera stream with new URL
        # (implementation depends on your camera_stream module)
        print(f"Switching to stream: {new_url}")

# Use it
handler = CustomVideoHandler(video_control_mgr)
```

## Extending the Application

### Adding a New Panel

```python
# 1. Create a new module (e.g., analytics_panel.py)
import tkinter as tk

class AnalyticsPanel:
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame
        self._create_ui()
    
    def _create_ui(self):
        tk.Label(
            self.parent_frame,
            text="📊 Analytics",
            font=("Arial", 14, "bold")
        ).pack()
        
        # Add your widgets here

# 2. Add to main.py
from analytics_panel import AnalyticsPanel

# 3. In _create_main_panels(), add:
analytics_panel = tk.Frame(main_container, bg="#34495e")
analytics_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
self.analytics_panel = AnalyticsPanel(analytics_panel)
```

### Custom Configuration Loader

```python
import yaml

def load_config_from_file(filename="config.yaml"):
    """Load configuration from YAML file"""
    with open(filename, 'r') as f:
        user_config = yaml.safe_load(f)
    
    # Override default config
    import config
    for key, value in user_config.items():
        if hasattr(config, key):
            setattr(config, key, value)

# Use it
load_config_from_file("my_config.yaml")
```

### Logging Integration

```python
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('magic_mirror.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger('MagicMirror')

# Use throughout the application
logger.info("Application started")
logger.warning("Connection to Raspberry Pi lost")
logger.error("Failed to process camera stream")
```

### Database Integration for Event History

```python
import sqlite3
from datetime import datetime

class EventDatabase:
    """Store motion detection events in database"""
    
    def __init__(self, db_file="events.db"):
        self.conn = sqlite3.connect(db_file)
        self._create_tables()
    
    def _create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS motion_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                camera TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                event_type TEXT,
                details TEXT
            )
        ''')
        self.conn.commit()
    
    def add_event(self, camera, event_type, details):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO motion_events (camera, event_type, details)
            VALUES (?, ?, ?)
        ''', (camera, event_type, details))
        self.conn.commit()
    
    def get_recent_events(self, limit=10):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT * FROM motion_events
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (limit,))
        return cursor.fetchall()

# Use it
db = EventDatabase()
db.add_event("Front Door", "motion", "Person detected")
recent = db.get_recent_events()
```

## Command-Line Interface

### Running with Arguments

```python
# Add to main.py
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='Magic Mirror Control Center')
    parser.add_argument('--host', help='Raspberry Pi host', default=config.RASPI_HOST)
    parser.add_argument('--port', type=int, help='Raspberry Pi port', default=config.RASPI_PORT)
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    return parser.parse_args()

# In main()
args = parse_args()
if args.host:
    config.RASPI_HOST = args.host
if args.port:
    config.RASPI_PORT = args.port
```

Usage:
```bash
python3 main.py --host 192.168.1.150 --port 8080 --debug
```

## Testing Examples

### Unit Test Example

```python
import unittest
from notification_manager import NotificationManager
import tkinter as tk

class TestNotificationManager(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.frame = tk.Frame(self.root)
        self.mgr = NotificationManager(self.frame)
    
    def tearDown(self):
        self.root.destroy()
    
    def test_add_notification(self):
        self.mgr.add_notification("Test", "Test message", "INFO")
        self.assertEqual(len(self.mgr.notifications), 2)  # 1 default + 1 new
    
    def test_clear_notifications(self):
        self.mgr.add_notification("Test", "Test message", "INFO")
        self.mgr.clear_all_notifications()
        self.assertEqual(len(self.mgr.notifications), 0)

if __name__ == '__main__':
    unittest.main()
```

## Performance Tips

1. **Stream Quality**: Lower quality for slower connections
2. **Frame Rate**: Reduce FPS if system is slow
3. **Notification Limit**: Keep MAX_NOTIFICATIONS reasonable
4. **Threading**: Camera stream already uses threads for performance
5. **Memory**: Old notifications are automatically cleared

## Best Practices

1. **Error Handling**: Always wrap network calls in try-except
2. **Timeouts**: Use timeouts for all HTTP requests
3. **Resource Cleanup**: Always call cleanup() on camera streams
4. **Configuration**: Keep sensitive data in config files, not code
5. **Logging**: Log important events for debugging
6. **Testing**: Use test_app.py to verify changes

## Troubleshooting Integration Issues

### Connection Timeouts
```python
import requests

try:
    response = requests.get(url, timeout=5)  # 5 second timeout
except requests.exceptions.Timeout:
    print("Request timed out")
except requests.exceptions.ConnectionError:
    print("Connection failed")
```

### Stream Disconnections
```python
# Implement auto-reconnect
def auto_reconnect_stream():
    max_retries = 3
    for attempt in range(max_retries):
        try:
            camera_mgr.start_stream()
            break
        except Exception as e:
            print(f"Retry {attempt + 1}/{max_retries}")
            time.sleep(2)
```

## Support and Resources

- **Documentation**: See README.md and SETUP.md
- **Examples**: This file (EXAMPLES.md)
- **Issues**: GitHub Issues page
- **Configuration**: config.py file
