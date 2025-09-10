import socket, ssl, sys, pprint

hostname = sys.argv[1]
port = 443
# cadir = '/etc/ssl/certs'
cadir = "./certs/"  

# Set up the TLS context
context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
context.load_verify_locations(capath=cadir)
context.verify_mode = ssl.CERT_REQUIRED
context.check_hostname = True

# Create TCP connection
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((hostname, port))
input("After making TCP connection. Press any key to continue ...")

# Add the TLS
ssock = context.wrap_socket(sock, server_hostname=hostname,
do_handshake_on_connect=False)
ssock.do_handshake() # Start the handshake
pprint.pprint(ssock.getpeercert())
print(ssock.cipher())
input("After handshake. Press any key to continue ...")

# # --- Send HTTP Request ---
# request = b"GET / HTTP/1.0\r\nHost: " + hostname.encode('utf-8') + b"\r\n\r\n"

# ssock.sendall(request)

# # --- Read HTTP Response ---
# response = ssock.recv(2048)
# print("\n🌐 HTTP Response:")
# while response:
#     pprint.pprint(response.split(b"\r\n"))
#     response = ssock.recv(2048)

request = b"GET /favicon.ico HTTP/1.0\r\nHost: " + hostname.encode('utf-8') + b"\r\n\r\n"
ssock.sendall(request)

response = ssock.recv(2048)
while response:
    pprint.pprint(response.split(b"\r\n"))
    response = ssock.recv(2048)


# Close the TLS Connection
ssock.shutdown(socket.SHUT_RDWR)
ssock.close()