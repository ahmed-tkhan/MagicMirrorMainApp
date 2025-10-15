#!/usr/bin/env python3
"""
Test script for Magic Mirror Application
Validates code structure without requiring GUI
"""

import sys
import os

def test_configuration():
    """Test configuration module"""
    print("Testing configuration module...")
    import config
    
    # Check required settings
    assert hasattr(config, 'APP_TITLE')
    assert hasattr(config, 'APP_WIDTH')
    assert hasattr(config, 'APP_HEIGHT')
    assert hasattr(config, 'RASPI_HOST')
    assert hasattr(config, 'RASPI_PORT')
    assert hasattr(config, 'CAMERA_STREAM_URL')
    assert hasattr(config, 'VIDEO_OPTIONS')
    assert hasattr(config, 'MAX_NOTIFICATIONS')
    
    print(f"  ✓ App Title: {config.APP_TITLE}")
    print(f"  ✓ Window Size: {config.APP_WIDTH}x{config.APP_HEIGHT}")
    print(f"  ✓ Raspberry Pi: {config.RASPI_HOST}:{config.RASPI_PORT}")
    print(f"  ✓ Video Options: {len(config.VIDEO_OPTIONS)} cameras")
    print("Configuration module: PASSED\n")

def test_file_structure():
    """Test that all required files exist"""
    print("Testing file structure...")
    required_files = [
        'main.py',
        'config.py',
        'notification_manager.py',
        'video_control.py',
        'camera_stream.py',
        'requirements.txt',
        'README.md',
        'LICENSE'
    ]
    
    for filename in required_files:
        if os.path.exists(filename):
            print(f"  ✓ {filename}")
        else:
            print(f"  ✗ {filename} - MISSING!")
            return False
    
    print("File structure: PASSED\n")
    return True

def test_code_compilation():
    """Test that Python files compile without syntax errors"""
    print("Testing code compilation...")
    import py_compile
    
    python_files = [
        'main.py',
        'config.py',
        'notification_manager.py',
        'video_control.py',
        'camera_stream.py'
    ]
    
    for filename in python_files:
        try:
            py_compile.compile(filename, doraise=True)
            print(f"  ✓ {filename} compiles successfully")
        except py_compile.PyCompileError as e:
            print(f"  ✗ {filename} has syntax errors!")
            print(f"     Error: {e}")
            return False
    
    print("Code compilation: PASSED\n")
    return True

def test_module_structure():
    """Test module structure and imports"""
    print("Testing module structure...")
    
    # Test config module (doesn't require tkinter)
    try:
        import config
        print("  ✓ config module imports successfully")
    except ImportError as e:
        print(f"  ✗ config module import failed: {e}")
        return False
    
    # Check if tkinter is available for GUI modules
    try:
        import tkinter
        print("  ✓ tkinter is available")
        
        # Try importing GUI modules
        try:
            import notification_manager
            print("  ✓ notification_manager module imports successfully")
        except ImportError as e:
            print(f"  ✗ notification_manager import failed: {e}")
            return False
        
        try:
            import video_control
            print("  ✓ video_control module imports successfully")
        except ImportError as e:
            print(f"  ✗ video_control import failed: {e}")
            return False
        
        try:
            import camera_stream
            print("  ✓ camera_stream module imports successfully")
        except ImportError as e:
            print(f"  ✗ camera_stream import failed: {e}")
            return False
        
    except ImportError:
        print("  ⚠ tkinter not available (GUI modules can't be imported)")
        print("    This is expected in headless environments")
        print("    GUI modules will work on systems with GUI support")
    
    print("Module structure: PASSED\n")
    return True

def main():
    """Run all tests"""
    print("=" * 60)
    print("Magic Mirror Application - Test Suite")
    print("=" * 60)
    print()
    
    all_passed = True
    
    # Run tests
    try:
        test_configuration()
    except Exception as e:
        print(f"Configuration test FAILED: {e}\n")
        all_passed = False
    
    if not test_file_structure():
        all_passed = False
    
    if not test_code_compilation():
        all_passed = False
    
    if not test_module_structure():
        all_passed = False
    
    # Summary
    print("=" * 60)
    if all_passed:
        print("✓ ALL TESTS PASSED")
        print()
        print("The application is ready to run!")
        print("To start the application: python3 main.py")
    else:
        print("✗ SOME TESTS FAILED")
        print("Please check the errors above and fix them.")
        sys.exit(1)
    print("=" * 60)

if __name__ == "__main__":
    main()
