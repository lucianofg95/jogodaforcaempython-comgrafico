from PyQt5 import uic, QtWidgets
import time
import mysql.connector
from PyQt5.QtWidgets import QMessageBox

banco = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "123456",
    database = "bdforca"
)

def layout_palavra(tentativas): #puxar do banco de dados
    x = []
    cursor = banco.cursor()

    cursor.execute("select palavrasecreta from criapalavre where id = (SELECT MAX(id) as maxId FROM criapalavre)")
    palavra_secreta = cursor.fetchall()
    palavra_secreta = (palavra_secreta[0][0])

    print(tentativas)
    if tentativas == 1: #puxar tentativas da tabela chute
        enforcado02(q=0, w=1, e=0, r=0, t=0, y=0)
    elif tentativas == 2:
        enforcado02(q=0, w=2, e=0, r=0, t=0, y=0)
    elif tentativas == 3:
        enforcado02(q=0, w=3, e=0, r=0, t=0, y=0)
    elif tentativas == 4:
        enforcado02(q=0, w=3, e=4, r=6, t=7, y=11)
    elif tentativas == 5:
        enforcado()
        print('ACABARAM AS TENTATIVAS!!!')
        print('\n\n')
        sql = "delete from chute"
        cursor.execute(sql)
        banco.commit()
        time.sleep(5)
        chuta.close()
    print()
    print(acertos)
    for acerto, letra in zip(acertos, palavra_secreta):
        if acerto: # quer dizer que se o acerto for igual a True
            print(letra.upper(), end=' ')
            x.append(letra)
        else: #se o acerto for falso
            print('_', end=' ')
            x.append("_")

    y = " ".join(x)

    chuta.label_6.setText(y.upper())

    print('\n\n')

def update_acertos(lista_chute, acertos, tentativas):
    cursor = banco.cursor()
    chute = chuta.lineEdit_4.text()
    lista_chute.append(chute)
    print(lista_chute)
    cursor.execute("select palavrasecreta from criapalavre where id =(SELECT MAX(id) as maxId FROM criapalavre)")
    palavra_secreta = cursor.fetchall()
    palavra_secreta = (palavra_secreta[0][0])
    print(palavra_secreta)

    for i, letra in enumerate(palavra_secreta):
        if chute.lower() == letra:
            acertos[i] = True

    if chute not in palavra_secreta:
        tentativas = tentativas + 1


    sql = "insert chute(letrascitadas, tentativa) values (%s, %s)"
    cursor.execute(sql, (chute, tentativas))

    if tentativas == 5:
        layout_palavra(tentativas)


    if all(acertos):
        layout_palavra(tentativas)
        print('\n')
        avatar_vencedor()
        print("PARABÉNS, VOCÊ GANHOU!!!")
        print('\n\n')
        sql = "delete from chute"
        cursor.execute(sql)
        banco.commit()
        time.sleep(5)
    print(tentativas)
    banco.commit()


def setup():

    global acertos
    palavra1 = forca.lineEdit.text()
    palavra2 = forca.lineEdit_2.text()

    if palavra1 == palavra2:
        cria_palavra_dica()
        cursor = banco.cursor()

        cursor.execute("select palavrasecreta from criapalavre where id= (SELECT MAX(id) as maxId FROM criapalavre)")
        n_letras = cursor.fetchall()
        n_letras = (len(n_letras[0][0]))

        # inserir numero de palavras no banco de dados.
        acertos = ([False] * n_letras)
        print(acertos)
        teste = 2
        cursor.execute("insert into setup(numerodeletras, acertos) values('%s','%s')", (n_letras, teste))
        cursor.execute("insert into chute(letrascitadas, tentativa) values(' ','0')")
        chuta.show()
        chuta.label_7.setText(forca.lineEdit_3.text().upper())
    else:
        QMessageBox.about(forca, "aviso", "REPETIÇÃO DA PALAVRA NÃO CONFERE!")



def chutaai():
    if ((chuta.lineEdit_4.text()) not in lista_chute):

        cursor = banco.cursor()
        sql = "select tentativa from chute where id = (SELECT MAX(id) FROM chute)"
        cursor.execute(sql)
        tentativas = cursor.fetchall()
        tentativas = (tentativas[0][0])

        if tentativas < 5:
            lista_chute02 = ' - '.join(lista_chute)
            print('LETRAS CITADAS: {}'.format(lista_chute02).upper())
            print('\n')
            cursor.execute("select dica from criapalavre where id =(SELECT MAX(id) as maxId FROM criapalavre)")
            dica = cursor.fetchall()
            dica = (dica[0][0])
            print(dica)
            print('DICA SECRETA: %s' %dica)
            print('\n')
            update_acertos(lista_chute, acertos, tentativas)
            print("passou do update")

        sql = "select tentativa from chute where id = (SELECT MAX(id) FROM chute)"
        cursor.execute(sql)
        tentativas = cursor.fetchall()
        tentativas = (tentativas[0][0])

        layout_palavra(tentativas)

        lista_chutelabel = ((" - ".join(lista_chute)).upper())
        chuta.label_10.setText(lista_chutelabel)
        chuta.lineEdit_4.setText("")

    else:
        QMessageBox.about(chuta,"AVISO", "LETRA JÁ CITADA")

def cria_palavra_dica():
    cursor = banco.cursor()
    palavra = forca.lineEdit.text()
    dica = forca.lineEdit_3.text()
    cursor.execute("insert into criapalavre(palavrasecreta, dica) values ('" + palavra + "','" + dica + "')")


def enforcado():
    box = ['\u2572']
    a = [' ', ' ', box[0], ' ', '/']
    b = ['|', '|', '0', '|', ' ']
    c = [' ', ' ', '/----{Help!!!}', '', box[0]]
    for boneco in zip(a, b, c):
        print(''.join(boneco))
        chuta.label_4.setText(''.join(boneco))

def enforcado02(q,w,e,r,t,y):
    box = [' \u2572']
    membros = [box[0], '0', '/', '', '', ' |', '', '', '/', box[0]]
    print(''.join(membros[q:w]), '\n', ''.join(membros[e:r]), '\n', ''.join(membros[t:y]))
    chuta.label_4.setText(''.join(membros[q:w]))
    chuta.label_8.setText(''.join(membros[e:r]))
    chuta.label_9.setText(''.join(membros[t:y]))


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



app=QtWidgets.QApplication([])
forca=uic.loadUi("forca.ui")
chuta=uic.loadUi("chuteletra.ui")
forca.pushButton.clicked.connect(setup)
chuta.pushButton_2.clicked.connect(chutaai)

global lista_chute
lista_chute = []



forca.show()

app.exec()
