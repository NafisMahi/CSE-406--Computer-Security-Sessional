# CSE-406--Computer-Security-Sessional

# CSE406 - Computer Security

## Offline 1 (AES Encryption-Decryption with Diffie-Hellman Key Exchange) [Offline1][#https://github.com/NafisMahi/CSE-406--Computer-Security-Sessional/tree/main/Offline_1]

### Setup
Navigate to the `solutions` folder and run the following commands:


### Part 1 - Independent Implementation of AES
Run `testAES.py` to see the results.

### Part 2 - Independent Implementation of Diffie-Hellman Key Exchange
Run `testDH.py` to see the results.

### Part 3 - Implementation of AES cryptosystem with TCP socket programming
Run `server.py` and `client.py` to see the results.

### Bonus Tasks
- **RSA Key Exchange**: RSA is used to exchange the AES key between the client and the server. The keys are generated on the client side. The client and passes the public key to the server. The server then uses the public key to encrypt p, g, A and send those to the client. Again, the opposite is done while sending B from client to server. Run `testRSA.py` to see the results.
- **RSA Authentication**: While sending data from one to the other, there is no way for the receiver to know if the sender is actually the one whose data the receiver is expecting. RSA can be used to authenticate the sender. The sender can sign the data with its private key and the receiver can verify the signature with the sender's public key. Details can be found here in the [Signing Messages section](#).

## Offline 2 (Malware)
- [Problem Specification](#)
- [Solution](#)
- [Report](#)

## Online 2 (Firewall)
- [Problem Specification](#)
- [Solution](#)
