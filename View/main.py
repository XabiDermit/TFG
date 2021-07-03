import shutil
import sys

import requests
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow
from PyQt5.uic import loadUi
from PyQt5.QtGui import QPixmap
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
        mainleihoa.timelinebete()
        mainleihoa.userinfobete()
        leiholista.addWidget(mainleihoa)
        leiholista.setCurrentIndex(leiholista.currentIndex() + 2)

    def setauth(self, auth):
        self.auth = auth


class MainLeihoa(QDialog):
    def __init__(self, api):
        super(MainLeihoa, self).__init__()
        loadUi("mainleihoa.ui", self)
        self.api = api
        self.bilatubtn.clicked.connect(self.erabiltzaileasailkatu)

    def timelinebete(self):
        for txioa in self.api.home_timeline():
            self.timeline.addItem(txioa.text)

    def userinfobete(self):
        user = self.api.me()

        # irudia jarri
        ''' profile = user.profile_background_image_url
        irudia = profile.split("/")[-1]

        # Open the url image, set stream to True, this will return the stream content.

        r = requests.get(profile, stream=True)

        # Check if the image was retrieved successfully
        if r.status_code == 200:
            # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
            r.raw.decode_content = True

            # Open a local file with wb ( write binary ) permission.
            with open(irudia, 'wb') as f:
                shutil.copyfileobj(r.raw, f)
                pixmap = QPixmap(irudia)
                self.qIrudia.setPixmap(pixmap)

            print('Image sucessfully Downloaded: ', irudia)
        else:
            print('Image Couldn\'t be retreived')'''

        self.izena2lbl.setText(user.name)
        print("lagun kop:" + str(len(self.api.friends())))
        print("jarraitzaile kop: " + str(len(self.api.friends())))
        self.lagun2lbl.setText("74")
        self.jarraitzaile2lbl.setText("43")
        self.tweet2lbl.setText("4255")

    def erabiltzaileasailkatu(self):
        print(self.bilatutf.text())


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
