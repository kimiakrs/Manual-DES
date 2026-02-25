#Kimia Sadat Karbasi-SID60393958
#Start with 64-bit key
#Pc-1 Permutation
#Split into 28 bits , 28 bits
#16 rounds of left shifts
#Pc-2 Permutation 

#Convert plaintext to binary
#Apply initial permutation 
#Divide it into 2 L and R 
#Using 16 rounds of Feistel function (F-function)
#Expansion: The right half (R) is expanded from 32 bits to 48 bits using an Expansion Permutation (E-table).
#XOR with Key: The expanded R is XORed with a subkey derived from the original key. This results in a new 48-bit value.
#SBox (substitution): This 48-bit value is then passed through 8 S-boxes, each of which reduces the value back to 32 bits.
#Permutation (P-table)==> permuted output Xor with L ==> new R
#Swap L and R
#Final Permutation

#Output Cihpertext(Hex)
#Output Keytext (Hex)

import random

# Initial Permutation Table (IP)
IP = [
    58, 50, 42, 34, 26, 18, 10, 2,
    60, 52, 44, 36, 28, 20, 12, 4,
    62, 54, 46, 38, 30, 22, 14, 6,
    64, 56, 48, 40, 32, 24, 16, 8,
    57, 49, 41, 33, 25, 17, 9, 1,
    59, 51, 43, 35, 27, 19, 11, 3,
    61, 53, 45, 37, 29, 21, 13, 5,
    63, 55, 47, 39, 31, 23, 15, 7
]

# Final Permutation Table (FP)
FP = [
    40, 8, 48, 16, 56, 24, 64, 32,
    39, 7, 47, 15, 55, 23, 63, 31,
    38, 6, 46, 14, 54, 22, 62, 30,
    37, 5, 45, 13, 53, 21, 61, 29,
    36, 4, 44, 12, 52, 20, 60, 28,
    35, 3, 43, 11, 51, 19, 59, 27,
    34, 2, 42, 10, 50, 18, 58, 26,
    33, 1, 41, 9, 49, 17, 57, 25
]

# Expansion Table (E)
E = [
    32, 1, 2, 3, 4, 5, 4, 5,
    6, 7, 8, 9, 8, 9, 10, 11,
    12, 13, 12, 13, 14, 15, 16, 17,
    16, 17, 18, 19, 20, 21, 20, 21,
    22, 23, 24, 25, 24, 25, 26, 27,
    28, 29, 28, 29, 30, 31, 32, 1
]

# P Permutation Table
P = [
    16, 7, 20, 21, 29, 12, 28, 17,
    1, 15, 23, 26, 5, 18, 31, 10,
    2, 8, 24, 14, 32, 27, 3, 9,
    19, 13, 30, 6, 22, 11, 4, 25
]

# PC-1 for Key Scheduling
PC1 = [
    57, 49, 41, 33, 25, 17, 9,
    1, 58, 50, 42, 34, 26, 18,
    10, 2, 59, 51, 43, 35, 27,
    19, 11, 3, 60, 52, 44, 36,
    63, 55, 47, 39, 31, 23, 15,
    7, 62, 54, 46, 38, 30, 22,
    14, 6, 61, 53, 45, 37, 29,
    21, 13, 5, 28, 20, 12, 4
]

# PC-2 for Key Scheduling
PC2 = [
    14, 17, 11, 24, 1, 5, 3, 28,
    15, 6, 21, 10, 23, 19, 12, 4,
    26, 8, 16, 7, 27, 20, 13, 2,
    41, 52, 31, 37, 47, 55, 30, 40,
    51, 45, 33, 48, 44, 49, 39, 56,
    34, 53, 46, 42, 50, 36, 29, 32
]

# Standard Shift table for left shifting
SHIFTS = [1, 1, 2, 2, 2, 2, 2, 2,
          1, 2, 2, 2, 2, 2, 2, 1]

# All 8 DES S-boxes
S_BOXES = [
    [[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
     [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
     [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
     [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]],
    [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
     [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
     [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
     [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]],
    [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
     [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
     [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
     [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]],
    [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
     [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
     [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
     [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]],
    [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
     [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
     [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
     [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]],
    [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
     [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
     [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
     [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]],
    [[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
     [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
     [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
     [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]],
    [[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
     [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
     [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
     [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]]
]

#Convert text to binary using UTF-8 (supports Unicode).
def binary_converter(text):
    #Using List
    binary = []
    for char in text:
        # Encode as UTF-8 (1-4 bytes per char)
        for byte in char.encode('utf-8'):
            #Encode your Charachter to 8bits
            binary.append(f"{byte:08b}")
    #Conctenated all the strings in binary
    return ''.join(binary)  # Continuous binary string

def generate_key_64bit():
    return ''.join(str(random.randint(0, 1)) for _ in range(64))

def left_shift(bits, n):
    return bits[n:] + bits[:n]

def generate_subkeys(key64):
    key56 = permute(key64, PC1)
    C, D = key56[:28], key56[28:]
    subkeys = []
    for shift in SHIFTS:
        C, D = left_shift(C, shift), left_shift(D, shift)
        subkey = permute(C + D, PC2)
        subkeys.append(subkey)
    return subkeys

def permute(bits, table):
    return ''.join(bits[i - 1] for i in table)

def split_bits(bits):
    #Spliting 64 bits into 2 parts (32 bits / 32bits)
    return bits[:32], bits[32:]
#Using XOR
"""0 ^ 0 = 0

0 ^ 1 = 1

1 ^ 0 = 1

1 ^ 1 = 0 """
def xor(a, b):
    return ''.join(str(int(x) ^ int(y)) for x, y in zip(a, b))


def expand_right_half(R):
    return ''.join(R[i - 1] for i in E)

#Using s_box_substitution  it takes a 48 bits binary string and splits it into eight 6-bits chunks
def s_box_substitution(bits):
    #Action: Splits the 48-bit input into 8 chunks of 6 bits each (since 48/6 = 8).
    chunks = [bits[i:i + 6] for i in range(0, 48, 6)]
    output = ''
    #i is the chunk index (0 to 7), selecting one of the 8 predefined S-Boxes.

    #row and col index into the S-Box to fetch a 4-bit number.
    for i, chunk in enumerate(chunks):
        row = int(chunk[0] + chunk[5], 2)
        col = int(chunk[1:5], 2)
        output += format(S_BOXES[i][row][col], '04b')
    return output

def feistel_round(L, R, subkey):
    R_expanded = expand_right_half(R)
    xor_result = xor(R_expanded, subkey)
    sbox_result = s_box_substitution(xor_result)
    p_result = permute(sbox_result, P)
    return R, xor(L, p_result)  # Swap L and R

def encryption_block(block, subkeys):
    permuted = permute(block, IP)
    L, R = split_bits(permuted)
    for key in subkeys:
        L, R = feistel_round(L, R, key)
    combined = R + L  # Swap after last round
    return permute(combined, FP)

def encrypt_des(plaintext, subkeys):
    #Convert text to binary
    binary_data = binary_converter(plaintext)
    cipher_blocks = []
    for i in range(0, len(binary_data), 64):
        block = binary_data[i:i+64]
        cipher_blocks.append(encryption_block(block, subkeys))
    cipher_bin = ''.join(cipher_blocks)
        #Convert to Hex:
        # Converts the decimal number to a hexadecimal string
        # it means we add 2 for binary and then slice off 0x from the hex string to just corret charachter
    hex_cipher = hex(int(cipher_bin, 2))[2:].upper()
    return hex_cipher

def main():
    #Encryption
    with open("/opt/DES/Task3/plain.txt", "r", encoding ='utf-8') as f:
        plaintext = f.read().strip()

    key64 = generate_key_64bit()
    subkeys = generate_subkeys(key64)
    cipher_hex = encrypt_des(plaintext, subkeys)
    key_hex = hex(int(key64, 2))[2:].upper()
    #Save Key text here:
    with open("/opt/DES/Task3/key.txt", "w") as f:
        f.write(key_hex)
    #Save encrypted text here
    with open("/opt/DES/Task3/cipher.txt", "w") as f:
        f.write(cipher_hex)
    print("Original Text:", plaintext)
    print("64-bit Key:", key_hex)
    print("Encrypted Cipher (HEX):", cipher_hex)

if __name__ == "__main__":
    print("This is Task3-enc.py")
    print("Kimia Sadat Karbasi - Student ID Number ='60393958'")
    main()



