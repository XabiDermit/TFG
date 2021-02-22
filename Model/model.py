import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from joblib import dump, load
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.metrics import precision_recall_fscore_support


class Model:
    model = None

    def parametroak_lortu(self, x_train, y_train, x_test, y_test):
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
        solvers = ['adam', 'lbfgs']

        parametro_egokiak = ()
        best_recall = 0
        for solver in solvers:
            for activation in aktibazioak:
                for topologia in topologiak:
                    # Sailkatzailea sortu
                    mlp = MLPClassifier(max_iter=500, activation=activation, solver=solver,
                                        hidden_layer_sizes=topologia, verbose=True)

                    # sailkatzailea entrenatu
                    mlp.fit(x_train, y_train)

                    # iragarpenak egin
                    iragarpenak = mlp.predict(x_test)

                    # bot klasearen recall-a kontuan hartuko da,
                    cls_report = precision_recall_fscore_support(y_test, iragarpenak, average='binary', pos_label=0)
                    print(cls_report)
                    bot_recall = cls_report[1]

                    # recall egokiena lortu
                    if bot_recall > best_recall:
                        best_recall = bot_recall
                        print("Best recall[bot]: " + str(bot_recall))
                        # recall horretarako parametroak gorde
                        parametro_egokiak = (solver, activation, topologia)

        print(" solver: " + parametro_egokiak[0] + " activation: " +
              parametro_egokiak[1] + " topologia: " + parametro_egokiak[2])

        return parametro_egokiak

    def entrenatu(self, parametroak, X, Y):
        # sailkatzailearen parametro optimoak jakinda, modeloa entrenatu eta gorde
        # modeloa sortu
        mlp = MLPClassifier(max_iter=500, solver=parametroak[0], activation=parametroak[1],
                            hidden_layer_sizes=parametroak[2])

        # modeloa entrenatu (orain datu guztiekin)
        mlp.fit(X, Y)
        print("Modeloa entrenatu da")

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
model.entrenatu(model.parametroak_lortu(x_train, y_train, x_test, y_test), X, Y)
