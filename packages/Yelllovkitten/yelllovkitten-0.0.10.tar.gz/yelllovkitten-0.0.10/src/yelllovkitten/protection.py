def encode(text: str, password: int = 66):
    __alphabet = 'abcdefghijklmnopqrstuvwxyzабвгдеёжзийклмнопрстуфхцчшщъыьэюя1234567890!@#$%^&*() -+=_№\';:?[]{}\\/<>,.\'~`'
    new_password = None
    i = 0
    lenpass = len(text)
    while True:
        while True:
            if password > 100000 / len(__alphabet) - 100000 % len(__alphabet):
                password = password - 100000 / len(__alphabet) - 100000 % len(__alphabet)
            else:
                break
        passpassword = str((__alphabet.index(text[i]) + 1) * password)
        while True:
            if len(str(passpassword)) < 5:
               passpassword = str(0) + str(passpassword)
            else:
                if new_password == None:
                    new_password = passpassword
                else:
                    new_password = str(new_password) + passpassword
                break
        if lenpass * 5 == len(new_password):
            return str(new_password + '00000')
        if new_password == None:
            new_password = str((__alphabet.index(text[0]) + 1) * password)
            i = 1
            continue
        i = i + 1


def decode(text: int|str,password: int = 66):
    __alphabet = 'abcdefghijklmnopqrstuvwxyzабвгдеёжзийклмнопрстуфхцчшщъыьэюя1234567890!@#$%^&*() -+=_№\';:?[]{}\\/<>,.\'~`'
    text = str(text)
    answer = None
    while True:
        decoding = text[:5]
        text = text[5:]
        if decoding == '00000':
            return answer
        while True:
            if decoding[0] == '0':
                decoding = decoding[1:]
            else:
                decoding = int(decoding) / password
                break
        decoding = int(decoding)
        if answer == None:
            answer = str(__alphabet[decoding-1])
        else:
            answer = str(answer) + str(__alphabet[decoding-1])


#def full_encryption(text:str):
#    __alphabet = 'abcdefghijklmnopqrstuvwxyzабвгдеёжзийклмнопрстуфхцчшщъыьэюя1234567890!@#$%^&*() -+=_№\';:?[]{}\\/<>,.\'~`'
#    indexing = 666
#    while True:
#        last_letter = text[-1]
#        index_last_letter = __alphabet.index(last_letter)
#        index_last_letter = index_last_letter * indexing
