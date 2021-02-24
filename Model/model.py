import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from joblib import dump, load
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.metrics import precision_recall_fscore_support


class Model:
    model = None

    def parametroak_lortu(self, x, y):
        # metodo hau sailkatzailearentzako parametro optimoak lortzen ditu

        # paremetro optimoenak bilatu
        topologiak = [100, (100, 50), (50, 25, 12), (12, 6, 2), (25, 12, 4), (25, 25),
                      (100, 50, 25, 10), (80, 40), 150, (150, 100, 50), (80, 40, 20, 10),
                      (125, 75, 25), (70, 35, 18), (50, 100, 50), (25, 50, 100, 50, 25),
                      (25, 75, 25), (100, 100, 100), (75, 50, 25, 12), (20, 40, 20),
                      (15, 15, 15), (35, 70, 35), (12, 25, 12), (30, 60, 90, 60, 30),
                      (40, 20, 10, 5), (60, 40, 20), (150, 125, 100, 75, 50, 25),
                      (125, 75, 25), (75, 125, 75), (30, 45, 30, 15), (80, 60, 40, 20),
                      90, 80, 70, 60, 50, 40, 30, 20, 10, (25, 50, 75, 25), 200, 300,
                      (200, 100, 50), (300, 200, 100), (200, 150, 100, 50, 25),
                      (120, 60), (90, 45), (150, 75), (110, 55)]
        aktibazioak = ['identity', 'tanh', 'logistic', 'relu']


        parametro_egokiak = ()
        best_loss = float('inf')
        for activation in aktibazioak:
            for topologia in topologiak:
                # Sailkatzailea sortu
                mlp = MLPClassifier(max_iter=500, activation=activation, hidden_layer_sizes=topologia, verbose=True,
                                    n_iter_no_change=50)

                # sailkatzailea entrenatu
                mlp.fit(x, y)

                current_loss = mlp.best_loss_

                # recall egokiena lortu
                if current_loss < best_loss:
                    best_loss = current_loss
                    print("Best loss: " + str(current_loss))
                    # recall horretarako parametroak gorde
                    parametro_egokiak = (activation, topologia)

        print(f"activation: {parametro_egokiak[0]}")
        print(f"topologia: {parametro_egokiak[1]}")

        return parametro_egokiak

    def entrenatu(self, parametroak, x, y):
        # sailkatzailearen parametro optimoak jakinda, modeloa entrenatu eta gorde
        # modeloa sortu
        mlp = MLPClassifier(max_iter=500,  activation=parametroak[0], hidden_layer_sizes=parametroak[1],
                            n_iter_no_change=50)

        # modeloa entrenatu
        mlp.fit(x, y)
        print("Modeloa entrenatu da")

        # modeloaren kalitatearen estimazioa kalkulatu datu guztiekin: Ez-Zintzoa
        print("Kalitatearen estimazioa: Ez-Zintzoa:")
        iragarpenak = mlp.predict(x)
        print(classification_report(y, iragarpenak))
        print(confusion_matrix(y, iragarpenak))

        # modeloa gorde
        dump(mlp, 'model.joblib')
        print("Modeloa gorde da")

    def iragarri(self):
        # metodo hau modeloa kargatzen du eta iragarpen bat egiten du
        # modeloa kargatu
        if self.model is None:
            self.model = load('model.joblib')

        # iragarri
        # mlp.predict


# datuak lortu
datu_egunetuak = pd.read_csv('datu_eguneratuak.csv')
data = np.array(datu_egunetuak)
X = data[:, 1:-1]
Y = data[:, -1]

# train eta test multzoak lortu
x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.33)

# modelorako parametroak optimizatu
model = Model()
model.entrenatu(model.parametroak_lortu(X, Y), X, Y)

