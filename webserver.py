import socket
import dns.resolver


HOST = ''
PORT = 80  # privileged port
print("Running webserver")
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(1)
    while True:
        conn, addr = s.accept()
        while True:
            data = conn.recv(1024)
            if not data: break
            print(data)
            html = "<!DOCTYPE html><html><body><p>Black Site Accessed From " + str(addr[0]) + ":" + str(
                addr[1]) + "</body></html>"
            header = "HTTP/1.1 200 OK\r\nServer: 4501\r\nContent-Length: " + str(len(html)) + "\r\n\r\n"
            conn.sendall((header + html).encode('ascii'))
