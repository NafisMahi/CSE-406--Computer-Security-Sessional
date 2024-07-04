import math
import os
import time
from BitVector import BitVector
#import bitVector
import bitVect
import sys

roundConstants = [0x01,0x02,0x04,0x08,0x10,0x20,0x40,0x80,0x1b,0x36,0x6C,0xD8,0xAB,0x4D]
state_matrix = [[0x54,0x4f,0x4e,0x20],[0x77,0x6e,0x69,0x54],[0x6f,0x65,0x6e,0x77],[0x20,0x20,0x65,0x6f]]
key_matrix = [[0x54,0x73,0x20,0x67],[0x68,0x20,0x4b,0x20],[0x61,0x6d,0x75,0x46],[0x74,0x79,0x6e,0x75]]
mix_column = [[0x02,0x03,0x01,0x01],[0x01,0x02,0x03,0x01],[0x01,0x01,0x02,0x03],[0x03,0x01,0x01,0x02]]
invMix_column = [[0x0e,0x0b,0x0d,0x09],[0x09,0x0e,0x0b,0x0d],[0x0d,0x09,0x0e,0x0b],[0x0b,0x0d,0x09,0x0e]]

def needPadding(plaintext):
    if len(plaintext) % 16 != 0:
        return True
    else:
        return False

def needTrimming(key):
    if len(key) > 16:
        return True
    else:
        return False
    
def trimKey(key):
    if needTrimming(key):
        key = key[:16]
    return key

def padKey(key):
    key = trimKey(key)
    if len(key) < 16:
        for i in range(0,16-len(key)):
            key = key + " "
    return key

def paddingLength(plaintext): 
    return 16 - (len(plaintext) % 16)

def padPlaintext(plaintext):
    if needPadding(plaintext):
        padLength = paddingLength(plaintext)
        for i in range(0,padLength):
            plaintext = plaintext + " "
    return plaintext

#write a code for breaking down a string into multiple lists of 16 characters each
def breakDownPlaintext(plaintext):
    plaintext = padPlaintext(plaintext)
    plaintextList = []
    for i in range(0,len(plaintext),16):
        plaintextList.append(plaintext[i:i+16])
    return plaintextList

def ConvertToHex(plaintext):
    hexText = [[0 for j in range(4)] for i in range(4)]
    index  = 0
    for i in range(0,4):
        for j in range(0,4):
            hexText[i][j] = hex(ord(plaintext[index]))[2:]
            index = index + 1
    return hexText

def ConvertHexToDec(hexText):
    decText = [[0 for j in range(4)] for i in range(4)]
    for i in range(0,4):
        for j in range(0,4):
            decText[i][j] = int(hexText[i][j],16)
    return decText

def getStateMatrix(plaintext):
    return ConvertHexToDec(swaprowsAndColumns(ConvertToHex(plaintext)))

def getNextRoundKey(prevRoundKey,roundConstant):
    w = [0 for j in range(4)] 
    #circular byte left shift
    firstByte = []
    firstByte = prevRoundKey[3][0]
    for i in range(0,len(prevRoundKey) - 1):
        w[i] = prevRoundKey[3][i+1]
    w[3]=firstByte

    #substitute bytes
    for i in range(0,len(w)):
        value = BitVector(hexstring=w[i])
        int_val=value.intValue()
        int_val = value.intValue()
        s = bitVect.Sbox[int_val]
        w[i] = s

    #add Round constant
    for i in range (0,len(w)):
        value = BitVector(intVal=w[i])
        constant = hex(roundConstant)[2:]
        if i == 0:
             result = value ^ BitVector(hexstring=constant)
             
        elif i > 0:
             result = value ^ BitVector(hexstring="00")
        padding_length = 8 - len(result)
        padded_bit_vector = BitVector(size=padding_length) + result
        w[i] = padded_bit_vector.get_bitvector_in_hex()

    nextRoundKey = [[0 for j in range(4)] for i in range(4)]
    for i in range(0,len(nextRoundKey)):
        for j in range(0,len(nextRoundKey[i])):
            val1 = int(w[j],16)
            val2 = int(prevRoundKey[i][j],16)
            result = val1 ^ val2
            nextRoundKey[i][j] = hex(result)[2:]
      
        w = nextRoundKey[i]
        for k in range(0,len(w)):
            w[k] = str(w[k])
    return nextRoundKey

    
def getRoundKeys(key,rounds):
    roundKeys = []
    roundKeys.append(key)
    for i in range(0,rounds):
        roundKeys.append(getNextRoundKey(roundKeys[i],roundConstants[i]))
        #print("Round Key : \n", roundKeys[i])
    return roundKeys

def getDecimalRoundKey(roundKeys,round):
    desiredKey = roundKeys[round]
    desiredKey = swaprowsAndColumns(desiredKey)
    for i in range(0,len(desiredKey)):
        for j in range(0,len(desiredKey[i])):
            desiredKey[i][j] = int(desiredKey[i][j],16)
    return desiredKey


def addRoundKey(state,roundKey):
    result = [[0 for j in range(4)] for i in range(4)]
    for i in range(0,4):
        for j in range(0,4):
            state[i][j] = hex(state[i][j])[2:]
            roundKey[i][j] = hex(roundKey[i][j])[2:]
            result[i][j] = hex(int(state[i][j],16) ^ int(roundKey[i][j],16))[2:]
    return result

def substituteBytes(state):
    for i in range(0,len(state)):
        for j in range(0,len(state[i])):
            value = BitVector(hexstring=state[i][j])
            int_val = value.intValue()
            s = bitVect.Sbox[int_val]
            state[i][j] = s
            state[i][j] = hex(state[i][j])[2:]
    return state

def cylicalLeftShift(state):
    temp = state[0]
    for i in range(0,len(state)-1):
        state[i] = state[i+1]
    state[len(state)-1] = temp

def cyclicalRightShift(state):
    temp = state[len(state)-1]
    for i in range(len(state)-1,0,-1):
        state[i] = state[i-1]
    state[0] = temp

def shiftRows(state):
    offset = 0
    for i in range(0,len(state)):
        for j in range(0,offset):
            cylicalLeftShift(state[i])
        offset = offset + 1
    return state
    
def galoisMultiplication(a,b):
    a = hex(a)[2:]
    bv1 = BitVector(hexstring=a)
    bv2 = BitVector(hexstring=b)
    bv3 = bv1.gf_multiply_modular(bv2, bitVect.AES_modulus, 8)
    return bv3

def swaprowsAndColumns(state):
    result = [[0 for j in range(4)] for i in range(4)]
    for i in range(0,len(state)):
        for j in range(0,len(state)):
            result[i][j] = state[j][i]
    return result
    
def mixColumns(state):
    result = [["0x00" for j in range(4)] for i in range(4)]
    for i in range(0,len(state)):
        for j in range(0,len(state)):
            result[i][j] = BitVector(hexstring="00")
            for k in range(0,len(state)):
                result[i][j] = result[i][j] ^ galoisMultiplication(mix_column[i][k],state[k][j])
            result[i][j] = result[i][j].get_bitvector_in_hex();
            result[i][j] = int(result[i][j],16)
    return result

def encrypt(plaintext,key,roundKeys,rounds):
    state_matrix = getStateMatrix(plaintext)
    #roundKeys = getRoundKeys(ConvertToHex(key))
    #print(roundKeys)
    key_matrix = getDecimalRoundKey(roundKeys,0)
    state_matrix = addRoundKey(state_matrix,key_matrix)
    for i in range(0,rounds-1):
        state_matrix = substituteBytes(state_matrix)
        state_matrix = shiftRows(state_matrix)
        state_matrix = mixColumns(state_matrix)
        state_matrix = addRoundKey(state_matrix,getDecimalRoundKey(roundKeys,i+1))
    state_matrix = substituteBytes(state_matrix)
    state_matrix = shiftRows(state_matrix)
    for i in range(0,len(state_matrix)):
        for j in range(0,len(state_matrix[i])):
            state_matrix[i][j] = int(state_matrix[i][j],16)
    state_matrix = addRoundKey(state_matrix,getDecimalRoundKey(roundKeys,10))
    return state_matrix

def encryptAllBlocks(plaintext,key,roundKeys,rounds):
    cipher = []
    cipher_text = ""
    plaintextList = []

    plaintextList = breakDownPlaintext(plaintext)
    for i in range(0,len(plaintextList)):
        cipher.append(encrypt(plaintextList[i],key,roundKeys,rounds))
        cipher_text = cipher_text + convertHexMatrixToString(swaprowsAndColumns(cipher[i]))

    hexCipher = cipher_text
    cipher_text = BitVector(hexstring=cipher_text)
    length = 8 * int(math.ceil(len(cipher_text)/8)) - len(cipher_text)
    padded_bit_vector = BitVector(size=length) + cipher_text
    cipher_text = padded_bit_vector
    
    #print("length of hexcipher" + str(len(hexCipher)))
    #print("Cipher Text : \n")
    #print("In ASCII : "+cipher_text.get_bitvector_in_ascii())
    #print("In Hex : "+hexCipher)

    return cipher,hexCipher,cipher_text.get_bitvector_in_ascii()


def convertToAsciiEncoding(state):
    cipher_text = ""
    for i in range(0,len(state)):
        for j in range(0,len(state[i])):
            #print("hello")
            cipher_text = cipher_text + state[i][j]  
    cipher_text = BitVector(hexstring=cipher_text)
    length = 8 * int(math.ceil(len(cipher_text)/8)) - len(cipher_text)
    padded_bit_vector = BitVector(size=length) + cipher_text
    cipher_text = padded_bit_vector
    #print(cipher_text)
    return cipher_text.get_bitvector_in_ascii()

def convertHexMatrixToString(state):
    cipher_text = ""
    for i in range(0,len(state)):
        for j in range(0,len(state[i])):
            cipher_text = cipher_text + state[i][j].zfill(2)
    #print("length")
    #print(len(cipher_text))
    #print(cipher_text)
    #convertHexstringToMatrix(cipher_text)
    return cipher_text

def convertHexstringToMatrix(state):
    list = []
    result = [["0x00" for j in range(4)] for i in range(4)]
    k = 0
   # print("length "+str(len(state)))
    while k < len(state):
        for i in range(0,4):
            for j in range(0,4):
                result[i][j] = state[k] + state[k+1]
                k = k + 2
                #print("k "+str(k))
        list.append(swaprowsAndColumns(result))
    return list

def inverseshiftRows(state):
    offset = 0
    for i in range(0,len(state)):
        for j in range(0,offset):
            cyclicalRightShift(state[i])
        offset = offset + 1
    return state

def inverseSubstituteBytes(state):
    for i in range(0,len(state)):
        for j in range(0,len(state[i])):
            value = BitVector(hexstring=state[i][j])
            int_val = value.intValue()
            s = bitVect.InvSbox[int_val]
            state[i][j] = s
            state[i][j] = hex(state[i][j])[2:]
    return state

def inverseMixColumns(state):
    result = [["0x00" for j in range(4)] for i in range(4)]
    for i in range(0,len(state)):
        for j in range(0,len(state)):
            result[i][j] = BitVector(hexstring="00")
            for k in range(0,len(state)):
                result[i][j] = result[i][j] ^ galoisMultiplication(invMix_column[i][k],state[k][j])
            result[i][j] = result[i][j].get_bitvector_in_hex()
    return result


def decrypt(cipher_text,key,roundKeys,rounds):
    state_matrix = ConvertHexToDec(cipher_text)
    #roundKeys = getRoundKeys(ConvertToHex(key))
    key_matrix = getDecimalRoundKey(roundKeys,10)
    state_matrix = addRoundKey(state_matrix,key_matrix)
    for i in range(0,rounds-1):
        state_matrix = inverseshiftRows(state_matrix)
        state_matrix = inverseSubstituteBytes(state_matrix)
        for j in range (0,len(state_matrix)):
            for k in range(0,len(state_matrix[j])):
                state_matrix[j][k] = int(state_matrix[j][k],16) 
        state_matrix = addRoundKey(state_matrix,getDecimalRoundKey(roundKeys,9-i))
        state_matrix = inverseMixColumns(state_matrix)
    state_matrix = inverseshiftRows(state_matrix)
    state_matrix = inverseSubstituteBytes(state_matrix)
    for j in range (0,len(state_matrix)):
            for k in range(0,len(state_matrix[j])):
                state_matrix[j][k] = int(state_matrix[j][k],16)
    state_matrix = addRoundKey(state_matrix,getDecimalRoundKey(roundKeys,0))
    return state_matrix

def decryptAllBlocks(cipher,key,roundKeys,rounds):
    decrypted = []
    decrypted_text = ""

    for i in range(0,len(cipher)):
        decrypted.append(decrypt(cipher[i],key,roundKeys,rounds))
        decrypted_text = decrypted_text + convertHexMatrixToString(swaprowsAndColumns(decrypted[i]))
    
    hexDecrypted = decrypted_text
    decrypted_text= BitVector(hexstring=decrypted_text)
    length = 8 * int(math.ceil(len(decrypted_text)/8)) - len(decrypted_text)
    padded_bit_vector = BitVector(size=length) + decrypted_text
    decrypted_text = padded_bit_vector

    #print("Deciphered Text : \n")
    #print("In ASCII : "+decrypted_text.get_bitvector_in_ascii())
    #print("In Hex : "+hexDecrypted)

    return decrypted,hexDecrypted,decrypted_text.get_bitvector_in_ascii()

def readFileasBinary(filename):
    path = os.path.abspath(filename)
    _, extension = os.path.splitext(filename)
    with open(path,"rb") as f:
        text = f.read()
    return text,extension

def writeFileasBinary(text,extension):
    with open("decrypted" + extension,"wb") as f:
        f.write(text)

def take_input():
    print("DO YOU WANT TO ENCRYPT OTHER TYPES OF FILES? (Y/N)")
    choice = input()
    flag = 0
    extension = ""
    if choice == 'Y' or choice == 'y':
        print("enter the path of the file to be encrypted")
        path = input()
        plaintext,extension = readFileasBinary(path)
        plaintext = plaintext.decode('utf-8')
        flag = 1
    else:
        plaintext = input("Enter the plaintext: \n")
    key = input("Enter the key: \n")
    print("\n")
    plaintext = padPlaintext(plaintext)
    if len(key) == 16:
        rounds = 10
    elif len(key) == 20:
        rounds = 12
    elif len(key) == 24:
        rounds = 14
    else:
        key = padKey(key)
        rounds = 10
    output(plaintext,key,rounds,flag,extension)

def output(plaintext,key,rounds,flag,extension):
    print("Plain text:")
    print("In ASCII: "+plaintext)
    print("In Hex: "+convertHexMatrixToString(ConvertToHex(plaintext))+"\n")

    print("Key:")
    print("In ASCII: "+key)
    print("In Hex: "+convertHexMatrixToString(ConvertToHex(key))+"\n")

    start_generate_round_keys = time.perf_counter()
    roundKeys = getRoundKeys(ConvertToHex(key),rounds)
    end_generate_round_keys = time.perf_counter()
    time_taken_generate_round_keys = end_generate_round_keys - start_generate_round_keys

    start_encrypt = time.perf_counter()
    cipher,hexCipher,asciiCipher = encryptAllBlocks(plaintext,key,roundKeys=roundKeys,rounds=rounds)
    end_encrypt = time.perf_counter()
    time_taken_encrypt = end_encrypt - start_encrypt

    print("Cipher Text : ")
    print("In ASCII : "+asciiCipher)
    print("In Hex : "+hexCipher+"\n")

    start_decrypt = time.perf_counter()
    decrypted,hexDecrypted,asciiDecrypted = decryptAllBlocks(cipher,key,roundKeys=roundKeys,rounds=rounds)
    end_decrypt = time.perf_counter()
    time_taken_decrypt = end_decrypt - start_decrypt

    print("Deciphered Text : ")
    print("In ASCII : "+asciiDecrypted)
    print("In Hex : "+hexDecrypted)

    if flag == 1:
        writeFileasBinary(asciiDecrypted.encode('utf-8'),extension)

    print("Execution time details:\n")
    print("Key Schedule: "+str(time_taken_generate_round_keys)+" seconds\n")
    print("Encryption: "+str(time_taken_encrypt)+" seconds\n")
    print("Decryption: "+str(time_taken_decrypt)+" seconds\n")
