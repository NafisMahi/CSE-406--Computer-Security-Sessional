import math
import random
import secrets

def isPrime(n, k=40):
    if n == 2 or n == 3:
        return True
    if n <= 1 or n%2 == 0:
        return False
    
    t = 0
    f = n-1
    while f%2 == 0:
        t = t + 1
        f //= 2
    
    for i in range(k):
        ran = random.randrange(2,n-1)
        x = pow(ran,f,n)
        if x == 1 or x == n-1:
            continue
        
        for r in range(t-1):
            x = pow(x,2,n)
            if x == n-1:
                break
        else:
            return False
    return True

def generate_random_bits(n):
    num_bytes = (n + 7) // 8  # Calculate the number of bytes needed
    random_bytes = secrets.token_bytes(num_bytes)  # Generate random bytes
    random_bits = int.from_bytes(random_bytes, 'big')  # Convert bytes to integer
    random_bits &= (1 << n) - 1  # Mask out any extra bits
    return random_bits

def largePrime(k):
    while True:
        p = generate_random_bits(k)
        if isPrime(p) and isPrime(int((p-1)//2)):
            return p
        
def twoLargePrimes(k):
    p = largePrime(k)
    q = largePrime(k)
    while p == q:
        q = largePrime(k)
    return p,q

def convertToBinary(n):
    return bin(n)[2:]

def modularExponentiation(g,a,p):
    binary = convertToBinary(a)
    result = 1
    for i in range(len(binary)-1,-1,-1):
        if binary[i] == '1':
            result = (result*g)%p
        g = (g*g)%p
    return result

def gcd(a,b):
    if a == 0:
        return b
    return gcd(b%a,a)

def product(p,q):
    return p*q

def lcm(p,q):
    return (p*q)//gcd(p,q)

def select_e(lambda_value):
    while True:
        e = random.randint(2, lambda_value - 1)  # Generate a random value for e
        if math.gcd(e, lambda_value) == 1:  # Check if e and lambda_value are relatively prime
            return e
        
def select_d(e,lambda_value):
    d = pow(e, -1, lambda_value)  # Compute the modular inverse of e
    return d

def generate_keys(k):
    p,q = twoLargePrimes(k)
    n = product(p,q)
    lambda_value = lcm(p-1,q-1)
    e = select_e(lambda_value)
    d = select_d(e,lambda_value)
    return (e,n),(d,n)

def encrypt(publicKey,text):
    e , n = publicKey
    ciphers = []
    for ch in text:
        ciphers.append(modularExponentiation(ord(ch),e,n))
    return ciphers

def decrypt(privateKey,ciphers):
    d , n = privateKey
    text = ""
    for ch in ciphers:
        text += chr(modularExponentiation(ch,d,n))
    return text

def RSAEncrypt(publicKey,text):
    ciphers = encrypt(publicKey,text)
    return ciphers

def RSADecrypt(privateKey,ciphers):
    plaintext = decrypt(privateKey,ciphers)
    return plaintext

def main():
    print("Enter the message to be encrypted: ")
    text = input()
    publicKey,privateKey = generate_keys(64)
    ciphers = RSAEncrypt(publicKey,text)
    print("Encrypted message: ",ciphers)
    plaintext = RSADecrypt(privateKey,ciphers)
    print("Decrypted message: ",plaintext)

main()