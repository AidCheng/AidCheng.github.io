#!/usr/bin/env python3
import os
import subprocess
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import signal
import sys

class ReloadHandler(FileSystemEventHandler):
    def __init__(self):
        self.server_process = None
        self.start_server()

    def start_server(self):
        if self.server_process:
            self.server_process.terminate()
            self.server_process.wait()

        print("🚀 Starting server on http://localhost:8000")
        self.server_process = subprocess.Popen(
            [sys.executable, '-m', 'http.server', '8000'],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

    def on_modified(self, event):
        if event.is_directory:
            return

        # Only restart for relevant file changes
        if any(event.src_path.endswith(ext) for ext in ['.html', '.css', '.js', '.md', '.yml']):
            print(f"📝 File changed: {os.path.basename(event.src_path)}")
            print("🔄 Restarting server...")
            self.start_server()
            print("✅ Server restarted!")

    def stop(self):
        if self.server_process:
            self.server_process.terminate()
            self.server_process.wait()

def signal_handler(sig, frame):
    print("\n🛑 Stopping auto-reload...")
    handler.stop()
    observer.stop()
    sys.exit(0)

if __name__ == "__main__":
    # Set up signal handler for clean exit
    signal.signal(signal.SIGINT, signal_handler)

    print("🔥 Auto-reload server starting...")
    print("📁 Watching current directory for changes")
    print("🌐 Server will be available at http://localhost:8000")
    print("⏹️  Press Ctrl+C to stop")
    print("-" * 50)

    # Create event handler and observer
    handler = ReloadHandler()
    observer = Observer()
    observer.schedule(handler, path='.', recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        signal_handler(None, None)