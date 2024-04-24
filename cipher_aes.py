from generate_keys import expand_keys

is_Key = False

while( not is_Key):
    print("Digite a chave de criptografia com base no modelo abaixo:")
    print("20,1,94,33,199,0,48,9,31,94,112,40,59,30,100,248")

    key = input()
    key = key.split(',')

    if(len(key) != 16):
        print("Chave de encriptação invalida, digite novamente")
    else:
        is_Key = True


print(expand_keys())