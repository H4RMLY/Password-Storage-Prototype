from textwrap import wrap

hex_sbox = {
    '0': '4',
    '1': 'e',
    '2': 'a',
    '3': '5',
    '4': 'c',
    '5': '2',
    '6': '7',
    '7': 'f',
    '8': 'b',
    '9': '8',
    'a': '0',
    'b': '6',
    'c': '3',
    'd': '9',
    'e': 'd',
    'f': '1'
}

def repeatKeyToLength(key, plaintextLen):
    return (key * (plaintextLen//len(key) + 1))[:plaintextLen]

def binaryToHex(binary):
    convertedHex = []
    for i in range(len(binary)):
        convertedHex.append(hex(int(binary[i], 2))[2:])
    return ''.join(convertedHex)

def hexToBinary(hex):
    """
    Converts a given hexadecimal string to binary.

    Parameters:
    hex (str): The hexadecimal string to be converted.

    Returns:
    str: The binary representation of the input hexadecimal string.
    """
    binary = []
    for i in hex:
        binary.append(bin(int(i, 16))[2:].zfill(4))  # Convert each hexadecimal digit to binary and pad with zeros
    return binary

def hexToText(hex):
    text = ""
    for i in hex:
        text += chr(int(i, 16))
    return text

def textToHex(text):
    hexText = []
    for i in text:
        hexText.append(hex(ord(i))[2:])
    return ''.join(hexText)

def sboxEncrypt(inputText, sbox):
    outputText = []
    for i in inputText:
        outputText.append(sbox[i])
    return ''.join(outputText)

def sboxDecrypt(inputText, sbox):
    output = ""
    for i in inputText:
        # Creates a list of keys in the sbox and a list of their values and returns the key at the searched value index in the keys list
        output += list(sbox.keys())[list(sbox.values()).index(i)] 
    return output

def xorBinary(binary1, binary2):
    xorResult = ""
    for i in range(len(binary1)):
        if binary1[i] == binary2[i]:
            xorResult += '0'
        elif binary1[i]!= binary2[i]:
            xorResult += '1'
    return xorResult

def encrypt(plainText, key):
    """
    Encrypts a given plaintext using a simple XOR cipher and an S-Box.

    Parameters:
    plainText (str): The plaintext to be encrypted.
    key (str): The secret key used for encryption.

    Returns:
    str: The encrypted ciphertext.
    """
    key = repeatKeyToLength(key, len(plainText))
    hexText = textToHex(plainText)
    hexKey = textToHex(key)
    
    # Encrypts the hex plaintext with the s-box
    sboxText = sboxEncrypt(hexText, hex_sbox)
    
    # Convert encrypted hexadecimal to binary
    binaryText = [bin(int(i, 16))[2:].zfill(8) for i in sboxText]
    binaryKey = [bin(int(i, 16))[2:].zfill(8) for i in hexKey]
    
    # Perform XOR operation on binary representations of key and text
    xorResult = [xorBinary(binaryText[i], binaryKey[i]) for i in range(len(binaryText))]   
     
    # Convert binary back to hexadecimal
    xorHexResult = binaryToHex(xorResult)    
    return xorHexResult

def decrypt(encryptedText, key):
    """
    Decrypts a given encrypted text using a simple XOR cipher and an S-Box.

    Parameters:
    encryptedText (str): The encrypted text to be decrypted.
    key (str): The secret key used for decryption.

    Returns:
    str: The decrypted plaintext.
    """
    key = repeatKeyToLength(key, len(encryptedText))
    hexKey = textToHex(key)
    
    # Convert hexadecimal to binary
    binaryKey = [bin(int(i, 16))[2:].zfill(8) for i in hexKey]
    
    # Convert ciphertext to binary
    encryptedBinary = [bin(int(i, 16))[2:].zfill(8) for i in encryptedText]
    
    # Perform XOR operation on binary representations
    xorResult = [xorBinary(encryptedBinary[i], binaryKey[i]) for i in range(len(encryptedBinary))]
    
    # Convert binary back to hexadecimal
    xorHexResult = binaryToHex(xorResult)
    
    # Decrypt S-Box
    sboxText = sboxDecrypt(xorHexResult, hex_sbox)
    
    # Convert hex to text
    plainText = hexToText(wrap(sboxText,2))
    return plainText