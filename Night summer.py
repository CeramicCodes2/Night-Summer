#Night summer
from cryptography.fernet import Fernet
from PIL import Image
from numpy import array
from os.path import join,isfile
from time import sleep
from colorama import Fore,Back,init
init()
def load(path):
    if not isfile(path) or not path.endswith('.png'):
        raise NameError('img not exists or the image file is not a png image')
    return array(Image.open(path))
def words_to_bytes(words='',encoder='ascii'): return ''.join([bin(x)[2:].zfill(8) for x in words.encode(encoder)])
def bits_to_words(bits): return ''.join([chr(int(x,2)) for x in bits])
def bits2list(bits): return [bits[x:x+8] for x in range(0,len(bits),8)]#convierte la cadena en bloques de 8
def number2bits(number): return [y for x in bin(number)[2:].zfill(8) for y in x]
def multy(msj,key,encoder='ascii',encrypt=False,decrypt=False):
    # if len(key) != 32: raise NameError('el largo de la llave debe de ser de 32 bits')
    kms = Fernet(key)
    if (encrypt and decrypt) or (not encrypt and not decrypt):
        raise NameError('solo puede estar activada o desactivada una bandera')
    if encrypt:
        return kms.encrypt(msj.encode(encoder))
    if decrypt:
        return kms.decrypt(msj)
def calculate_words(flat,msj_in_bits):
    if (len(msj_in_bits) - 1) > flat.shape[0] or (len(msj_in_bits) - 1) == flat.shape[0]:
        raise NameError('la imagen es muy peque;a para el mensaje')
def LSB(path,msj):
    img = load(path)
    flat = img.flatten()
    msj = words_to_bytes(msj + ' ~')# el espacio es por que el ultimo digito en el procedimiento no supera el numero 7, eso es raro y no se por que es
    calculate_words(flat,msj)
    for y,bits in enumerate(zip(flat,msj)):
        tmp = number2bits(bits[0])
        tmp.pop()
        tmp.append(bits[1])
        flat[y] = int(''.join(tmp),2)
    return flat.reshape(img.shape),str(len(msj) - 1)# ubicacion
def DLSB(path):
    if not path.endswith('.png') or not isfile(path):
        raise NameError('la imagen no existe o no tiene extension .png')
    img = load(path)
    flat = img.flatten()
    ''' TODO:old version
    shaper = int(lg)
    txt = ''
    for bit in zip(range(0,shaper + 1),flat):
        txt += number2bits(bit[1]).pop()
    '''
    ttq = ''
    for y,num in enumerate(flat):
        ttq += number2bits(num).pop()
        if y%8 == 0 and '~' in bits_to_words(bits2list(ttq)):
            wll = bits_to_words(bits2list(ttq))
            return wll[:wll.index('~')]
def crypto_LSB(path,msj,key,encoder='utf-8'):
    if not isfile(path) or not path.endswith('.png'):
        raise ValueError('la imagen insertada no tiene extension png o no existe')
    img = load(path)
    flat = img.flatten()
    key = Fernet(key.encode(encoder))
    msj = words_to_bytes(key.encrypt(msj.encode(encoder) + b' ').decode(encoder) + b'~ '.decode(encoder))
    for y,bit in enumerate(zip(flat,msj)):
        tmp = number2bits(bit[0])
        tmp.pop()
        tmp.append(bit[1])
        flat[y] = ''.join(tmp)
    return flat.reshape(img.shape)
def decrypt_LSB(path,key,encoder='utf-8'):
    img = load(path)
    flat = img.flatten()
    ttq = ''
    '''
    txt = ''
    for bit in zip(range(0,leght),flat):
        txt += number2bits(bit[1]).pop()
    '''
    key = Fernet(key.encode(encoder))
    for y,num in enumerate(flat):
        ttq += number2bits(num).pop()
        if y%8 == 0 and '~' in bits_to_words(bits2list(ttq)):
            wll = bits_to_words(bits2list(ttq))
            return key.decrypt(wll[:wll.index('~')].encode(encoder)).decode(encoder)
def load_ico(path,color):
    if not isfile(path):
        raise NameError('error icono no cargado')
    with open(path,'r') as ico:
        print(color + ico.read())
def save_image(img,name:str):
    name += '.png'
    Image.fromarray(img).save(name)
def banner():
    load_ico(r'D:\banner.txt',Fore.GREEN)
    sleep(1)
    print('''\n\n\n\n\n\n\n\n\n\n\n\n''')
    sleep(0.5)
    print(Fore.BLUE + 'que opercion desea hacer:','''
    [0] -> salir
    [1] -> esconder mensaje con LSB < sin cifrar>
    [2] -> leer mensaje con LSB < sin cifrar >
    [3] -> esconder mensaje con LSB < cifrando >
    [4] -> leer mensaje con LSB < cifrado >
    ''')
    flag = True
    while flag:
        inp = int(input('$>'))
        if inp == 0:
            flag = False
        if inp == 1:
            s1 = input('ingrese la ruta de la imagen: \n $>')
            s2 = input('ingrese el mensaje: \n $>')
            s3 = input('ingrese el titulo de su nueva imagen \n $>')
            s,v = LSB(s1,s2)
            save_image(s,s3)
            print(f'su largo de imagen es {v}')
            sleep(0.5)
        if inp == 2:
            s1 = input('ingrese la ruta de la imagen: \n $>')
            print(DLSB(s1))
            sleep(0.5)
        if inp == 3:
            s1 = input('ingrese la ruta de la imagen: \n $>')
            s2 = input('ingrese el mensaje: \n $>')
            s3 = input('ingrese su llave: \n $>')
            s4 = input('ingrese el titulo de su nueva imagen \n $>')
            im = crypto_LSB(s1,s2,s3)
            save_image(im,s4)
            sleep(0.5)
        if inp == 4:
            s1 = input('ingrese la ruta de la imagen: \n $>')
            s3 = input('ingrese su llave: \n $>')
            print(decrypt_LSB(s1,s3))
            sleep(0.5)
if __name__ == "__main__":
    banner()