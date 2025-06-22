# import asyncio
# import websockets
# import json
# from datetime import datetime
# from typing import Set

# # Store all connected clients
# connected_clients: Set[websockets.WebSocketServerProtocol] = set()

# async def chat_server(websocket, path):
#     # Register new client
#     connected_clients.add(websocket)
#     print(f"New client connected. Total clients: {len(connected_clients)}")
    
#     try:
#         username = ""
        
#         async for message in websocket:
#             try:
#                 data = json.loads(message)
                
#                 if data["type"] == "set_username":
#                     # Set the username for this connection
#                     username = data["username"]
#                     print(f"User {username} joined the chat")
                    
#                     # Notify all clients about new user
#                     join_message = {
#                         "type": "system",
#                         "text": f"{username} joined the chat",
#                         "timestamp": datetime.now().isoformat()
#                     }
                    
#                     await broadcast(join_message)
                    
#                 elif data["type"] == "message":
#                     print(f"Message from {username}: {data['text']}")
                    
#                     # Forward message to all clients
#                     chat_message = {
#                         "type": "message",
#                         "username": username,
#                         "text": data['text'],
#                         "timestamp": datetime.now().isoformat()
#                     }
                    
#                     await broadcast(chat_message)
                    
#             except json.JSONDecodeError:
#                 print("Invalid JSON received")
#             except KeyError:
#                 print("Invalid message format")
                
#     finally:
#         # Remove client when they disconnect
#         connected_clients.remove(websocket)
#         if username:
#             print(f"User {username} left the chat")
            
#             # Notify all clients about disconnection
#             leave_message = {
#                 "type": "system",
#                 "text": f"{username} left the chat",
#                 "timestamp": datetime.now().isoformat()
#             }
            
#             await broadcast(leave_message)

# async def broadcast(message):
#     """Send a message to all connected clients"""
#     if connected_clients:
#         message_json = json.dumps(message)
#         await asyncio.gather(
#             *[client.send(message_json) for client in connected_clients]
#         )

# if __name__ == "__main__":
#     print("Starting WebSocket chat server on ws://localhost:8765")
    
#     start_server = websockets.serve(
#         chat_server,
#         "localhost",
#         8765,
#         ping_interval=60,
#         ping_timeout=30
#     )
    
#     asyncio.get_event_loop().run_until_complete(start_server)
#     asyncio.get_event_loop().run_forever()


# import asyncio
# import websockets
# import json
# from datetime import datetime
# from typing import Set
# from websockets.legacy.server import WebSocketServerProtocol

# # Store all connected clients
# connected_clients: Set[WebSocketServerProtocol] = set()

# async def chat_server(websocket, path):
#     connected_clients.add(websocket)
#     print(f"New client connected. Total clients: {len(connected_clients)}")
    
#     username = ""

#     try:
#         async for message in websocket:
#             try:
#                 data = json.loads(message)
                
#                 if data["type"] == "set_username":
#                     username = data["username"]
#                     print(f"User {username} joined the chat")
                    
#                     join_message = {
#                         "type": "system",
#                         "text": f"{username} joined the chat",
#                         "timestamp": datetime.now().isoformat()
#                     }
#                     await broadcast(join_message)

#                 elif data["type"] == "message":
#                     print(f"Message from {username}: {data['text']}")
                    
#                     chat_message = {
#                         "type": "message",
#                         "username": username,
#                         "text": data['text'],
#                         "timestamp": datetime.now().isoformat()
#                     }
#                     await broadcast(chat_message)

#             except (json.JSONDecodeError, KeyError):
#                 print("Invalid message received")

#     finally:
#         connected_clients.remove(websocket)
#         if username:
#             print(f"User {username} left the chat")

#             leave_message = {
#                 "type": "system",
#                 "text": f"{username} left the chat",
#                 "timestamp": datetime.now().isoformat()
#             }
#             await broadcast(leave_message)

# async def broadcast(message):
#     """Send a message to all connected clients"""
#     if connected_clients:
#         message_json = json.dumps(message)
#         await asyncio.gather(*(client.send(message_json) for client in connected_clients))

# async def main():
#     async with websockets.serve(
#         chat_server,
#         "localhost",
#         8765,
#         ping_interval=60,
#         ping_timeout=30
#     ):
#         print("WebSocket chat server started on ws://localhost:8765")
#         await asyncio.Future()  # run forever

# if __name__ == "__main__":
#     asyncio.run(main())

import asyncio
import websockets
import json
from datetime import datetime
from typing import Set
from websockets.legacy.server import WebSocketServerProtocol

# Menyimpan semua klien yang terhubung
connected_clients: Set[WebSocketServerProtocol] = set()

async def chat_server(websocket: WebSocketServerProtocol):
    connected_clients.add(websocket)
    print(f"Client baru terhubung. Total klien: {len(connected_clients)}")

    username = ""

    try:
        async for message in websocket:
            try:
                data = json.loads(message)

                if data["type"] == "set_username":
                    username = data["username"]
                    print(f"Pengguna {username} bergabung ke obrolan.")

                    join_message = {
                        "type": "system",
                        "text": f"{username} joined the chat",
                        "timestamp": datetime.now().isoformat()
                    }
                    await broadcast(join_message)

                elif data["type"] == "message":
                    print(f"Pesan dari {username}: {data['text']}")

                    chat_message = {
                        "type": "message",
                        "username": username,
                        "text": data["text"],
                        "timestamp": datetime.now().isoformat()
                    }
                    await broadcast(chat_message)

            except (json.JSONDecodeError, KeyError):
                print("Pesan tidak valid diterima")

    finally:
        connected_clients.remove(websocket)
        if username:
            print(f"Pengguna {username} keluar dari obrolan.")

            leave_message = {
                "type": "system",
                "text": f"{username} left the chat",
                "timestamp": datetime.now().isoformat()
            }
            await broadcast(leave_message)

async def broadcast(message: dict):
    """Mengirim pesan ke semua klien"""
    if connected_clients:
        message_json = json.dumps(message)
        await asyncio.gather(*(client.send(message_json) for client in connected_clients))

async def main():
    async with websockets.serve(
        chat_server,
        "0.0.0.0",
        8787,
        ping_interval=60,
        ping_timeout=30
    ):
        print("WebSocket chat server berjalan di ws://localhost:8765")
        await asyncio.Future()  # Menjaga agar server tetap berjalan

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nServer dihentikan oleh pengguna.")

