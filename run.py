#!/usr/bin/env python3
"""
Launcher script for the whisper-query-parser application.
"""
import argparse
import os
import sys

from app import create_gradio_interface


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="whisper-query-parser - Voice to Text Application")
    
    parser.add_argument(
        "--port", 
        type=int, 
        default=7860, 
        help="Port to run the Gradio interface on"
    )
    
    parser.add_argument(
        "--host", 
        type=str, 
        default="0.0.0.0", 
        help="Host to run the Gradio interface on"
    )
    
    parser.add_argument(
        "--share", 
        action="store_true", 
        help="Create a public link for the interface"
    )
    
    parser.add_argument(
        "--debug", 
        action="store_true", 
        help="Run in debug mode"
    )
    
    return parser.parse_args()


def main():
    """Main entry point for the application."""
    args = parse_arguments()
    
    print("Starting whisper-query-parser application...")
    print(f"Interface will be available at http://localhost:{args.port}")
    
    if args.share:
        print("Public sharing is enabled - a public URL will be created")
    
    # Create and launch the Gradio interface
    interface = create_gradio_interface()
    
    try:
        interface.launch(
            server_name=args.host,
            server_port=args.port,
            share=args.share,
            debug=args.debug
        )
    except KeyboardInterrupt:
        print("\nShutting down whisper-query-parser application...")
    except Exception as e:
        print(f"Error starting the application: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main()) 