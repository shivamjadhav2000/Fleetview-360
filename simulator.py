import socket
import struct
import time
from datetime import datetime as dt
import random
import threading
from utils import int_to_bytes,float_to_bytes,calculate_crc32

ERROR_LOOKUP = {
    1: "CRC mismatch",
    2: "Header not found",
    3: "Packet length mismatch",
    0: "Invalid data"
}

class DataPacket:
    def __init__(self,imei,protocolversion='v1',packetcount=0,packet_frequency=2,lat=0,lng=0,fuellevel=0,active=1,speed=0):
        self.imei = imei
        self.protocolversion = protocolversion
        self.packetcount = packetcount
        self.fuellevel = fuellevel if fuellevel else random.randint(0,100)
        self.lat=lat if lat else random.uniform(20,90)
        self.lng=lng if lng else random.uniform(-180,180)
        self.active=active
        self.speed=speed if speed else random.randint(0,100)
        self.packet_number=0
        self.packet_frequency=packet_frequency
    def get_lat(self):
        self.lat += random.uniform(-0.00001, 0.00001)  # Move a few meters
        print(f"Lat: {self.lat}")
        p=float_to_bytes(self.lat)
        print("len== lat=",len(p))
        return p
    def get_lng(self):
        self.lng += random.uniform(-0.00001, 0.00001)
        print(f"Lng: {self.lng}")
        return float_to_bytes(self.lng)
    def get_speed(self):
        self.speed += random.uniform(-0.5, 0.5)
        print(f"Speed: {self.speed}")
        return float_to_bytes(self.speed)
    def get_fuel_level(self):
        self.fuellevel += random.uniform(-2.5, 0)
        print(f"Fuel level: {self.fuellevel}")
        return float_to_bytes(self.fuellevel)
    def get_packet_number(self):
        max_packet_number = 60*60*24
        max_packet_number = max_packet_number//self.packet_frequency
        if self.packet_number >=max_packet_number:
            self.packet_number=0
        self.packet_number+=1
        return int_to_bytes(self.packet_number,4)
    def get_header(self):
        header = b'$'
        header+= int_to_bytes(51,1)
        header+= int_to_bytes(23,1)
        header+=self.get_packet_number()
        header+=b'v1.0'
        header+= int_to_bytes(self.imei,7)
        header+= int_to_bytes(int(dt.now().timestamp()),4)
        header+=b'@'
        return header
    def get_body(self):
        packet = b'&'  # Start byte
        packet+= int_to_bytes(24,1)
        packet+= int_to_bytes(int(dt.now().timestamp()),4)
        packet+= self.get_lat()
        packet+= self.get_lng()
        packet+=self.get_speed()
        packet+=self.get_fuel_level()
        packet+=self.active.to_bytes(1,byteorder='big')
        packet+=b'#'  # End byte
        return packet
    def generate_packet(self):
        header = self.get_header()
        body = self.get_body()
        print(f"Header: {header}")
        print(f"Body: {body}")
        crc=calculate_crc32(header+body)
        crc=int_to_bytes(crc,4)
        return header+body+crc




def send_data(device):
    server_address = ('127.0.0.1', 12345)  # Replace with actual server IP and port
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(server_address)
    send_frequency=2
    print(f"Connected to server at {server_address}")
    Packet_generator=DataPacket(device,packet_frequency=send_frequency)
    while True:
        packet=Packet_generator.generate_packet()
        print(f"Sending packet: {packet}")
        client_socket.sendall(packet)
        res=client_socket.recv(1024)
        print(f"Received response: {res}")
        ACK,packet_number=res.split()
        if ACK==b'ACK':
            print(f"Received ACK for packet number: {packet_number.decode()}")
        else:
            print(f"Error sending packet: {ERROR_LOOKUP[int(packet_number)]}")
        time.sleep(send_frequency)

# Server communication
def main():
    number_of_devices=30
    devices={i for i in range(10**14,10**14+number_of_devices)}
    print(devices)
    active_devices=set()
    device_Thread=dict()
    while True:
        new_devices=active_devices^devices
        for device in new_devices:
            if device in devices:
                client_thread=threading.Thread(target=send_data,args=(device,))
                client_thread.daemon=True
                client_thread.start()
                active_devices.add(device)
            else:
                device_Thread[device].stop()
                del device_Thread[device]
                active_devices.remove(device)
        time.sleep(5)
    
    
    


if __name__ == "__main__":
    main()
