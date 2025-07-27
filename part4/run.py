#!/usr/bin/env python3
"""
Entry point to start the Flask application.

This script creates and runs the Flask app instance with debug mode enabled.
"""

from app import create_app

app = create_app()

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)

# point d'entrée pour l'exécution de l'application
