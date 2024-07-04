#To demonstrate Sender and Receiver, use TCP Socket Programming. To make things easy, please refresh your brain using this guide. Suppose, ALICE is the sender and BOB is the receiver. They will first agree on a shared secret key. For this, ALICE will send p, g and ga (mod p) to BOB. BOB, after receiving these, will send gb (mod p) to ALICE. Both will then compute the shared secret key, store it and inform each other that they are ready for transmission. Now, ALICE will send the AES encrypted ciphertext (CT) to BOB using the sockets. BOB should be able to decrypt it using the shared secret key. 
#start code here
import socket
import sys
#sys.path.append('/path/to/BitVector')
import diffieHellman_1805027
import aes_1805027

p = diffieHellman_1805027.largePrime(128) # Prime number
print("p: ",p)
g = diffieHellman_1805027.findPrimitiveRoot(p)  # Primitive root modulo
print("g: ",g)
a = diffieHellman_1805027.largePrime(64)   # Private key for Alice
print("a: ",a)

# Calculate ga (mod p)
A = diffieHellman_1805027.modularExponentiation(g,a,p)


# Establish connection with Bob
alice_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
alice_socket.connect(('localhost', 8000))

print("Established connection with Bob")

# Send p, g, and ga (mod p) to Bob
alice_socket.send(str(p).encode())
received_msg = alice_socket.recv(1024).decode()
print("Received acknowledgement of p from Bob")

alice_socket.send(str(g).encode())
received_msg = alice_socket.recv(1024).decode()
print("Received acknowledgement of g from Bob")

alice_socket.send(str(A).encode())
received_msg = alice_socket.recv(1024).decode()
print("Received acknowledgement of A from Bob")

# Receive gb (mod p) from Bob
B = int(alice_socket.recv(1024).decode())
print("Received B from Bob")

# Calculate the shared secret key
shared_secret_key = diffieHellman_1805027.modularExponentiation(B,a,p)
shared_secret_key = str(shared_secret_key)

if len(shared_secret_key) == 16:
    rounds = 10
elif len(shared_secret_key) == 20:
    rounds = 12
elif len(shared_secret_key) == 24:
    rounds = 14
else:
    shared_secret_key = aes_1805027.padKey(shared_secret_key)   # Pad the key to make it 128 bits
    rounds = 10
print("Computed the shared secret key")

#start a while loop and keep sending encrypted messages to bob
while True:
    # Encrypt the message using the shared secret key
    message = input("Enter message to send: ")
    message = aes_1805027.padPlaintext(message)
    
    #cipher = Fernet(str(shared_secret_key).encode())
    roundKeys = aes_1805027.getRoundKeys(aes_1805027.ConvertToHex(shared_secret_key),rounds=rounds)
    cipher,hexCipher,asciiCipher = aes_1805027.encryptAllBlocks(message,shared_secret_key,roundKeys,rounds=rounds)

    print("Encrypted message: ",asciiCipher)
    
    # Send the encrypted message to Bob
    alice_socket.sendall(hexCipher.encode())

