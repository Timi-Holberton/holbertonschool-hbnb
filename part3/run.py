#!/usr/bin/env python3
from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)

# point d'entrée pour l'exécution de l'application
