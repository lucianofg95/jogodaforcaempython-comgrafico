from PyQt5 import uic, QtWidgets
import time
import mysql.connector
from PyQt5.QtWidgets import QMessageBox
from peewee import SqliteDatabase, Model, TextField, ForeignKeyField, DateTimeField, IntegerField,fn

db = SqliteDatabase('bdforca.db')

class basemodel(Model):
    class Meta:
        database = db

class usuario(basemodel):
    nome = TextField(unique=True)
    vitoria = IntegerField()
    derrota = IntegerField()

class criapalavra(basemodel):
    jogador = ForeignKeyField(usuario, backref='usuarios')
    palavrasecreta = TextField()
    dica = TextField()
    datacriacao = DateTimeField(default='datetime.now()')

class chutejog(basemodel):
    jogador02 = ForeignKeyField(usuario, backref='usuarios')
    letracitada = TextField()
    tentativa = IntegerField()

db.create_tables([usuario, criapalavra, chutejog] )


banco = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "123456",
    database = "bdforca"
)
alfabeto=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',' ','ç']

def login():
    usuariologin.show()
    jogadoresativos = []

    for row in (usuario.select()):
        n_jog = (row.nome)
        for row in (usuario.select().where(usuario.nome == n_jog)):
            jogadoresativos.append(row.nome)
            jogadoresativos.append(row.vitoria)
            jogadoresativos.append(row.derrota)

    n_usuarios= 0
    for row in (usuario.select()):
        n_usuarios += 1

    usuariologin.tableWidget.setRowCount(n_usuarios)
    usuariologin.tableWidget.setColumnCount(3)

    q = 0
    for i in range(0, n_usuarios):
        for j in range(0,3):
            usuariologin.tableWidget.setItem(i,j,QtWidgets.QTableWidgetItem(str(jogadoresativos[q])))
            q += 1

def criarlogin():
    nomeusuario = usuariologin.lineEdit.text()
    usuario.create(
        nome= nomeusuario,
        vitoria= 0,
        derrota= 0
    )
    for row in (usuario.select().where(usuario.nome == nomeusuario)):
        forca.comboBox.addItem(row.nome)
        forca.comboBox_2.addItem(row.nome)

    usuariologin.lineEdit.setText("")





def layout_palavra(tentativas): #puxar do banco de dados
    x = []

    for row in (criapalavra.select(criapalavra.palavrasecreta, fn.max(criapalavra.id))):
        palavra_secreta = (row.palavrasecreta)

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
        chutejog.delete()
        time.sleep(5)

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

    delete = chutejog.delete()
    chutex = chuta.lineEdit_4.text()
    lista_chute.append(chutex)
    print(lista_chute)

    for row in (criapalavra.select(criapalavra.palavrasecreta, fn.MAX(criapalavra.id))):
        palavra_secreta = (row.palavrasecreta)

    for i, letra in enumerate(palavra_secreta):
        if chutex.lower() == letra:
            acertos[i] = True

    if chutex not in palavra_secreta:
        tentativas = tentativas + 1


    try:
        chutejogagor = chutejog.create(
            jogador02=jogadorpartida,
            letracitada=chutex,
            tentativa=tentativas
        )
        chutejogagor.save()
    except:
        print("erro de execução ao inserir chute no banco de dados")


    if tentativas == 5:
        layout_palavra(tentativas)
        delete.execute()
        pontopositivo = usuario.update(derrota=usuario.derrota + 1).where(usuario.id == jogadorpartida)
        pontonegativo = usuario.update(vitoria=usuario.vitoria + 1).where(usuario.id == criadorpalavra)
        pontopositivo.execute()
        pontonegativo.execute()

    if all(acertos):
        delete.execute()
        layout_palavra(tentativas)
        print('\n')
        avatar_vencedor()
        print("PARABÉNS, VOCÊ GANHOU!!!")
        print('\n\n')
        try:
            pontopositivo = usuario.update(vitoria=usuario.vitoria + 1).where(usuario.id == jogadorpartida)
            pontonegativo = usuario.update(derrota=usuario.derrota + 1).where(usuario.id == criadorpalavra)
            pontopositivo.execute()
            pontonegativo.execute()

        except:
            print("erro de execução")
        # time.sleep(5)
    print(tentativas)


def setup():

    global acertos

    palavra1 = forca.lineEdit.text()
    palavra2 = forca.lineEdit_2.text()
    global jogadorpartida
    for row in (usuario.select(usuario.id).where(usuario.nome == forca.comboBox_2.currentText())):
        jogadorpartida = (row.id)

    if palavra1 == palavra2:
        cria_palavra_dica()

        for row in (criapalavra.select(criapalavra.palavrasecreta,fn.MAX(criapalavra.id))):
            n_letras = (row.palavrasecreta)
            n_letras = len(n_letras)

        # inserir numero de palavras no banco de dados.
        acertos = ([False] * n_letras)
        print(acertos)

        try:
            chutejogagor = chutejog.create(
                jogador02=jogadorpartida,
                letracitada=' ',
                tentativa=0
            )
            chutejogagor.save()
        except:
            print("erro de execução ao inserir chute de referência primário no banco de dados")

        chuta.show()
        chuta.label_7.setText(forca.lineEdit_3.text().upper())
    else:
        QMessageBox.about(forca, "aviso", "REPETIÇÃO DA PALAVRA NÃO CONFERE!")



def chutaai():
    if ((chuta.lineEdit_4.text()) in alfabeto):
        if ((chuta.lineEdit_4.text()) not in lista_chute):

            for row in (chutejog.select(chutejog.tentativa, fn.max(chutejog.id))):
                tentativas = (row.tentativa)



            if tentativas < 5:
                lista_chute02 = ' - '.join(lista_chute)
                print('LETRAS CITADAS: {}'.format(lista_chute02).upper())
                print('\n')
                for row in (criapalavra.select(criapalavra.dica, fn.max(criapalavra.id))):
                    dica = (row.dica)

                print(dica)
                print('DICA SECRETA: %s' %dica)
                print('\n')
                update_acertos(lista_chute, acertos, tentativas)
                print("passou do update")

            for row in (chutejog.select(chutejog.tentativa, fn.max(chutejog.id))):
                tentativas = (row.tentativa)

            layout_palavra(tentativas)

            lista_chutelabel = ((" - ".join(lista_chute)).upper())
            chuta.label_10.setText(lista_chutelabel)
            chuta.lineEdit_4.setText("")


        else:
            QMessageBox.about(chuta,"AVISO", "LETRA JÁ CITADA")
    else:
        QMessageBox.about(chuta, "AVISO", "Caractere inválido!")


def cria_palavra_dica():
    cursor = banco.cursor()

    palavra = forca.lineEdit.text()
    dica = forca.lineEdit_3.text()
    global criadorpalavra
    for row in (usuario.select().where(usuario.nome == forca.comboBox.currentText())):
        criadorpalavra = (row.id)

    cursor.execute("insert into criapalavre(palavrasecreta, dica) values ('" + palavra + "','" + dica + "')")

    try:
        criapalavra.create(
            jogador=criadorpalavra,
            palavrasecreta=palavra,
            dica=dica
        )
    except:
        print("erro de execução")

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

def jogarnovamente():
    chuta.label_7.setText("")
    chuta.label_10.setText("")
    chuta.label_6.setText("")
    forca.lineEdit.setText("")
    forca.lineEdit_2.setText("")
    forca.lineEdit_3.setText("")
    chuta.close()
    forca.close()
    forca.show()
    lista_chute.clear()



app=QtWidgets.QApplication([])
forca=uic.loadUi("forca.ui")
chuta=uic.loadUi("chuteletra.ui")
usuariologin=uic.loadUi("usuario.ui")
forca.pushButton.clicked.connect(setup)
chuta.pushButton_2.clicked.connect(chutaai)
forca.pushButton_2.clicked.connect(login)
usuariologin.pushButton_2.clicked.connect(criarlogin)
chuta.pushButton.clicked.connect(jogarnovamente)

global lista_chute
lista_chute = []



forca.show()

for row in (usuario.select()):
    forca.comboBox.addItem(row.nome)
    forca.comboBox_2.addItem(row.nome)


app.exec()
