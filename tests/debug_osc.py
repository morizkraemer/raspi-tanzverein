#!/usr/bin/env python3
"""
Debug OSC messages - test what QLC+ is receiving
"""

from pythonosc.udp_client import SimpleUDPClient
from pythonosc.dispatcher import Dispatcher
from pythonosc import osc_server
import time

# Configuration
IP = "127.0.0.1"
IN_PORT = 9001
OUT_PORT = 7700

def handle_osc_message(address, *args):
    """Handle incoming OSC messages"""
    print(f"📨 Received OSC: {address} {args}")
    print(f"   Address: '{address}'")
    print(f"   Args: {args}")
    print(f"   Arg types: {[type(arg).__name__ for arg in args]}")
    print(f"   Arg values: {[repr(arg) for arg in args]}")
    print("-" * 40)

def main():
    print("🔍 OSC Debug Listener")
    print(f"Listening on {IP}:{IN_PORT}")
    print("Send test messages to see what QLC+ receives")
    print("-" * 40)
    
    # Create dispatcher
    dispatcher = Dispatcher()
    dispatcher.set_default_handler(handle_osc_message)
    
    # Create and start server
    server = osc_server.ThreadingOSCUDPServer((IP, IN_PORT), dispatcher)
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Stopping debug listener...")
        server.shutdown()
        print("✅ Debug listener stopped.")

if __name__ == "__main__":
    main()
