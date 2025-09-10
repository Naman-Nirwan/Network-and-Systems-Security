from pwn import cyclic

padding_test = cyclic(300)  # Generate a unique 300-character pattern

req = (
    b"GET /" + padding_test + b" HTTP/1.0\r\n"
    b"Host: localhost\r\n"
    b"\r\n"
)

# Send the request
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("localhost", 8080))
sock.send(req)
sock.close()

