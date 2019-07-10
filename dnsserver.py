import socket
from array import array

HOST = ''
PORT = 53  # privileged port
blacksiteip = array('B', [172, 25, 174, 114])
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.bind((HOST, PORT))
    # s.listen(1)
    while True:
        # conn, addr = s.accept()
        while True:
            data, addr = s.recvfrom(4096) # Receive data
            if not data: break
            print(data)
            index = data.decode('ascii', errors='ignore').find("blacksite") - 1 # Decode ascii
            resrec = array('H', [0x0cc0, 0x0100, 0x0100, 0xff0f, 0xff0f, 0x0400])  # Build DNS Header for NA
            response = bytearray(data + resrec + blacksiteip)   # NA
            # Flags
            response[2] |= 0x80  #  Answer Response
            response[7] = 0x01  # One Answer
            s.sendto(response, addr) # Send it



