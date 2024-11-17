from utils import save_packet_to_file, calculate_crc32,bytes_to_int
from packet_parser import parse_packet, save_parsed_data

# Function to handle client connections
def handle_client(conn, addr):
    with conn:
        while True:  # Keep running if server is active
            try:
                packet = conn.recv(1024)
                if not packet:
                    conn.sendall(b'NO DATA RECEIVED')
                    break
                else:
                    crc=bytes_to_int(packet[-4:])
                    calculated_crc=calculate_crc32(packet[:-4])
                    if crc!=calculated_crc:
                        conn.sendall(b'ERROR 1') #crc mismatch
                        break
                    print(f"Received packet: {packet}",packet[0:1].decode())
                    if packet[0:1].decode()!='$':
                        conn.sendall(b'ERROR 2') #header not found
                        break
                    if bytes_to_int(packet[1:2])!=len(packet):
                        conn.sendall(b'ERROR 3') #packet length mismatch
                    else:
                        save_packet_to_file(packet)
                        actual_data=packet[:-4]
                        parsed_data,packet_number = parse_packet(actual_data)
                        if parsed_data:
                            save_parsed_data(parsed_data)
                            print(f"Parsed data: {parsed_data}")
                            print(f"ACK {packet_number}")
                            conn.sendall(b'ACK '+str(packet_number).encode())
                        else:
                            conn.sendall(b'ERROR 0') #invalid data 
                            break
            except Exception as e:
                print(f"Error handling client {addr}: {e}")
                break
        print(f"Closing connection with {addr}")
