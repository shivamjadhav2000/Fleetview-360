import zlib
import struct

# Convert float to bytes
def float_to_bytes(value):
    return struct.pack('>f', value)  # '>f' for 4-byte float (big-endian)

# Convert 4 bytes back to a float
def bytes_to_float(byte_data):
    return struct.unpack('>f', byte_data)[0]


def int_to_bytes(value, num_bytes):
    return value.to_bytes(num_bytes, byteorder='big')
def bytes_to_int(data):
    return int.from_bytes(data, byteorder='big')


def calculate_crc32(data):
    if isinstance(data, str):
        data = data.encode('utf-8')
    
    crc_value = zlib.crc32(data)
    
    return crc_value & 0xffffffff  # Ensures it's limited to 4 bytes (32 bits)
# Function to save packet data to a text file
def save_packet_to_file(packet_data):
    with open('received_packets.txt', 'wb') as file:
        file.write(packet_data + b'\n')
# Function to monitor user input to stop the server
def monitor_input(stop_server):
    while True:
        try:
            user_input = input()
            if user_input.lower() == 'quit':  # You can use 'quit' to stop the server
                stop_server()
                break
        except KeyboardInterrupt:
            stop_server()
            break
