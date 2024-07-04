import random
import secrets
import time

from tabulate import tabulate

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
        
def findPrimitiveRoot(p):
    if p == 2:
        return 1
    for g in range(2,p):
        val1 = pow(g,2,p)
        val2 = pow(g,(p-1)//2,p)
        if not (val1 == 1) and not (val2 == 1):
            return g
 
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

def diffieHellman():
    start_p = time.perf_counter()
    p = largePrime(128)
    end_p = time.perf_counter()
    time_p = end_p - start_p

    start_g = time.perf_counter()
    g = findPrimitiveRoot(p)
    end_g = time.perf_counter()
    time_g = end_g - start_g

    start_a = time.perf_counter()
    a = largePrime(64)
    end_a = time.perf_counter()
    time_a = end_a - start_a

    
    b = largePrime(64)

    start_A = time.perf_counter()
    A = modularExponentiation(g,a,p)
    end_A = time.perf_counter()
    time_A = end_A - start_A

    B = modularExponentiation(g,b,p)

    start_s = time.perf_counter()
    s1 = modularExponentiation(B,a,p)
    end_s = time.perf_counter()
    time_s = end_s - start_s

    s2 = modularExponentiation(A,b,p)
    
    if s1 == s2:
        return True, time_p, time_g, time_a, time_A, time_s
    else:
        return False, time_p, time_g, time_a, time_A, time_s


def drawBeautifulTable():
    # Define the table headers
    headers = ["k", "p", "g", "a or b", "A or B", "shared key"]
    results = [diffieHellman() for i in range(3)]

    k_values = [128, 192, 256]
    p_values = [results[0][1], results[1][1], results[2][1]]  # Replace p1, p2, p3 with your actual values
    g_values = [results[0][2], results[1][2], results[2][2]]  # Replace g1, g2, g3 with your actual values
    a_values = [results[0][3], results[1][3], results[2][3]]  # Replace a1, a2, a3 with your actual values
    A_values = [results[0][4], results[1][4], results[2][4]]  # Replace A1, A2, A3 with your actual values
    shared_key_values = [results[0][5], results[1][5], results[2][5]]  # Replace s1, s2, s3 with your actual values

    data = list(zip(k_values, p_values, g_values, a_values, A_values, shared_key_values))

    table = tabulate(data, headers, tablefmt="fancy_grid")
    print(table)
