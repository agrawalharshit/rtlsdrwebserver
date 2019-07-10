import socket
import sys

HOST = ''
PORT = 4000
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # with open(sys.argv[1], "rb") as fd:
    #   with open(sys.argv[2], "rb") as key:
    s.connect((HOST, PORT))
    # fdata = fd.read()
    # kdata = key.read()
    while True:
        print('Enter a message:')
        message = input()
        # print(message.encode('ascii'))
        fdata = message.encode('ascii')
        # fdata = b'\x52\x69\x61'
        # key = [223, 88, 2, 185, 207, 24, 254, 192, 226, 63, 124, 244, 195, 152, 8, 4, 41, 110, 86, 62, 11, 181, 142,
        #       18, 103, 129, 66, 93, 249, 181, 11, 142, 197, 81, 19, 179, 54, 68, 55, 77, 60, 21, 47, 215, 194]
        key = [63, 94, 78, 114, 58, 73, 111, 119, 51, 99, 121, 25, 16, 62, 100, 85, 79, 38, 110, 27, 40, 2, 18, 57, 69,
               61,
               86, 47, 76, 74, 67, 41, 54, 13, 81, 125, 50, 109, 84, 48, 44, 30, 55, 65, 89, 4, 59, 24, 118, 82, 66,
               124,
               102, 83, 35, 91, 37, 12, 22, 39, 60, 7, 28, 122, 101, 75, 92, 77, 115, 72, 116, 90, 33, 97, 34, 3, 71,
               32,
               53, 106, 8, 15, 36, 19, 68, 109, 70, 112, 49, 6, 10, 31, 113, 95, 103, 21, 117, 11, 127, 96, 29, 120, 50]
        kdata = bytes(bytearray(key))
        # kdata = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' + \
        #    b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' + \
        #    b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        s.sendall(bytes(map(lambda x: x[0] ^ x[1], list(zip(fdata, kdata)))))

