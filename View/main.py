import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow
from PyQt5.uic import loadUi
import Model.konexioa as login


class Loginaukeratu(QDialog):
    def __init__(self):
        super(Loginaukeratu, self).__init__()
        # leihoa kargatu
        loadUi("welcome.ui", self)
        # botoien funtzioak definitu
        self.kautotubtn.clicked.connect(self.kautotu)
        self.kautotugabebtn.clicked.connect(self.kontugabekautotu)

    def kautotu(self):
        auth = login.kontuarekinkautotu()
        pinsartu.setauth(auth)
        leiholista.setCurrentIndex(leiholista.currentIndex() + 1)

    def kontugabekautotu(self):
        login.kontugabekautotu()


class PinSartu(QDialog):
    auth = None

    def __init__(self):
        super(PinSartu, self).__init__()
        # leihoa kargatu
        loadUi("pin.ui", self)
        # botoien funtzioak definitu
        self.pinbtn.clicked.connect(self.pinsartu)

    def pinsartu(self):
        pin = self.pintf.text()
        api = login.autorizatu(self.auth, pin)
        timeline = Timeline(api)
        leiholista.addWidget(timeline)
        leiholista.setCurrentIndex(leiholista.currentIndex() + 1)

    def setauth(self, auth):
        self.auth = auth


class Timeline(QDialog):
    def __init__(self, api):
        super(Timeline, self).__init__()
        loadUi("timeline.ui", self)

        self.timeline.addItem("Hola")
        for txioa in api.home_timeline():
            print(txioa.text())
            self.timeline.addItem(txioa.text())


# aplikazioa sortu
app = QApplication(sys.argv)

# hasierapen berezia behar ez duten leihoak hasieratu
loginaukeratu = Loginaukeratu()
pinsartu = PinSartu()

# leihoen lista sortu eta leihoa bertan gorde
leiholista = QtWidgets.QStackedWidget()
leiholista.addWidget(loginaukeratu)
leiholista.addWidget(pinsartu)

# hasiera leihoa parametroak definitu
leiholista.setFixedWidth(1200)
leiholista.setFixedHeight(700)

# aplikazioa hasieratu
leiholista.show()
try:
    sys.exit(app.exec_())
except:
    print("Exiting")
