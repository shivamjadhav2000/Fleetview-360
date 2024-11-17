# Fleetview-360

Fleetview-360 is a scalable solution designed to handle fleet management and device tracking. It provides live tracking and fuel monitoring capabilities, built to manage IoT devices and facilitate communication through the Socket.IO module in Python. The system leverages multithreading to handle individual devices and exchange information such as sensor data. A custom protocol is used to parse or represent data in just 54 bytes.

# Telemetry Data Simulation and Packet Validation

This project simulates telemetry data transmission between multiple devices and a server, ensuring data integrity and proper parsing of packets. It handles CRC validation, packet parsing, and supports a server-client architecture where devices (simulated) send data packets to the server.

## Features

- **Simulated Devices**: Devices generate random telemetry data including `IMEI`, `latitude`, `longitude`, `speed`, and `fuel level`.
- **Packet Format**: Data packets include a header and body, validated using CRC32 checks.
- **Error Handling**: Includes checks for CRC mismatch, header format errors, and packet length mismatches.
- **Threading**: Multiple devices can connect to the server, with threading support for simultaneous communication.
- **Data Parsing**: The server parses incoming packets, extracts telemetry data, and saves it to a file.
  
## Components

### 1. **Server (`server.py`)**

- The server listens for incoming connections on a specified IP and port (`127.0.0.1:12345`).
- It processes the data packets sent by the devices, validates the packet integrity, and parses the data.
- The server sends acknowledgments (`ACK`) or error messages in response to packets.

### 2. **Simulator (`simulator.py`)**

- The simulator generates packets with random telemetry data such as `latitude`, `longitude`, `speed`, and `fuel level` for each device.
- It sends these packets to the server at regular intervals, simulating real-time data transmission.

### 3. **Packet Parser (`packet_parser.py`)**

- Parses the header and body of each packet, extracting critical data like `IMEI`, `timestamp`, `latitude`, `longitude`, etc.
- Saves parsed data to a text file.

### 4. **Utility Functions (`utils.py`)**

- Provides functions for:
  - Converting integers and floats to bytes and vice versa.
  - Calculating CRC32 checksums.
  - Saving packets and parsed data to files.
  - Monitoring user input to stop the server.

## Setup

### Prerequisites

- Python 3.x
- Required libraries:
  - `socket`
  - `struct`
  - `random`
  - `time`
  - `threading`
  - `zlib`
  

```bash
.
├── server.py         # Server script to handle incoming packets
├── simulator.py      # Simulator script to generate and send telemetry data
├── packet_parser.py  # Functions to parse incoming packets
├── utils.py          # Utility functions for packet processing
├── received_packets.txt  # File to store received packets
├── parsed_data.txt       # File to store parsed data
└── README.md         # This file


Running the Server
Open a terminal window and navigate to the project directory.
Start the server by running:
bash
Copy code
python server.py
The server will begin listening for incoming connections from devices.

Running the Device Simulator
Open a new terminal window and navigate to the project directory.
Start the simulator by running:
bash
Copy code
python simulator.py
The simulator will generate random packets and send them to the server at regular intervals (2 seconds by default).

Example Output
Server Output:

arduino
Copy code
Connected to server at ('127.0.0.1', 12345)
Received packet: b'$...'
Parsed data: {'packet_number': 12345, 'protocol version': 'v1.0', ...}
ACK 12345
Simulator Output:

bash
Copy code
Sending packet: b'$...'
Received response: b'ACK 12345'
Error Handling
If there is an issue with the packet (e.g., CRC mismatch, header not found), the server will send an error message back to the device.

Possible error messages include:

CRC mismatch
Header not found
Packet length mismatch
Invalid data
Stopping the Server
To stop the server, simply type quit in the terminal where the server is running.