def send_req(host: str, port: int, req: bytes) -> bytes:
    print("📌 Sending Request:")
    print(req.decode("latin1", errors="ignore"))  # Print the full request
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    sock.send(req)

    response = sock.recv(1024)
    sock.close()
    
    return response

