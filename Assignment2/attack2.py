import hashlib
import time

def load_passwords(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        return [line.strip() for line in f]
def load_salted_hashes(file_path):
    """
    Loads salted hashes from a file in the format salt:hash.
    Returns a list of (salt, hash) tuples.
    """
    salted_hashes = []
    try:
        with open(file_path, 'r') as f:
            for line in f:
                parts = line.strip().split(':')  # Split by colon
                if len(parts) == 2:  # Ensure valid format
                    salted_hashes.append((parts[0], parts[1]))
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
    return salted_hashes

# Step 2: Crack Salted Hashes
def crack_salted_hashes(passwords, salted_hashes, hash_function):
    """
    Attempts to crack salted hashes using a list of passwords.
    """
    cracked_passwords = ['0']*len(salted_hashes)
    i=0
    for salt, target_hash in salted_hashes:
        for password in passwords:
            # Combine the salt and password
            salted_password = password+salt  # Adjust combination if needed
            # Generate the hash
            hash_value = hash_function(salted_password.encode()).hexdigest()
            # Check if it matches the target hash
            if hash_value == target_hash:
                cracked_passwords[i]=((salt, password, target_hash))
                break  # Stop after finding the correct password
        i+=1
        
    return cracked_passwords

# Main Function
if __name__ == "__main__":
    # Files
    md5_file = "md5_salted_hashes.txt"
    sha1_file = "sha1_salted_hashes.txt"
    sha256_file = "sha256_salted_hashes.txt"
    password_file = "passwords.txt"  # Replace with your dictionary file

    # Load salted hashes
    print("Loading salted hashes...")
    md5_salted = load_salted_hashes(md5_file)
    sha1_salted = load_salted_hashes(sha1_file)
    sha256_salted = load_salted_hashes(sha256_file)

    # Load passwords
    print("Loading password dictionary...")
    passwords = load_passwords(password_file)

    # Crack MD5 salted hashes
    print("Cracking MD5 salted hashes...")
    start_time = time.time()
    cracked_md5 = crack_salted_hashes(passwords, md5_salted, hashlib.md5)
    end_time = time.time()
    print(f"MD5 salted cracking completed in {end_time - start_time:.2f} seconds.")
    print(len(cracked_md5))
    for salt, password, target_hash in cracked_md5:
        print(f"Cracked: Salt={salt}, Password={password}, Hash={target_hash}")

    # Crack SHA1 salted hashes
    print("Cracking SHA1 salted hashes...")
    start_time = time.time()
    cracked_sha1 = crack_salted_hashes(passwords, sha1_salted, hashlib.sha1)
    end_time = time.time()
    print(f"SHA1 salted cracking completed in {end_time - start_time:.2f} seconds.")
    for salt, password, target_hash in cracked_sha1:
        print(f"Cracked: Salt={salt}, Password={password}, Hash={target_hash}")

    # Crack SHA256 salted hashes
    print("Cracking SHA256 salted hashes...")
    start_time = time.time()
    cracked_sha256 = crack_salted_hashes(passwords, sha256_salted, hashlib.sha256)
    end_time = time.time()
    print('0' in cracked_sha256 or '0' in cracked_sha1 or '0' in cracked_md5)
    print(f"SHA256 salted cracking completed in {end_time - start_time:.2f} seconds.")
    for salt, password, target_hash in cracked_sha256:
        print(f"Cracked: Salt={salt}, Password={password}, Hash={target_hash}")

    print("Cracking complete!")
