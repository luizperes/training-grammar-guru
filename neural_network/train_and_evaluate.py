# Based on https://csil-git1.cs.surrey.sfu.ca/lperesde/nlpclass-1777-pixel/blob/master/evaluator/tmosharr/deep_learning.py
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


def create_model():
    model = Sequential()
    model.add(Dense(16, input_dim=31, activation='relu')) # Hidden layer.
    model.add(Dense(3, activation='softmax' )) # Output layer.
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model

# Seed for RNG. Doesn't seem to be used anywhere.
seed = 7
np.random.seed(seed)

# print('Extracting data from files..')
dftrain = pd.read_csv('feat_train.csv')
dftest = pd.read_csv('feat_test.csv')
dataset_train = dftrain.values
dataset_test = dftest.values

# print('Preparing data..')
# Split into input and target data sets for training.
X_train = dataset_train[:, 0:31].astype(float)
Y_train = dataset_train[:, 31].astype(int)
# Prepare test data.
X_test = dataset_test[:, :].astype(float)

# Map training targets to labels.
cat_y= []
for y in Y_train:
    if y==1:
        cat_y.append('better')
    elif y==0:
        cat_y.append('same')
    else:
        cat_y.append('worse')

# Transform labels into a normalized encoding.
encoder = LabelEncoder()
encoder.fit(cat_y)
encoded_Y = encoder.transform(cat_y)
dummy_y = np_utils.to_categorical(encoded_Y)

# Create and train model.
# print('Creating base model..')
model = create_model()

# print('Training model..')
model.fit(X_train, dummy_y, epochs=50, batch_size= 100, verbose=False)

# Evaluate the model.
# print('Evaluating model..')
predictions = model.predict(X_test)
for prediction in predictions:
    # Initialize best index and score.
    best_index = -1
    best_score = -1

    # Look for the actual best index and score in the current prediction.
    for index in range(len(prediction)):
        if prediction[index] > best_score:
            best_score = prediction[index]
            best_index = index

    # Print the best index.
    if best_index == 0:
        print(1)
    elif best_index == 1:
        print(0)
    else:
        print(-1)

# Record model weights in .h5 file.
# https://stackoverflow.com/questions/47266383/save-and-load-weights-in-keras
# print('Saving model..')
model.save_weights('nn_weights.h5')
# print('Done! Bye!')
