import numpy as np 
import random
from Learn_Pong import Obj, Ball, Game
import tensorflow as tf
from tensorflow import keras
import pandas as pd
import matplotlib.pyplot as plt
import pickle
import json
import time

#Desktop="/Users/QTD0277/Desktop/"
Desktop=""
Save_file="Pong_logs/g_logs_1.pkl"
Save_models="Models/Test_Model"
Save_var= "Models/var.json"
X=[]
y=[]
X2=[]
y2=[]

def pickle_load(filename):
	"loads data from a desktop pickle file. returns the data"
	with open(Desktop+filename,'rb') as f:  # Python 3: open(..., 'rb')
	    loaded = pickle.load(f)
	    print("loaded data from: ",filename)
	return loaded

#data=pickle_load(Save_file)

def relu(h):
	print(h<0)
	return h[h<0]
def build_model():
	'''Creates the Structure of a model with 3 layers. 64 parameter input and 1 output'''
	print("building model")
	model = keras.Sequential([
	keras.layers.Dense(64, activation=tf.nn.relu, 
	                   input_shape=(X.shape[1],)),
	keras.layers.Dense(64, activation=tf.nn.relu),
	keras.layers.Dense(1,activation=tf.nn.sigmoid)
	])

	optimizer = tf.train.AdamOptimizer()

	model.compile(loss='binary_crossentropy',
	            optimizer=optimizer,
	            metrics=['accuracy'])
	return model
def plot_history(history):
	'''helper fucntion for plotting results of model. 
	Training loss: Error of Training Data Predictions
	Validation loss: Error of Testing Data Predictions (Post training.. aka Validation Data)'''
	plt.figure()
	plt.xlabel('Epoch')
	plt.ylabel('Error ')
	print(np.array(history.history))
	plt.plot(history.epoch, np.array(history.history['loss']), 
	       label='Train Loss')
	plt.plot(history.epoch, np.array(history.history['val_loss']),
	       label = 'Val loss')
	plt.legend()
	plt.show()

def parse_data():
	global X,X2,y,y2
	data = pickle_load(Save_file)
	num_games = len(data)
	val_ratio = .2
	for counter in range(num_games):
		for step in range(len(data[counter][0])):
			if counter > val_ratio*num_games:
				X2.append(data[counter][0][step]); y2.append(data[counter][1][step])
			else:
				X.append(data[counter][0][step]); y.append(data[counter][1][step])
	## convert into array
	X=np.array(X)
	y=np.array(y)
	X2=np.array(X2)
	y2=np.array(y2)


	### normalize
	print("normalizing")
	mean = X.mean(axis=0)
	std = X.std(axis=0)
	X = (X - mean) / std
	X2=(X2-mean)/std
	var_store={"mean": mean.tolist(),
			   "std" : std.tolist() }
	var_store=json.dumps(var_store)
	with open(Desktop+Save_var, "w") as json_file:
	    json_file.write(var_store)

def save_model():
	model_json = model.to_json()
	with open(Desktop+Save_models+".json", "w") as json_file:
	    json_file.write(model_json)
	# serialize weights to HDF5
	model.save_weights(Desktop+Save_models+".h5")
def run_training():
	######## RUN Training and Testing(Validation) with model and visualize #########
	EPOCHS = 50
	early_stop = keras.callbacks.EarlyStopping(monitor='val_loss', patience=100)

	history = model.fit(X, y, epochs=EPOCHS,
	                    validation_split=0.2, verbose=0,
	                    callbacks=[early_stop])
	plot_history(history)
	[loss, mae] = model.evaluate(X2, y2, verbose=0)
	print("Testing set Mean Abs Error: ${:7.2f}".format(mae))
time_stamp=time.time()
parse_data()
model = build_model()
model.summary()
run_training()
print("Time taken= ",time.time()-time_stamp)
save_model()

##################################################################
