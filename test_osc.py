#!/usr/bin/env python3
"""
OSC Test Script
Tests both sending and receiving OSC messages
"""

from pythonosc.udp_client import SimpleUDPClient
from pythonosc.dispatcher import Dispatcher
from pythonosc import osc_server
import threading
import time

# Configuration
IP = "127.0.0.1"
IN_PORT = 9001
OUT_PORT = 7700

def handle_osc_message(address, *args):
    """Handle incoming OSC messages"""
    print(f"📨 RECEIVED: {address} {args}")

def start_osc_server():
    """Start OSC server"""
    dispatcher = Dispatcher()
    dispatcher.set_default_handler(handle_osc_message)
    
    server = osc_server.ThreadingOSCUDPServer((IP, IN_PORT), dispatcher)
    print(f"🔍 OSC Server listening on {IP}:{IN_PORT}")
    server.serve_forever()

def send_test_messages():
    """Send test messages to ourselves"""
    client = SimpleUDPClient(IP, IN_PORT)
    
    print("📤 Sending test messages...")
    
    # Send various test messages
    test_messages = [
        ("/test", []),
        ("/hello", ["world"]),
        ("/numbers", [1, 2, 3]),
        ("/float", [3.14]),
        ("/led", [1]),
        ("/01/dmx/0", [255])
    ]
    
    for address, args in test_messages:
        print(f"📤 SENDING: {address} {args}")
        client.send_message(address, args)
        time.sleep(0.5)
    
    print("✅ Test messages sent!")

def main():
    print("🧪 OSC COMMUNICATION TEST")
    print("=" * 40)
    
    # Start OSC server
    print("Starting OSC server...")
    server_thread = threading.Thread(target=start_osc_server, daemon=True)
    server_thread.start()
    
    # Wait a moment for server to start
    time.sleep(1)
    
    # Send test messages
    send_test_messages()
    
    # Keep running to receive messages
    print("\n⏳ Waiting for messages... (Press Ctrl+C to stop)")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n👋 Test completed!")

if __name__ == "__main__":
    main()
