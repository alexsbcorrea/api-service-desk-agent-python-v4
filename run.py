from app import create_app
from app.socketio.events import socketio

app = create_app()

if __name__ == "__main__":
    socketio.run(app, host="localhost", port=5000, debug=True)