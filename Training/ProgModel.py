from keras.models import Sequential
from keras.layers import Dense, Conv2D, Flatten  # create model
from keras.layers import Input
from keras.models import Sequential, load_model, Model
import numpy as np
import pickle as pk
from keras import regularizers


def conv_layer(x, filters, kernel_size, act):
    x = Conv2D(
        filters=filters
        , kernel_size=kernel_size
        , data_format="channels_first"
        , padding='same'
        , kernel_regularizer=regularizers.l2(0.0001)
        , use_bias=False
        , activation=act
    )(x)
    return (x)


def softmax(x, name):
    x = Flatten()(x)

    x = Dense(
        362
        , use_bias=False
        , kernel_regularizer=regularizers.l2(0.0001)
        , activation='softmax'
        , name=name
    )(x)

    return (x)


def build_model():
    main_input = Input(shape=(24, 19, 19), name='main_input')

    x = conv_layer(main_input, 92, 5, 'linear')

    for h in range(6):
        x = conv_layer(x, 384, 3, 'relu')

    K1 = conv_layer(x, 1, 3, 'linear')
    K2 = conv_layer(x, 1, 3, 'linear')
    K3 = conv_layer(x, 1, 3, 'linear')

    K1 = softmax(K1, "k1")
    K2 = softmax(K2, "k2")
    K3 = softmax(K3, "k3")

    model = Model(inputs=[main_input], outputs=[K1, K2, K3])

    model.compile(
        loss={"k1": "categorical_crossentropy", "k2": "categorical_crossentropy", "k3": "categorical_crossentropy"},
        optimizer='adam', metrics=['categorical_accuracy'])
    return model


def readData(modelInput):
    TrainingStates = []
    Truth = []
    k1, k2, k3 = [], [], []

    for data in modelInput:
        TrainingStates.append(data[0])

        k1temp = np.reshape(data[1][0], 19 * 19)
        k1.append(np.append(k1temp, int(np.sum(k1temp) == 0)))

        k2temp = np.reshape(data[1][1], 19 * 19)
        k2.append(np.append(k2temp, int(np.sum(k2temp) == 0)))

        k3temp = np.reshape(data[1][2], 19 * 19)
        k3.append(np.append(k3temp, int(np.sum(k3temp) == 0)))

    k1 = np.asarray(k1)
    k2 = np.asarray(k2)
    k3 = np.asarray(k3)
    TrainingStates = np.asarray(TrainingStates)
    Truth = {'k1': k1, 'k2': k2, 'k3': k3}
    return TrainingStates, Truth


def release_list(a):
    del a


#model = build_model()
model = load_model('LargeNoKoModel27.h5')


# modelInput7 = pk.load(open("VtrainigData/NoKoTrainingData_3000.pkl", 'rb'))
"""""
modelInput8 = pk.load(open("VtrainigData/NoKoTrainingData_3088.pkl", 'rb'))
modelInput9 = pk.load(open("VtrainigData/NoKoTrainingData_3300.pkl", 'rb'))
modelInput10 = pk.load(open("VtrainigData/NoKoTrainingData_3600.pkl", 'rb'))
modelInput11 = pk.load(open("VtrainigData/NoKoTrainingData_3900.pkl", 'rb'))

modelInput12 = pk.load(open("VtrainigData/NoKoTrainingData_1650.pkl", 'rb'))
modelInput13 = pk.load(open("VtrainigData/NoKoTrainingData_1700.pkl", 'rb'))
modelInput14 = pk.load(open("VtrainigData/NoKoTrainingData_1150.pkl", 'rb'))
modelInput15 = pk.load(open("TrainingData_680.pkl", 'rb'))
modelInput16 = (pk.load(open("TrainingData_700.pkl", 'rb')))
modelInput17 = pk.load(open("TrainingData_731.pkl", 'rb'))
modelInput18 = (pk.load(open("TrainingData_720.pkl", 'rb')))
"""

for i in range(30):
    for j in range(6):
        if j == 0:
            modelInput1 = pk.load(open("VtrainigData/NoKoTrainingData_1200.pkl", 'rb'))
            modelInput2 = pk.load(open("VtrainigData/NoKoTrainingData_1500.pkl", 'rb'))
            modelInput3 = pk.load(open("VtrainigData/NoKoTrainingData_1800.pkl", 'rb'))
            modelInput4 = pk.load(open("VtrainigData/NoKoTrainingData_2100.pkl", 'rb'))

            modelInput = np.concatenate((modelInput1, modelInput2, modelInput3, modelInput4), axis=0)

            TrainingStatesT, TruthT = readData(modelInput)


        elif j == 1:
            modelInput6 = pk.load(open("VtrainigData/NoKoTrainingData_3088.pkl", 'rb'))
            modelInput7 = pk.load(open("VtrainigData/NoKoTrainingData_3300.pkl", 'rb'))
            modelInput8 = pk.load(open("VtrainigData/NoKoTrainingData_3600.pkl", 'rb'))
            modelInput9 = pk.load(open("VtrainigData/NoKoTrainingData_3900.pkl", 'rb'))

            modelInput = np.concatenate((modelInput6, modelInput7, modelInput8, modelInput9), axis=0)

            TrainingStatesT, TruthT = readData(modelInput)

        elif j == 2:
            modelInput11 = pk.load(open("VtrainigData/NoKoTrainingData_4200.pkl", 'rb'))
            modelInput12 = pk.load(open("VtrainigData/NoKoTrainingData_4500.pkl", 'rb'))
            modelInput13 = pk.load(open("VtrainigData/NoKoTrainingData_4800.pkl", 'rb'))
            modelInput25 = pk.load(open("VtrainigData/NoKoTrainingData_2700.pkl.", 'rb'))

            modelInput = np.concatenate((modelInput11, modelInput12, modelInput13, modelInput25), axis=0)

            TrainingStatesT, TruthT = readData(modelInput)


        elif j == 3:
            modelInput16 = pk.load(open("VtrainigData/NoKoTrainingData_5400.pkl", 'rb'))
            modelInput17 = pk.load(open("VtrainigData/NoKoTrainingData_5700.pkl", 'rb'))
            modelInput18 = pk.load(open("VtrainigData/NoKoTrainingData_6000.pkl", 'rb'))
            modelInput19 = pk.load(open("VtrainigData/NoKoTrainingData_6300.pkl", 'rb'))

            modelInput = np.concatenate((modelInput16, modelInput17, modelInput18, modelInput18), axis=0)
            TrainingStatesT, TruthT = readData(modelInput)


        elif j == 4:
            modelInput21 = pk.load(open("VtrainigData/NoKoTrainingData_6600.pkl", 'rb'))
            modelInput22 = pk.load(open("VtrainigData/NoKoTrainingData_6900.pkl", 'rb'))
            modelInput15 = pk.load(open("VtrainigData/NoKoTrainingData_5100.pkl.", 'rb'))
            modelInput24 = pk.load(open("VtrainigData/NoKoTrainingData_7200.pkl", 'rb'))

            modelInput = np.concatenate((modelInput21, modelInput22, modelInput15, modelInput24), axis=0)

            TrainingStatesT, TruthT = readData(modelInput)

        elif j == 5:
            modelInput5 = pk.load(open("VtrainigData/NoKoTrainingData_2400.pkl.", 'rb'))
            modelInput10 = pk.load(open("VtrainigData/NoKoTrainingData_3000.pkl.", 'rb'))
            modelInput20 = pk.load(open("VtrainigData/NoKoTrainingData_6354.pkl", 'rb'))
            modelInput23 = pk.load(open("VtrainigData/NoKoTrainingData_7016.pkl", 'rb'))
            modelInput14 = pk.load(open("VtrainigData/NoKoTrainingData_4970.pkl", 'rb'))
            modelInput = np.concatenate((modelInput5, modelInput10, modelInput23, modelInput20, modelInput14), axis=0)

            TrainingStatesT, TruthT = readData(modelInput)

        model.fit(TrainingStatesT, TruthT, epochs=1, batch_size=256, shuffle=True, verbose=2, validation_split=.001)

        modelInput = []
        TrainingStatesT = []
        TruthT = []
        modelInput1 = []
        modelInput2 = []
        modelInput3 = []
        modelInput4 = []
        modelInput5 = []
        modelInput6 = []
        modelInput7 = []
        modelInput8 = []
        modelInput9 = []
        modelInput10 = []
        modelInput11 = []
        modelInput12 = []
        modelInput13 = []
        modelInput14 = []
        modelInput15 = []
        modelInput16 = []
        modelInput17 = []
        modelInput18 = []
        modelInput19 = []
        modelInput20 = []
        modelInput21 = []
        modelInput22 = []
        modelInput23 = []
        modelInput24 = []
        modelInput25 = []

    model.save("LargeNoKoModel" + str(i+28) + ".h5")
