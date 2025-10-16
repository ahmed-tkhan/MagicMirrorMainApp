# Magic Mirror Control Center - UI Overview

## Application Layout

The Magic Mirror Control Center features a modern, dark-themed interface divided into three main panels:

```
┌─────────────────────────────────────────────────────────────────┐
│  ✨ Magic Mirror Control Center                                │
│  Central Control for Raspberry Pi Camera System                 │
├──────────────┬─────────────────┬──────────────────────────────┤
│              │                 │                                │
│ Notifications│  Video Control  │      Camera Stream             │
│    Panel     │     Panel       │         Panel                  │
│   (30%)      │     (25%)       │         (45%)                  │
│              │                 │                                │
│ ┌──────────┐ │ ┌─────────────┐ │  ┌──────────────────────┐    │
│ │ 📢 Motion│ │ │ 🎥 Video    │ │  │  📹 Camera Stream    │    │
│ │ Detection│ │ │   Control   │ │  │                      │    │
│ │ Notifica-│ │ │   Panel     │ │  │                      │    │
│ │ tions    │ │ │             │ │  │   [Video Display]    │    │
│ │          │ │ │ Camera:     │ │  │                      │    │
│ │ ┌──────┐ │ │ │ [Dropdown]  │ │  │                      │    │
│ │ │ALERT │ │ │ │             │ │  │                      │    │
│ │ │Motion│ │ │ │ [▶ Play]    │ │  └──────────────────────┘    │
│ │ │      │ │ │ │ [⏹ Stop]    │ │                               │
│ │ └──────┘ │ │ │ [🔄 Refresh]│ │  [▶ Start] [⏹ Stop]          │
│ │          │ │ │             │ │  [📷 Snapshot]               │
│ │ ┌──────┐ │ │ │ Quality:    │ │                               │
│ │ │INFO  │ │ │ │ [720p]      │ │  Stream URL: 192.168.1.100   │
│ │ │System│ │ │ │             │ │  Status: Streaming            │
│ │ │Ready │ │ │ │ FPS: [30]   │ │  Resolution: 640x480         │
│ │ └──────┘ │ │ │             │ │                               │
│ └──────────┘ │ │ Status:     │ │                               │
│              │ │ ● Connected │ │                               │
│              │ └─────────────┘ │                               │
└──────────────┴─────────────────┴──────────────────────────────┘
│ Ready                          ● Raspberry Pi: Connected        │
└─────────────────────────────────────────────────────────────────┘
```

## Panel Details

### Left Panel - Notifications (📢)

**Features:**
- Scrollable list of motion detection alerts
- Color-coded notification types:
  - 🔵 INFO - Blue (System information)
  - 🟡 WARNING - Orange (Warnings)
  - 🔴 ALERT - Red (Motion detected)
  - ⚫ ERROR - Dark Red (Errors)
- Each notification shows:
  - Title with type badge
  - Timestamp
  - Detailed message
  - Dismiss button (✕)
- Auto-scrolling for new notifications
- Maximum 10 notifications displayed

**Visual Style:**
```
┌────────────────────────────────┐
│ 📢 Motion Detection           │
│    Notifications              │
├────────────────────────────────┤
│ ┌──────────────────────────┐  │
│ │ Motion Detected [ALERT]  │  │
│ │ 2025-10-15 16:45:23     │  │
│ │                          │  │
│ │ Motion detected at Front │  │
│ │ Door. Check camera feed. │  │
│ │                [✕ Dismiss]│  │
│ └──────────────────────────┘  │
│                               │
│ ┌──────────────────────────┐  │
│ │ System Ready [INFO]      │  │
│ │ 2025-10-15 16:40:00     │  │
│ │                          │  │
│ │ All systems operational  │  │
│ │                [✕ Dismiss]│  │
│ └──────────────────────────┘  │
└────────────────────────────────┘
```

### Middle Panel - Video Control (🎥)

**Features:**
- Camera source selection dropdown
- Quick camera buttons (Cam 1-4)
- Playback controls:
  - ▶ Play/⏸ Pause (toggles)
  - ⏹ Stop
  - 🔄 Refresh
- Stream quality selector (240p to 1080p)
- Frame rate slider (5-60 FPS)
- Connection status indicator
- Raspberry Pi information display

**Visual Style:**
```
┌────────────────────────────┐
│ 🎥 Video Control Panel    │
├────────────────────────────┤
│ ┌────────────────────────┐ │
│ │ Video Source Selection │ │
│ │                        │ │
│ │ Select Camera:         │ │
│ │ [Camera 1 - Front Door▼│ │
│ │                        │ │
│ │ [Cam 1][Cam 2][Cam 3]  │ │
│ └────────────────────────┘ │
│                            │
│ ┌────────────────────────┐ │
│ │ Playback Controls      │ │
│ │                        │ │
│ │  [▶ Play]  [⏹ Stop]   │ │
│ │     [🔄 Refresh]       │ │
│ └────────────────────────┘ │
│                            │
│ ┌────────────────────────┐ │
│ │ Stream Quality         │ │
│ │                        │ │
│ │ Quality: [High (720p)▼]│ │
│ │ FPS: [━━●━━━━] 30      │ │
│ └────────────────────────┘ │
│                            │
│ ┌────────────────────────┐ │
│ │ Connection Status      │ │
│ │                        │ │
│ │ ● Streaming           │ │
│ │ Pi: 192.168.1.100:8080│ │
│ └────────────────────────┘ │
└────────────────────────────┘
```

### Right Panel - Camera Stream (📹)

**Features:**
- Live video display area (640x480 default)
- Stream control buttons:
  - ▶ Start Stream
  - ⏹ Stop Stream
  - 📷 Snapshot
- Stream information:
  - URL display
  - Connection status
  - Resolution info
- Placeholder when not streaming
- Real-time frame updates

**Visual Style:**
```
┌──────────────────────────────────┐
│ 📹 Camera Stream                │
├──────────────────────────────────┤
│                                  │
│  ┌────────────────────────────┐ │
│  │                            │ │
│  │                            │ │
│  │        [Camera Icon]       │ │
│  │   Camera Stream Offline    │ │
│  │                            │ │
│  │ Click 'Start Stream'       │ │
│  │     to connect             │ │
│  │                            │ │
│  └────────────────────────────┘ │
│                                  │
│  [▶ Start] [⏹ Stop] [📷 Snap]  │
│                                  │
│ ┌──────────────────────────────┐│
│ │ Stream Information           ││
│ │                              ││
│ │ URL: http://192.168.1.100... ││
│ │ Status: Not Connected        ││
│ │ Resolution: 640x480          ││
│ └──────────────────────────────┘│
└──────────────────────────────────┘
```

## Menu Bar

### File Menu
- **Settings**: Open configuration dialog
- **Exit**: Close application

### Tools Menu
- **Test Motion Detection**: Simulate motion event
- **Clear Notifications**: Remove all notifications
- **Connection Test**: Test Raspberry Pi connection

### Help Menu
- **Documentation**: View help information
- **About**: Application information

## Status Bar

Located at the bottom of the window:
```
┌─────────────────────────────────────────────────┐
│ Ready              ● Raspberry Pi: Connected    │
└─────────────────────────────────────────────────┘
```

## Color Scheme

The application uses a modern dark theme:

- **Background**: Dark gray (#1a1a1a, #34495e)
- **Headers**: Dark blue-gray (#2c3e50)
- **Primary Text**: White (#ffffff)
- **Secondary Text**: Light gray (#bdc3c7, #95a5a6)
- **Accents**: Blue (#3498db)
- **Success**: Green (#27ae60)
- **Warning**: Orange (#f39c12)
- **Error**: Red (#e74c3c, #c0392b)

## Interaction Flow

### Starting Video Stream

1. User selects camera from dropdown or quick button
   → Application updates selection
   → Status bar shows selected camera

2. User clicks "Play" button
   → Button changes to "Pause"
   → Status indicator turns green
   → Application sends command to Raspberry Pi

3. User clicks "Start Stream" in camera panel
   → Video canvas shows live feed
   → Stream info updates
   → Start button becomes disabled, Stop button enabled

### Receiving Motion Alert

1. Motion detection service detects movement
   → Application receives notification
   → New alert appears in notification panel (red)
   → Notification includes camera name and timestamp
   → Status bar briefly shows alert message

2. User reviews notification
   → User can dismiss individual alert
   → Or use Tools > Clear Notifications for all

### Taking Snapshot

1. User clicks "Snapshot" button while streaming
   → Current frame is captured
   → Status shows "Snapshot saved: filename.png"
   → Message auto-clears after 3 seconds

## Responsive Behavior

- **Minimum Window Size**: 1000x600 pixels
- **Default Size**: 1200x800 pixels
- **Panel Proportions**: 30% / 25% / 45%
- **Scrollable Areas**: Notifications panel auto-scrolls
- **Resizable Window**: All panels adjust proportionally

## Accessibility Features

- Clear visual hierarchy
- High contrast text
- Large, easy-to-click buttons
- Color-coded notifications
- Status indicators
- Descriptive labels
- Keyboard navigation support (via Tkinter)

## Performance Indicators

- **Status Bar**: Shows connection state
- **Stream Status**: Shows streaming state
- **Notification Count**: Limited to 10 for performance
- **Frame Rate Display**: Shows current FPS setting
- **Quality Selector**: User can adjust for performance

## Error States

The application gracefully handles errors:

- **No Camera**: Shows placeholder with message
- **Connection Lost**: Red status indicator + error notification
- **Stream Failure**: Returns to placeholder view
- **Raspberry Pi Offline**: Grayed out status indicator

## Future UI Enhancements

Potential additions (placeholders for future development):
- Analytics dashboard
- Recording controls
- Multi-camera grid view
- Motion event timeline
- Settings dialog with form
- Dark/light theme toggle
- Fullscreen mode
- Picture-in-picture for multiple streams
