import socket
import threading
import sys
from packet_handler import handle_client
from utils import monitor_input

# Global event to control server shutdown
server_running = threading.Event()
client_threads = []  # List to keep track of all threads

# Function to run the server
def run_server(host='0.0.0.0', port=12345):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen(5)  # Listen for incoming connections
        print(f"Server is listening on {host}:{port}")

        while server_running.is_set():  # Keep accepting new clients if server is running
            conn, addr = server_socket.accept()
            client_thread = threading.Thread(target=handle_client, args=(conn, addr))
            client_thread.start()
            client_threads.append(client_thread)
            print(f"Started thread for client {addr}")

# Function to stop the server gracefully
def stop_server():
    print("\nStopping server...")
    server_running.clear()  # Stop the server
    print("Server stopped.")

    # Wait for all client-handling threads to finish
    for thread in client_threads:
        thread.join()

if __name__ == "__main__":
    # Set the server_running event to True to start the server
    server_running.set()

    # Start a thread to monitor user input for quitting the server
    input_thread = threading.Thread(target=monitor_input, args=(stop_server,))
    input_thread.daemon = True  # Daemonize the input thread so it ends when the program ends
    input_thread.start()

    # Start the server
    run_server()

    # Once the server stops, exit the program
    print("Server has completely stopped. Exiting program.")
    sys.exit(0)
