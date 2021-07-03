import time

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from joblib import dump, load
from sklearn import metrics


class Model:
    model = None

    def parametroak_lortu(self, X, Y):
        # metodo hau sailkatzailearentzako parametro optimoak lortzen ditu

        # train eta test multzoak lortu
        x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.33)

        # paremetro guztiak definitu
        topologiak = [100, (100, 50), (100, 50, 25, 10), (80, 40), (150, 100, 50), (125, 75, 25), (50, 100, 50),
                      (25, 75, 25), (100, 100, 100), (60, 40, 20), (125, 75, 25), (75, 125, 75), (225, 150, 75),
                      (25, 50, 75, 25), (250, 150, 50), (200, 100, 50), (300, 200, 100), (150, 75), (110, 55),
                      90, (125, 100, 75), 80, (150, 125, 100)]

        aktibazioak = ['identity', 'tanh', 'logistic', 'relu']

        parametro_egokiak = ()
        i = 0
        best_recall = 0.0
        for activation in aktibazioak:
            for topologia in topologiak:

                i += 1
                print("#######################################################################################")
                print(str(i) + ". iterazioa")
                print("Aktibazio funtzioa: " + activation)
                print("Topologia: " + str(topologia))

                # Sailkatzailea sortu
                mlp = MLPClassifier(max_iter=500, activation=activation, hidden_layer_sizes=topologia, verbose=False,
                                    n_iter_no_change=75)

                # sailkatzailea entrenatu
                mlp.fit(x_train, y_train)

                # sailkatzailea ebaluatu
                iragarpenak = mlp.predict(x_test)
                current_recall = metrics.recall_score(y_test, iragarpenak, pos_label=0)

                # recall egokiena lortu
                if current_recall > best_recall:
                    best_recall = current_recall
                    print("Best recall: " + str(current_recall))

                    # recall horretarako parametroak gorde
                    parametro_egokiak = (activation, topologia)

        # parametro optimoak inprimatu
        print(f"activation: {parametro_egokiak[0]}")
        print(f"topologia: {parametro_egokiak[1]}")

        return parametro_egokiak

    def entrenatu(self, parametroak, x, y):
        # sailkatzailearen parametro optimoak jakinda, modeloa entrenatu eta gorde
        # modeloa sortu
        mlp = MLPClassifier(max_iter=500, activation=parametroak[0], hidden_layer_sizes=parametroak[1],
                            n_iter_no_change=100)

        # modeloa entrenatu
        mlp.fit(x, y)
        print("Modeloa entrenatu da")

        # modeloaren kalitatearen estimazioa kalkulatu datu guztiekin: Ez-Zintzoa
        print("Kalitatearen estimazioa: Ez-Zintzoa:")
        iragarpenak = mlp.predict(x)
        print(metrics.classification_report(y, iragarpenak))
        print(metrics.confusion_matrix(y, iragarpenak))

        # modeloa gorde
        dump(mlp, 'Model2.joblib')
        print("Modeloa gorde da")

    def iragarri(self):
        # metodo hau modeloa kargatzen du eta iragarpen bat egiten du
        # modeloa kargatu
        if self.model is None:
            self.model = load('firstModel.joblib')

        # iragarri
        # mlp.predict


def denbora_erakutsi(exekuzio_denbora):
    # Metodo hau programaren exekuzio denbora txukun inprimatzen du
    egun = exekuzio_denbora // (24 * 3600)
    exekuzio_denbora %= (24 * 3600)
    ordu = exekuzio_denbora // 3600
    exekuzio_denbora %= 3600
    minutu = exekuzio_denbora // 60
    exekuzio_denbora %= 60
    segundu = exekuzio_denbora
    print("Egun:Ordu:Minutu:Segundu --> %d:%d:%d:%d" % (egun, ordu, minutu, segundu))


# datuak lortu
datu_egunetuak = pd.read_csv('datu_eguneratuak.csv')
data = np.array(datu_egunetuak)
X = data[:, 1:-1]
Y = data[:, -1]

# modelorako parametroak optimizatu
model = Model()
hasiera_denbora = time.time()
model.entrenatu(model.parametroak_lortu(X, Y), X, Y)
exekuzio_denbora = time.time() - hasiera_denbora
print("Modeloaren entrenamenduaren exekuzio denbora: ")
denbora_erakutsi(exekuzio_denbora)
