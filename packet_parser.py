import struct
import datetime
from utils import bytes_to_int,bytes_to_float
def parse_header(header):
    packet_number=bytes_to_int(header[3:7])
    protocol_version=header[7:11].decode()
    imei=bytes_to_int(header[11:18])
    timestamp=bytes_to_int(header[18:22])
    return {'packet_number':packet_number,
            'protocol version':protocol_version,
            'imei':imei,
            'timestamp':timestamp
            }
def parse_body(body):
    start_byte=body[0:1].decode()
    if start_byte!='&':
        return None
    body_length=bytes_to_int(body[1:2])
    timestamp=bytes_to_int(body[2:6])
    latitude=bytes_to_float(body[6:10])
    longitude=bytes_to_float(body[10:14])
    speed=bytes_to_float(body[14:18])
    fuel_level=bytes_to_float(body[18:22])
    return {'start_byte':start_byte,
            'body_length':body_length,
            'timestamp':timestamp,
            'latitude':latitude,
            'longitude':longitude,
            'speed':speed,
            'fuel_level':fuel_level
            }
# Function to parse the received packet and return structured data
def parse_packet(packet):
    try:
        if packet[0:1].decode()=='$':
            packet_length=bytes_to_int(packet[1:2])
            header_length=bytes_to_int(packet[2:3])
            header=packet[0:header_length]
            body=packet[header_length:]
            header_data=parse_header(header)
            body_data=parse_body(body)
            packet_data={**header_data,**body_data}
            return packet_data,header_data['packet_number']


        return None,None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None,None


# Function to save the parsed data to a file
def save_parsed_data(parsed_data, file_path='parsed_data.txt'):
    with open(file_path, 'a') as file:
        file.write(f"{parsed_data}\n")
