import numpy as np
import pandas as pd
from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasClassifier
from keras.utils import np_utils
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.preprocessing import LabelEncoder
from sklearn.pipeline import Pipeline

def baseline_model():
    model = Sequential()
    model.add(Dense(8, input_dim=4, activation='relu'))
    model.add(Dense(3, activation='softmax', ))
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model

seed = 7
np.random.seed(seed)

dftrain = pd.read_csv('feature_values.csv')
dataset_train = dftrain.values
X_train = dataset_train[:, 0:27].astype(float)
Y_train = dataset_train[:, 27].astype(int)

cat_y= []
for y in Y_train:
    if y==1:
        cat_y.append('better')
    elif y==0:
        cat_y.append('same')
    else:
        cat_y.append('worse')

encoder = LabelEncoder()
encoder.fit(cat_y)
encoded_Y = encoder.transform(cat_y)
dummy_y = np_utils.to_categorical(encoded_Y)

model = Sequential()
model.add(Dense(8, input_dim=27, activation='relu'))
model.add(Dense(3, activation='softmax' ))
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

model.fit(X_train, dummy_y, epochs=30, batch_size= 100, verbose=False)
model.save('wow')