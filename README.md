# Magic Mirror Control Center

A Python GUI application for controlling a Magic Mirror system with motion detection notifications, remote video selection/control on Raspberry Pi, and audio/video relay from home cameras.

## Features

✨ **Modern GUI Interface** - Built with Tkinter for cross-platform compatibility
📢 **Motion Detection Notifications** - Real-time alerts when motion is detected
🎥 **Video Control Panel** - Remote selection and control of Raspberry Pi video sources
📹 **Camera Stream Display** - Live audio/video relay from home cameras
⚙️ **Easy Configuration** - Centralized settings in `config.py`
🔧 **Modular Architecture** - Well-organized code for easy integration and extension

## Screenshots

The application features three main panels:
- **Left Panel**: Motion detection notifications with color-coded alerts
- **Middle Panel**: Video control with camera selection and playback controls
- **Right Panel**: Live camera stream display with controls

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/ahmed-tkhan/MagicMirrorMainApp.git
cd MagicMirrorMainApp
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure the application by editing `config.py`:
```python
# Update with your Raspberry Pi IP and port
RASPI_HOST = "192.168.1.100"
RASPI_PORT = 8080

# Update with your camera stream URL
CAMERA_STREAM_URL = "http://192.168.1.100:8081/stream"
```

## Usage

### Running the Application

```bash
python main.py
```

### Main Features

#### 1. Motion Detection Notifications
- Displays real-time notifications when motion is detected
- Color-coded alerts (INFO, WARNING, ALERT, ERROR)
- Dismiss individual notifications or clear all
- Automatic scrolling for multiple notifications

#### 2. Video Control Panel
- Select from multiple camera sources
- Play/Pause/Stop controls for video playback
- Stream quality adjustment (240p to 1080p)
- Frame rate control (5-60 FPS)
- Quick camera selection buttons
- Connection status indicator

#### 3. Camera Stream Display
- Live video feed from Raspberry Pi camera
- Start/Stop stream controls
- Take snapshots of current frame
- Real-time stream information
- Connection status and resolution display

#### 4. Menu Options
- **File Menu**:
  - Settings: Configure application parameters
  - Exit: Close the application
  
- **Tools Menu**:
  - Test Motion Detection: Simulate a motion event
  - Clear Notifications: Remove all notifications
  - Connection Test: Verify Raspberry Pi connection
  
- **Help Menu**:
  - Documentation: View help information
  - About: Application information

## Project Structure

```
MagicMirrorMainApp/
├── main.py                  # Main application entry point
├── config.py                # Configuration settings
├── notification_manager.py  # Handles motion detection notifications
├── video_control.py         # Remote video selection and control
├── camera_stream.py         # Camera streaming and display
├── requirements.txt         # Python dependencies
├── README.md               # This file
└── LICENSE                 # MIT License
```

## Architecture

The application follows a modular architecture with clear separation of concerns:

### Core Modules

1. **main.py** - Main application class that orchestrates all components
2. **notification_manager.py** - Manages notification display and motion alerts
3. **video_control.py** - Handles video source selection and playback control
4. **camera_stream.py** - Manages camera stream display and capture
5. **config.py** - Centralized configuration for easy customization

### Key Design Principles

- **Modular**: Each component is independent and can be extended separately
- **Callback-based**: Uses callbacks for inter-component communication
- **Thread-safe**: Camera streaming runs in separate thread to avoid UI blocking
- **Configurable**: All settings centralized in config.py
- **Placeholder-ready**: Easy to integrate with actual Raspberry Pi backend

## Integration Guide

### Connecting to Raspberry Pi

The application provides placeholder methods for Raspberry Pi integration:

1. **Video Control Commands**:
```python
# In video_control.py
def send_command_to_raspi(self, command: str, params: dict = None):
    # Add your HTTP/WebSocket communication here
    import requests
    url = f"http://{config.RASPI_HOST}:{config.RASPI_PORT}{config.RASPI_CONTROL_ENDPOINT}"
    response = requests.post(url, json={"command": command, "params": params})
    return response.json()
```

2. **Motion Detection Integration**:
```python
# In notification_manager.py
# Connect to your motion detection service
# Can use webhooks, polling, or WebSocket
```

3. **Camera Stream**:
```python
# In camera_stream.py
# Update _stream_loop() to connect to your camera URL
self.video_capture = cv2.VideoCapture(config.CAMERA_STREAM_URL)
```

### Extending Functionality

#### Adding New Video Sources

Edit `config.py`:
```python
VIDEO_OPTIONS = [
    "Camera 1 - Front Door",
    "Camera 2 - Back Yard",
    "Camera 3 - Garage",
    "Camera 4 - Living Room",
    "Camera 5 - Your New Camera"  # Add here
]
```

#### Adding Custom Notifications

```python
# In your code
app.notification_manager.add_notification(
    title="Custom Alert",
    message="Your custom message here",
    notification_type="WARNING"  # INFO, WARNING, ALERT, or ERROR
)
```

#### Customizing UI Colors

The application uses a dark theme with blue accents. Colors can be modified in each component's `_create_ui()` methods.

## Configuration Options

### Application Settings
- `APP_TITLE`: Application window title
- `APP_WIDTH`, `APP_HEIGHT`: Window dimensions

### Raspberry Pi Connection
- `RASPI_HOST`: IP address of Raspberry Pi
- `RASPI_PORT`: Port number
- `RASPI_VIDEO_ENDPOINT`: Video API endpoint
- `RASPI_CONTROL_ENDPOINT`: Control API endpoint

### Camera Settings
- `CAMERA_STREAM_URL`: URL of camera stream
- `CAMERA_WIDTH`, `CAMERA_HEIGHT`: Stream resolution

### Motion Detection
- `MOTION_CHECK_INTERVAL`: How often to check for motion (ms)
- `MOTION_NOTIFICATION_DURATION`: How long to display notifications (ms)

### Notifications
- `MAX_NOTIFICATIONS`: Maximum number of notifications to display
- `NOTIFICATION_FADE_TIME`: Fade animation duration (ms)

## Troubleshooting

### Camera Not Working
- Ensure OpenCV is properly installed: `pip install opencv-python`
- Check camera permissions on your system
- Verify camera stream URL in `config.py`
- Try using default camera (index 0) for testing

### Cannot Connect to Raspberry Pi
- Verify Raspberry Pi IP address and port in `config.py`
- Ensure Raspberry Pi is on the same network
- Check firewall settings
- Test connection manually with `ping <RASPI_HOST>`

### Dependencies Issues
- Ensure Python 3.8+ is installed
- Update pip: `pip install --upgrade pip`
- Reinstall dependencies: `pip install -r requirements.txt --force-reinstall`

## Development

### Adding New Features

1. Create a new module in the project root
2. Import in `main.py`
3. Initialize in `MagicMirrorApp.__init__()`
4. Add UI panel in `_create_main_panels()`

### Testing

Run the application and use the Tools menu:
- "Test Motion Detection" - Simulates a motion event
- "Connection Test" - Tests Raspberry Pi connectivity

## Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with Python and Tkinter
- Uses OpenCV for camera streaming
- Designed for Raspberry Pi integration

## Support

For questions or issues, please open an issue on GitHub.
