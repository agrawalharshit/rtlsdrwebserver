import socket
from binascii import hexlify, crc32
from struct import pack
from playsounds import *

HOST = ''
PORT = 4000
tone1 = gen_tone(100, 0.015625, 900)
tone2 = gen_tone(100, 0.015625, 300)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
print('Running Server')
while True:
    conn, addr = s.accept()
    while True:
        data = conn.recv(4096)
        if not data: break
        header = b'\x81' + pack('B', len(data)) + pack('I', crc32(data))
        # array = list(map(lambda x: int(x), list(bin(int(hexlify(data), 16))[2:])))
        array = list(map(lambda x: int(x), ''.join(format(x, '08b') for x in header + data)))
        modulateFSK(array, tone1, tone2)
        # For printing / debugging
        data = ''.join(format(x, '') for x in array)
        print(data)

