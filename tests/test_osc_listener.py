#!/usr/bin/env python3
"""
Simple OSC listener for testing - listens on port 9001 for any messages
"""

from pythonosc.dispatcher import Dispatcher
from pythonosc import osc_server
import threading

IP = "127.0.0.1"
PORT = 9001

def handle_osc_message(address, *args):
    """Handle incoming OSC messages"""
    print(f"📨 OSC: {address} {args}")

def main():
    print(f"🎧 OSC Listener starting on {IP}:{PORT}")
    print("Press Ctrl+C to stop")
    print("-" * 40)
    
    # Create dispatcher
    dispatcher = Dispatcher()
    
    # Map all messages to the handler (catch-all)
    dispatcher.set_default_handler(handle_osc_message)
    
    # Create and start server
    server = osc_server.ThreadingOSCUDPServer((IP, PORT), dispatcher)
    print(f"✅ Listening for OSC messages on {IP}:{PORT}")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Stopping OSC listener...")
        server.shutdown()
        print("✅ OSC listener stopped.")

if __name__ == "__main__":
    main()
