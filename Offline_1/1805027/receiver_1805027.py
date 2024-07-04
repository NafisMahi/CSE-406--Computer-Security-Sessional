#To demonstrate Sender and Receiver, use TCP Socket Programming. To make things easy, please refresh your brain using this guide. Suppose, ALICE is the sender and BOB is the receiver. They will first agree on a shared secret key. For this, ALICE will send p, g and ga (mod p) to BOB. BOB, after receiving these, will send gb (mod p) to ALICE. Both will then compute the shared secret key, store it and inform each other that they are ready for transmission. Now, ALICE will send the AES encrypted ciphertext (CT) to BOB using the sockets. BOB should be able to decrypt it using the shared secret key. 
#start code here
import socket
import diffieHellman_1805027
import aes_1805027

b=diffieHellman_1805027.largePrime(64)

# Establish connection with Alice
bob_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
bob_socket.bind(('localhost', 8000))
bob_socket.listen(1)
print("Waiting for Alice to connect...")

alice_socket, address = bob_socket.accept()

print("Established connection with Alice")

# Receive p, g, and ga (mod p) from Alice
p = int(alice_socket.recv(1024).decode())
alice_socket.send("i received p".encode())
print("Received p from Alice")

g = int(alice_socket.recv(1024).decode())
alice_socket.send("i received g".encode())
print("Received g from Alice")

A = int(alice_socket.recv(1024).decode())
alice_socket.send("i received A".encode())
print("Received A from Alice")

B = diffieHellman_1805027.modularExponentiation(g,b,p)
alice_socket.sendall(str(B).encode())

# Calculate the shared secret key
shared_secret_key = diffieHellman_1805027.modularExponentiation(A,b,p)
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

while True:
    print("Waiting for message from Alice...")
    hexCipher = alice_socket.recv(1024).decode()
    cipher = aes_1805027.convertHexstringToMatrix(hexCipher)
    roundKeys = aes_1805027.getRoundKeys(aes_1805027.ConvertToHex(shared_secret_key),rounds=rounds)

    decyrpted,hexDecrypted,asciiDecrypted = aes_1805027.decryptAllBlocks(cipher,shared_secret_key,roundKeys,rounds=rounds)
    print("Decrypted message: ",asciiDecrypted)





