import hashlib
import time

# Step 1: Load Target Hashes
def load_hashes(file_path):
    with open(file_path, 'r') as f:
        return [line.strip() for line in f]

# Step 2: Load Password Dictionary
def load_passwords(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        return [line.strip() for line in f]

# Step 3: Generate and Compare Hashes
def crack_hashes(passwords, target_hashes, hash_function):
    cracked_passwords = ['0']*len(target_hashes)
    dic={}
    for i in range(len(target_hashes)):
        dic[target_hashes[i]]=i
    for password in passwords:
        # Generate the hash
        hash_value = hash_function(password.encode()).hexdigest()
        # Check if it matches any target hash
        try:
            if dic[hash_value]>=0:
                cracked_passwords[dic[hash_value]] = (password, hash_value)
        except:
            pass
        
    for i in range(len(cracked_passwords)):
        if cracked_passwords[i] == '0':
            cracked_passwords[i] = ("Password not found", target_hashes[i])
            print(f"Password not found for hash: {target_hashes[i]}")
    return cracked_passwords

# Main Function
if __name__ == "__main__":
    # Files
    md5_file = "md5_hashes.txt"
    sha1_file = "sha1_hashes.txt"
    sha256_file = "sha256_hashes.txt"
    # password_file = "rockyou.txt"  # Replace with your dictionary file
    password_file="passwords.txt"

    # Load hashes
    print("Loading target hashes...")
    md5_hashes = load_hashes(md5_file)
    sha1_hashes = load_hashes(sha1_file)
    sha256_hashes = load_hashes(sha256_file)

    # Load passwords
    print("Loading password dictionary...")
    passwords = load_passwords(password_file)
 

    # Crack MD5 hashes
    print("Cracking MD5 hashes...")
    start_time = time.time()
    cracked_md5 = crack_hashes(passwords, md5_hashes, hashlib.md5)
    end_time = time.time()
    print(f"Total MD5 cracked passwords: {len(cracked_md5)} ")
    print(f"MD5 cracking completed in {end_time - start_time:.2f} seconds.")
    for password, hash_value in cracked_md5:
        print(f"Cracked: {password} -> {hash_value}")

    # Crack SHA1 hashes
    print("Cracking SHA1 hashes...")
    start_time = time.time()
    cracked_sha1 = crack_hashes(passwords, sha1_hashes, hashlib.sha1)
    end_time = time.time()
    print(f"SHA1 cracking completed in {end_time - start_time:.2f} seconds.")
    for password, hash_value in cracked_sha1:
        print(f"Cracked: {password} -> {hash_value}")

    # Crack SHA256 hashes
    print("Cracking SHA256 hashes...")
    start_time = time.time()
    cracked_sha256 = crack_hashes(passwords, sha256_hashes, hashlib.sha256)
    end_time = time.time()
    print(f"SHA256 cracking completed in {end_time - start_time:.2f} seconds.")
    for password, hash_value in cracked_sha256:
        print(f"Cracked: {password} -> {hash_value}")

    print("Cracking complete!")
