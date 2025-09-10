import socket
import random
from math import ceil, sqrt

def crack_DHA(p, g, y, max_power=None, verify: bool = False):

    if max_power == None:
        max_power = p
    m = ceil(sqrt(max_power))

    baby_step = dict()
    # Compute all the baby steps
    g_j = 1
    for j in range(0, m):
        baby_step[g_j] = j
        g_j = (g_j * g) % p
    
    g_m = pow(g, p-(m+1), p)
    temp = y
    for i in range(0, m):

        if temp in baby_step:
            return (i * m) + baby_step[temp]
        
        temp = (temp * g_m) % p

    return -1

def dh_key_exchange(server_ip, server_port, entry_number):
    try:
        # Connect to the server
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            print("Connecting to server")
            s.connect((server_ip, server_port))
            print("Connected to the server.")

            # Send entry number
            s.sendall(entry_number.encode())
            print(f"Sent entry number: {entry_number}")

            # Receive P, G, and A
            data = s.recv(1024).decode()
            P, G = map(int, data.split(','))
            print(f"Received parameters: P={P}, G={G}")

            # Generate private key
            private_key = random.randint(1, P - 1)
            print(f"Generated private key: {private_key}")

            # Compute public key
            public_key = pow(G, private_key, P)
            print(f"Computed public key: {public_key}")

            # Send public key to server
            s.sendall(str(public_key).encode())
            print(f"Sent public key: {public_key}")

            # Receive confirmation or response from server
            A = s.recv(1024).decode()
            A=int(A)
            print(f"Received Secret key: {A}")
            shared_secret = pow(A, private_key, P)
            print(f"Computed shared secret: {shared_secret}")
            
            server_key = crack_DHA(P,G,A)
            print(f"Private key:{server_key}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    server_ip = "10.237.27.193"  # Replace with actual server IP
    server_port = 5555      # Replace with actual server port
    entry_number = "2021CS50593"  # Replace with your entry number
    dh_key_exchange(server_ip, server_port, entry_number)
