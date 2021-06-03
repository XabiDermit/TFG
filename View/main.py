import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow
from PyQt5.uic import loadUi
import Model.konexioa as login


class Loginaukeratu(QDialog):
    def __init__(self):
        super(Loginaukeratu, self).__init__()
        # leihoa kargatu
        loadUi("hasieraleihoa.ui", self)
        # botoien funtzioak definitu
        self.kautotubtn.clicked.connect(self.kautotu)
        self.kautotugabebtn.clicked.connect(self.kontugabekautotu)

    def kautotu(self):
        auth = login.kontuarekinkautotu()
        pinsartu.setauth(auth)
        leiholista.setCurrentIndex(leiholista.currentIndex() + 1)

    def kontugabekautotu(self):
        login.kontugabekautotu()
        leiholista.setCurrentIndex(leiholista.currentIndex() + 2)


class PinSartu(QDialog):
    auth = None

    def __init__(self):
        super(PinSartu, self).__init__()
        # leihoa kargatu
        loadUi("pinsartu.ui", self)
        # botoien funtzioak definitu
        self.pinbtn.clicked.connect(self.pinsartu)

    def pinsartu(self):
        pin = self.pintf.text()
        api = login.autorizatu(self.auth, pin)
        mainleihoa = MainLeihoa(api)
        leiholista.addWidget(mainleihoa)
        leiholista.setCurrentIndex(leiholista.currentIndex() + 1)

    def setauth(self, auth):
        self.auth = auth


class MainLeihoa(QDialog):
    def __init__(self, api):
        super(MainLeihoa, self).__init__()
        loadUi("mainleihoa.ui", self)

        self.timeline.addItem("Hola")
        for txioa in api.home_timeline():
            print(txioa.text)
            self.timeline.addItem(txioa.text)


class SimpleMainLeihoa(QDialog):

    def __init__(self):
        super(SimpleMainLeihoa, self).__init__()
        loadUi("simplemainleihoa.ui", self)
        self.bilatubtn.clicked.connect(self.erabiltzaileasailkatu)

    def erabiltzaileasailkatu(self):
        print(self.bilatutf.text())


# aplikazioa sortu
app = QApplication(sys.argv)

# hasierapen berezia behar ez duten leihoak hasieratu
loginaukeratu = Loginaukeratu()
pinsartu = PinSartu()
simpleMainLeihoa = SimpleMainLeihoa()

# leihoen lista sortu eta leihoa bertan gorde
leiholista = QtWidgets.QStackedWidget()
leiholista.addWidget(loginaukeratu)
leiholista.addWidget(pinsartu)
leiholista.addWidget(simpleMainLeihoa)

# hasiera leihoa parametroak definitu
leiholista.setFixedWidth(1200)
leiholista.setFixedHeight(700)

# aplikazioa hasieratu
leiholista.show()
try:
    sys.exit(app.exec_())
except:
    print("Exiting")
