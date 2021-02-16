import sklearn as sk
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn import neural_network
from sklearn.metrics import classification_report, confusion_matrix


def entrenatu(X_train, X_test, y_train, y_test):

    # sare neuronalerako topologia desberdinak definitu
    topologies = [100, 50, (100, 50), (50, 25, 12), (12,6,2), (25, 12, 4)]

    # aktibazio funtzio posible guztiekin probatu
    # activations = ['identity', 'logistic', 'relu', 'softmax', 'tanh'] --> softmax errorea ematen du
    activations = ['identity', 'tanh', 'logistic', 'relu']

    best_options = ()
    lowest_loss = float('inf')
    for activation in activations:
        print("################################### " + activation + " #################################")
        for topology in topologies:
            print("############################## topologia= " + str(topology) + "###################################")
            # modeloa sortu
            clf = sk.neural_network.MLPClassifier(max_iter=500, activation=activation, verbose=True,
                                                  hidden_layer_sizes=topology)

            # modeloa entrenatu
            clf.fit(X_train, y_train)

            print("Menor error: " + str(clf.best_loss_))

            # errore txikiena egunertu eta parametro hoberenak gorde
            if clf.best_loss_ < lowest_loss:
                lowest_loss = clf.best_loss_
                best_options = (activation, topology, "loss = " + str(clf.best_loss_))

    print(best_options)

    return best_options

# datuak lortu
datu_egunetuak = pd.read_csv('datu_eguneratuak.csv')
data = np.array(datu_egunetuak)
X = data[:, 1:-1]
Y = data[:, -1]
# train eta test multzoak lortu
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.3)

aukerak = entrenatu(X_train, X_test, y_train, y_test)
clf = sk.neural_network.MLPClassifier(max_iter=500, activation=aukerak[0], hidden_layer_sizes=aukerak[1])
clf.fit(X_train,y_train)
predicciones = clf.predict(X_test)
print(confusion_matrix(y_test,predicciones))
print(classification_report(y_test,predicciones))