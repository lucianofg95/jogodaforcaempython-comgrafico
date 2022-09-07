from PyQt6 import uic, QtWidgets
from PyQt6.QtWidgets import QMessageBox
from peewee import SqliteDatabase, Model, TextField, ForeignKeyField, DateTimeField, IntegerField,fn
from PyQt6 import QtGui

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

alfabeto=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',' ','ç']

def placarjogadores():
    placar.show()
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

    placar.tableWidget.setRowCount(n_usuarios)
    placar.tableWidget.setColumnCount(3)

    q = 0
    for i in range(0, n_usuarios):
        for j in range(0,3):
            placar.tableWidget.setItem(i,j,QtWidgets.QTableWidgetItem(str(jogadoresativos[q])))
            q += 1
def login():
    usuariologin.close()
    usuariologin.show()
    jogadoresativos = []


    for row in (usuario.select()):
        n_jog = (row.nome)
        for row in (usuario.select().where(usuario.nome == n_jog)):
            jogadoresativos.append(row.nome)


    n_usuarios= 0
    for row in (usuario.select()):
        n_usuarios += 1

    usuariologin.tableWidget.setRowCount(n_usuarios)
    usuariologin.tableWidget.setColumnCount(3)

    q = 0
    for i in range(0, n_usuarios):
        for j in range(0,1):
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

        usuariologin.tableWidget.clear()

    usuariologin.lineEdit.setText("")
    login()


def layout_palavra(tentativas): #puxar do banco de dados
    x = []

    for row in (criapalavra.select(criapalavra.palavrasecreta, fn.max(criapalavra.id))):
        palavra_secreta = (row.palavrasecreta)

    if tentativas == 1: #puxar tentativas da tabela chute
        chuta.label_12.setPixmap(QtGui.QPixmap('forca1.png'))
    elif tentativas == 2:
        chuta.label_12.setPixmap(QtGui.QPixmap('forca2.png'))
    elif tentativas == 3:
        chuta.label_12.setPixmap(QtGui.QPixmap('forca3.png'))
    elif tentativas == 4:
        chuta.label_12.setPixmap(QtGui.QPixmap('forca4.png'))
    elif tentativas == 5:
        QMessageBox.about(chuta, "Perdeu", "INFELIZMENTE, VOCÊ PERDEU!")
        chuta.label_12.setPixmap(QtGui.QPixmap('forca6.png'))
        chutejog.delete()


    for acerto, letra in zip(acertos, palavra_secreta):
        if acerto: # quer dizer que se o acerto for igual a True
            x.append(letra)
        else: #se o acerto for falso
            x.append("_")

    y = " ".join(x)

    chuta.label_6.setText(y.upper())


def update_acertos(lista_chute, acertos, tentativas):

    delete = chutejog.delete()
    chutex = chuta.lineEdit_4.text()
    lista_chute.append(chutex)

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
        chuta.label_12.setPixmap(QtGui.QPixmap('forca7.png'))
        try:
            pontopositivo = usuario.update(vitoria=usuario.vitoria + 1).where(usuario.id == jogadorpartida)
            pontonegativo = usuario.update(derrota=usuario.derrota + 1).where(usuario.id == criadorpalavra)
            pontopositivo.execute()
            pontonegativo.execute()

        except:
            print("erro de execução")

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
        chuta.label_12.setPixmap(QtGui.QPixmap("forca0.png"))

    else:
        QMessageBox.about(forca, "aviso", "REPETIÇÃO DA PALAVRA NÃO CONFERE!")

def chutaai():

    if ((chuta.lineEdit_4.text()) in alfabeto):
        if ((chuta.lineEdit_4.text()) not in lista_chute):

            for row in (chutejog.select(chutejog.tentativa, fn.max(chutejog.id))):
                tentativas = (row.tentativa)

            if tentativas < 5:
                for row in (criapalavra.select(criapalavra.dica, fn.max(criapalavra.id))):
                    dica = (row.dica)

                update_acertos(lista_chute, acertos, tentativas)

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

    palavra = forca.lineEdit.text()
    dica = forca.lineEdit_3.text()
    global criadorpalavra
    for row in (usuario.select().where(usuario.nome == forca.comboBox.currentText())):
        criadorpalavra = (row.id)

    try:
        criapalavra.create(
            jogador=criadorpalavra,
            palavrasecreta=palavra,
            dica=dica
        )
    except:
        print("erro de execução")

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

def excluirusuario():
    ids = []

    linha = usuariologin.tableWidget.currentRow()
    usuariologin.tableWidget.removeRow(linha)

    for row in (usuario.select()):
        ids.append(row.id)

    removerusuario = usuario.delete().where(usuario.id == (ids[linha]))
    removerusuario.execute()

    forca.comboBox.clear()
    forca.comboBox_2.clear()

    for row in (usuario.select()):
        forca.comboBox.addItem(row.nome)
        forca.comboBox_2.addItem(row.nome)

def fecharplacardejogadores():
    placar.close()

app=QtWidgets.QApplication([])
forca=uic.loadUi("forca.ui")
chuta=uic.loadUi("chuteletra.ui")
usuariologin=uic.loadUi("usuario.ui")
placar = uic.loadUi("placar.ui")
forca.pushButton.clicked.connect(setup)
chuta.pushButton_2.clicked.connect(chutaai)
forca.pushButton_2.clicked.connect(login)
usuariologin.pushButton_2.clicked.connect(criarlogin)
chuta.pushButton.clicked.connect(jogarnovamente)
forca.pushButton_3.clicked.connect(placarjogadores)
usuariologin.pushButton.clicked.connect(excluirusuario)
placar.pushButton.clicked.connect(fecharplacardejogadores)

global lista_chute
lista_chute = []
forca.show()
forca.label_7.setPixmap(QtGui.QPixmap('corda.png'))
forca.label_8.setPixmap(QtGui.QPixmap('corda2.png'))

for row in (usuario.select()):
    forca.comboBox.addItem(row.nome)
    forca.comboBox_2.addItem(row.nome)

app.exec()
