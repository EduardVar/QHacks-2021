from server import app, frontend, backend
import server.backend as bn

"""
This file runs the server at a given port
"""

FLASK_PORT = 8082

if __name__ == "__main__":
    app.run(debug=True, port=FLASK_PORT, host='127.0.0.1')
    