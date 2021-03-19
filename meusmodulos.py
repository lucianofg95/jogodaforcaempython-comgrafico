from PyQt5 import uic, QtWidgets

# global universal
# def recebepushbutton():
#     chute = "CUcu"
#     armazenar(chute)
#
# def armazenar(chute):
#     universal = chute
#     print(universal)
#     if forca.pushButton_2.clicked(True):
#         print("outr")


# def buscar(chute5):
#
#         print(chute5)
#
def imprimir():
    chute = input(forca.lineEdit_4.text())
    print(chute)

app = QtWidgets.QApplication([])
forca = uic.loadUi("forca.ui")
forca.pushButton_2.clicked.connect(imprimir)
# forca.pushButton.clicked.connect(recebepushbutton)

print(forca.pushButton_2.text())

forca.show()

app.exec()
