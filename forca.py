import os
import time

def menu(a):
    print(a)
    print("JOGO DA FORCA - CURSO PYTHON")
    print("Escolha a Opção:")
    print("1) Iniciar")
    print("2) Placar")
    print("3) Sair")
    op = input("Escolha o número da opção: ")
    return op


def layout_palavra(acertos, palavra_secreta, tentativas):
    os.system("clear")
    print()
    if tentativas == 1:
        enforcado02(q=0, w=1, e=0, r=0, t=0, y=0)
    elif tentativas == 2:
        enforcado02(q=0, w=2, e=0, r=0, t=0, y=0)
    elif tentativas == 3:
        enforcado02(q=0, w=3, e=0, r=0, t=0, y=0)
    elif tentativas == 4:
        enforcado02(q=0, w=3, e=4, r=6, t=7, y=11)
    elif tentativas == 5:
        enforcado()
    print()
    for acerto, letra in zip(acertos, palavra_secreta):
        if acerto: # quer dizer que se o acerto for igual a True
            print(letra.upper(), end=' ')
        else: #se o acerto for falso
            print('_', end=' ')

    print('\n\n')

def update_acertos(palavra_secreta, chute, acertos, lista_chute):
    lista_chute.append(chute)
    for i, letra in enumerate(palavra_secreta):
        if chute.lower() == letra:
            acertos[i] = True

def setup():
    palavra_secreta, dica = cria_palavra_dica()
    n_letras = len(palavra_secreta)
    acertos = [False]*n_letras
    return palavra_secreta.lower(), dica, n_letras, acertos


def jogar():
    os.system("clear")

    palavra_secreta, dica, n_letras, acertos = setup()
    tentativas = 0

    lista_chute=[]
    while tentativas < 5:
        layout_palavra(acertos, palavra_secreta, tentativas)
        lista_chute02 = ' - '.join(lista_chute)
        print('LETRAS CITADAS: {}'.format(lista_chute02).upper())
        print('\n')
        print('DICA SECRETA: %s' % dica)
        chute = input('\nTente uma letra: ')
        print('\n')
        update_acertos(palavra_secreta, chute, acertos, lista_chute)


        if chute not in palavra_secreta:

            tentativas += 1

            print(palavra_secreta)

            if tentativas == 5:
                layout_palavra(acertos, palavra_secreta,tentativas)
                print('ACABARAM AS TENTATIVAS!!!')
                print('\n\n')
                time.sleep(5)
                forca_python(a='MENU\n ')

        if all(acertos):
            layout_palavra(acertos, palavra_secreta, tentativas)
            print('\n')
            avatar_vencedor()
            print("PARABÉNS, VOCÊ GANHOU!!!")
            print('\n\n')
            time.sleep(5)
            forca_python(a='MENU \n')

def cria_palavra_dica():
    os.system("clear")
    palavra_secreta = input("\nDigite a palavra secreta: ")
    dica = input("\nDigite a dica: ")
    return palavra_secreta, dica


def forca_python(a = ' '):
    os.system("clear")
    op = int(menu(a))
    if op == 1:
        jogar()
    elif op == 2:
        print("tarefa")
    else:
        print('sair')

def enforcado():
    box = ['\u2572']
    a = [' ', ' ', box[0], ' ', '/']
    b = ['|', '|', '0', '|', ' ']
    c = [' ', ' ', '/----{Help!!!}', '', box[0]]
    for boneco in zip(a, b, c):
        print(''.join(boneco))


def enforcado02(q,w,e,r,t,y):
    box = [' \u2572']
    membros = [box[0], '0', '/', '', '', ' |', '', '', '/', box[0]]
    print(''.join(membros[q:w]), '\n', ''.join(membros[e:r]), '\n', ''.join(membros[t:y]))

def avatar_vencedor():
    box = ['\u2572']
    a = [' ', '/', '/']
    b = ['0', '|', ' ']
    c = ['----{Ufa!...Parabéns!!!}', box[0], box[0]]
    for boneco in zip(a, b, c):
        print(''.join(boneco))

def contador():
    a = 0
    while a < 20:
        a += 1
        print('=', end='')
        time.sleep(1)

def contagem_de_tempo_input(signum, frame):
    raise Exception(' ')


forca_python()