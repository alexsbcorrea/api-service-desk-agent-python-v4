from flask_socketio import SocketIO, emit, join_room

socketio = SocketIO(cors_allowed_origins="*")

@socketio.on("connect")
def handle_connect(auth):
    print("Client connected")
    print(auth)
    join_room(auth.room)
    
