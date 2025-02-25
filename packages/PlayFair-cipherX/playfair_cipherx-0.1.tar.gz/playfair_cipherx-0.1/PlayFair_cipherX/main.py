def prepare_text(text):
    text = text.upper().replace('J', 'I')
    text = ''.join(filter(str.isalpha, text))
    if len(text) % 2 != 0:
        text += 'X'
    return text

def create_matrix(key):
    key = prepare_text(key)
    matrix = [['' for _ in range(5)] for _ in range(5)]
    alphabet = 'ABCDEFGHIKLMNOPQRSTUVWXYZ'
    key_set = set()

    k = 0
    for char in key:
        if char not in key_set:
            matrix[k // 5][k % 5] = char
            key_set.add(char)
            k += 1

    for char in alphabet:
        if char not in key_set:
            matrix[k // 5][k % 5] = char
            k += 1
    return matrix

def find_position(matrix, char):
  for i in range(5):
    for j in range(5):
      if matrix[i][j] == char:
        return i,j
  return -1,-1

def encrypt(plaintext, key):
    matrix = create_matrix(key)
    plaintext = prepare_text(plaintext)
    ciphertext = ''

    for i in range(0, len(plaintext), 2):
        a, b = plaintext[i], plaintext[i+1]
        row1, col1 = find_position(matrix, a)
        row2, col2 = find_position(matrix, b)

        if row1 == row2:
            ciphertext += matrix[row1][(col1 + 1) % 5]
            ciphertext += matrix[row2][(col2 + 1) % 5]
        elif col1 == col2:
            ciphertext += matrix[(row1 + 1) % 5][col1]
            ciphertext += matrix[(row2 + 1) % 5][col2]
        else:
            ciphertext += matrix[row1][col2]
            ciphertext += matrix[row2][col1]

    return ciphertext

def decrypt(ciphertext, key):
  matrix = create_matrix(key)
  plaintext = ''
  for i in range(0,len(ciphertext),2):
    a,b = ciphertext[i],ciphertext[i+1]
    row1, col1 = find_position(matrix, a)
    row2, col2 = find_position(matrix, b)
    if row1 == row2:
      plaintext += matrix[row1][(col1 - 1) % 5]
      plaintext += matrix[row2][(col2 - 1) % 5]
    elif col1 == col2:
      plaintext += matrix[(row1 - 1) % 5][col1]
      plaintext += matrix[(row2 - 1) % 5][col2]
    else:
      plaintext += matrix[row1][col2]
      plaintext += matrix[row2][col1]
  return plaintext