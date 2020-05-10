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
        1
        , use_bias=False
        , kernel_regularizer=regularizers.l2(0.0001)
        , name=name
    )(x)

    return (x)


def build_model():
    main_input = Input(shape=(24, 19, 19), name='main_input')

    x = conv_layer(main_input, 92, 5, 'linear')

    for h in range(3):
        x = conv_layer(x, 384, 3, 'relu')

    V = conv_layer(x, 1, 3, 'linear')

    V = softmax(V, "v")

    model = Model(inputs=[main_input], outputs=[V])

    model.compile(loss='mean_squared_error', optimizer='adam', metrics=['categorical_accuracy'])
    return model


def readData(modelInput):
    TrainingStates = []
    vTruth=[]

    for data in modelInput:
        TrainingStates.append(data[0])
        vTruth.append(data[2])

    vTruth = np.asarray(vTruth)
    TrainingStates = np.asarray(TrainingStates)
    return TrainingStates, vTruth


model = build_model()
#model = load_model('ValueNoKoModel1.h5')


modelInput1 = pk.load(open("VtrainigData/NoKoTrainingData_1200.pkl", 'rb'))
modelInput2 = pk.load(open("VtrainigData/NoKoTrainingData_1500.pkl", 'rb'))
modelInput3 = pk.load(open("VtrainigData/NoKoTrainingData_1800.pkl", 'rb'))
modelInput4 = pk.load(open("VtrainigData/NoKoTrainingData_2100.pkl", 'rb'))
modelInput5 = pk.load(open("VtrainigData/NoKoTrainingData_2400.pkl.", 'rb'))
modelInput6 = pk.load(open("VtrainigData/NoKoTrainingData_2700.pkl", 'rb'))
#modelInput7 = pk.load(open("VtrainigData/NoKoTrainingData_3000.pkl", 'rb'))
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

modelInput = np.concatenate((modelInput1, modelInput2, modelInput3, modelInput4, modelInput5, modelInput6
                             ), axis=0)
del modelInput1
del modelInput2
del modelInput3
del modelInput4
del modelInput5
del modelInput6

#MI=[modelInput1, modelInput2,modelInput3]


TrainingStatesT, TruthT = readData(modelInput)

model.fit(TrainingStatesT[3:], TruthT[3:], epochs=40, batch_size=256, shuffle=True, verbose=2, validation_split=.01)
model.save("ValueNoKoModel12.h5")

pred = model.predict(np.asarray([TrainingStatesT[0]]))
pred2 = model.predict(np.asarray([TrainingStatesT[2]]))
pred3 = model.predict(np.asarray([TrainingStatesT[1]]))

print(pred)
print(pred2)
print(pred3)



