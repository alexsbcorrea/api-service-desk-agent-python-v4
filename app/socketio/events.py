from flask_socketio import SocketIO, emit

socketio = SocketIO(cors_allowed_origins="*")

@socketio.on("connect")
def handle_connect():
    print("Client connected")
