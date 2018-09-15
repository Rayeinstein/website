import tensorflow as tf 
from tensorflow import keras
from tensorflow.keras.models import model_from_json
from Learn_Pong import Game,Obj,Ball,sign
from Pong_data import get_parameters
import h5py
import random
import json
import numpy as np 
from pynput import keyboard

#Desktop="/Users/QTD0277/Desktop/"
Desktop=""
Save_file="Pong_logs/g_logs_1.pkl"
Save_models="Models/Test_Model"
Save_var= "Models/var.json"

def load_model():
	# load json and create model
	json_file = open(Desktop+Save_models+".json", 'r')
	loaded_model_json = json_file.read()
	json_file.close()
	loaded_model = model_from_json(loaded_model_json)
	# load weights into new model
	loaded_model.load_weights(Desktop+Save_models+".h5")
	print("Loaded model from disk")
	return loaded_model

def play(game):
	test_data = get_parameters(game)
	test_data = np.array(test_data)
	test_data = (test_data - means) / stds
	m1 = model.predict(np.array([test_data]))[0][0]
	param=random.uniform(0,1)
	#print(m1,param)
	if param < m1:
		m1="up"
	else:
		m1="down"
	game.step(p1_move=m1,p2_move=m2)
	#print("m1: ",m1)
	#print("score: ", score)
	#print(game)
def play_alg(game):
	ball_pos=g.ball.r
	p1_pos=g.p1.r
	ball_vel=g.ball.vr
	#if p1_pos < ball_pos:
	if ball_vel > 0:
		m1=random.choice(("up","down","down","down"))
	else:
		m1=random.choice(("up","up","up","down"))
	game.step(p1_move=m1,p2_move=m2)

def play_rand(game):
	m1=random.choice(("up","down"))
	game.step(p1_move=m1,p2_move=m2)

# obtain variables and model + parse it
def obtain_vars():
	global means,stds
	print("read json data")
	json_data = open(Save_var).read()
	data = json.loads(json_data)
	print("calculating means/ std")
	means = np.array(data["mean"])
	stds = np.array(data['std'])

obtain_vars()
print("loading model")
model=load_model()
print("starting game")

def to_run():
	# initialize game and play
	g=Game()
	score=0
	total_games=0
	while total_games<1000:
		#m2 = input("P2_move: ")
		m2 = random.choice(("up","down"))
		if g.state == "victory":
			score-=1

		if g.state == "defeat":
			score +=1
		if g.state != "ongoing":
			total_games+=1
			g=Game()
		play(g)
	print(score,total_games)
	return ("Score: ",score)
to_run()
