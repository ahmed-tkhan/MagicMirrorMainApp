# Setup and Installation Guide

## Quick Start

### 1. System Requirements

- **Operating System**: Windows, macOS, or Linux
- **Python Version**: 3.8 or higher
- **Display**: GUI-enabled system (not headless server)

### 2. Install Python

#### Windows
Download Python from [python.org](https://www.python.org/downloads/) and run the installer.
Make sure to check "Add Python to PATH" during installation.

#### macOS
```bash
# Using Homebrew
brew install python3

# Or download from python.org
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install python3 python3-pip python3-tk
```

#### Linux (Fedora/RHEL)
```bash
sudo dnf install python3 python3-pip python3-tkinter
```

### 3. Clone the Repository

```bash
git clone https://github.com/ahmed-tkhan/MagicMirrorMainApp.git
cd MagicMirrorMainApp
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

If you encounter permission errors, use:
```bash
pip install --user -r requirements.txt
```

### 5. Configure the Application

Edit `config.py` to match your setup:

```python
# Change these to match your Raspberry Pi
RASPI_HOST = "192.168.1.100"  # Your Raspberry Pi IP address
RASPI_PORT = 8080              # Your Raspberry Pi port

# Change this to your camera stream URL
CAMERA_STREAM_URL = "http://192.168.1.100:8081/stream"

# Customize video options
VIDEO_OPTIONS = [
    "Camera 1 - Front Door",
    "Camera 2 - Back Yard",
    "Camera 3 - Garage",
    "Camera 4 - Living Room"
]
```

### 6. Run the Application

```bash
python3 main.py
```

Or on Windows:
```bash
python main.py
```

## Troubleshooting

### "No module named 'tkinter'"

**On Ubuntu/Debian:**
```bash
sudo apt install python3-tk
```

**On Fedora/RHEL:**
```bash
sudo dnf install python3-tkinter
```

**On macOS:**
Tkinter should be included with Python. If not, reinstall Python from python.org.

**On Windows:**
Tkinter is included with Python. Reinstall Python if needed.

### "No module named 'cv2'"

Install OpenCV:
```bash
pip install opencv-python
```

### Camera Not Opening

The application tries to use your default camera (index 0). If you don't have a camera:
- The stream will show a placeholder
- You can still test all other features
- Update `camera_stream.py` to use your specific camera URL

### Raspberry Pi Connection Issues

1. Verify the IP address:
```bash
ping 192.168.1.100  # Replace with your Pi's IP
```

2. Check if the Pi's service is running
3. Verify firewall settings on both machines
4. Ensure both devices are on the same network

## Advanced Configuration

### Custom Window Size

In `config.py`:
```python
APP_WIDTH = 1920   # Your preferred width
APP_HEIGHT = 1080  # Your preferred height
```

### Motion Detection Settings

In `config.py`:
```python
MOTION_CHECK_INTERVAL = 5000  # Check every 5 seconds (in milliseconds)
MOTION_NOTIFICATION_DURATION = 10000  # Show for 10 seconds
```

### Video Quality Settings

The application supports multiple quality presets:
- Low (240p)
- Medium (480p)
- High (720p)
- Ultra (1080p)

Users can select quality from the Video Control Panel.

## Integration with Raspberry Pi

### Setting Up the Raspberry Pi Backend

The application expects a REST API on your Raspberry Pi:

**Required Endpoints:**

1. **Control Endpoint** (`/api/control`)
   - Method: POST
   - Body: `{"command": "play", "params": {"camera": "Camera 1"}}`

2. **Video Endpoint** (`/api/video`)
   - Method: GET
   - Returns: Video stream or status

3. **Stream Endpoint** (`/stream`)
   - Method: GET
   - Returns: MJPEG or H.264 stream

### Example Raspberry Pi Flask Server

Create this on your Raspberry Pi:

```python
from flask import Flask, request, jsonify, Response
import cv2

app = Flask(__name__)

@app.route('/api/control', methods=['POST'])
def control():
    data = request.json
    command = data.get('command')
    params = data.get('params', {})
    
    # Handle command
    print(f"Received command: {command} with params: {params}")
    
    return jsonify({"status": "success", "command": command})

@app.route('/api/video', methods=['GET'])
def video():
    return jsonify({"status": "active", "camera": "default"})

@app.route('/stream')
def stream():
    def generate():
        camera = cv2.VideoCapture(0)
        while True:
            success, frame = camera.read()
            if not success:
                break
            ret, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
    
    return Response(generate(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
```

## Testing the Application

Run the test suite:
```bash
python3 test_app.py
```

This will verify:
- Configuration is correct
- All files are present
- Code compiles without errors
- Modules can be imported

## Running in Development Mode

For development with auto-reload, you can use:
```bash
# Watch for file changes (requires watchdog)
pip install watchdog
python3 main.py
```

## Building for Distribution

### Using PyInstaller

Install PyInstaller:
```bash
pip install pyinstaller
```

Create executable:
```bash
pyinstaller --onefile --windowed --name "MagicMirror" main.py
```

The executable will be in the `dist/` folder.

## Next Steps

1. Configure your Raspberry Pi IP and ports
2. Set up the Raspberry Pi backend (see Integration section)
3. Test the connection using "Tools > Connection Test"
4. Customize camera names in `config.py`
5. Start monitoring your cameras!

## Support

If you encounter any issues:
1. Check this setup guide
2. Review the README.md
3. Check the test output: `python3 test_app.py`
4. Open an issue on GitHub with details about your system and error messages
