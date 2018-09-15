import numpy as np 
import random
from tensorflow.keras.models import model_from_json

from Learn_Pong import Game,Obj,Ball,sign
from Pong_data import get_parameters,pickle_save,pickle_load
from Pong_Model import relu, parse_data, save_model, run_training
from Run_pong_model import load_model,obtain_vars

import h5py
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

#
all_results=[]

# 1. load model
obtain_vars()
print("loading model")
model=load_model()
means = 0
g = Game()
stds = 0
all_logs=[]
g_log=[[],[]]
m1 = None; m2 = None
score = 0

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

def play(game):
	test_data = get_parameters(game)
	test_data = np.array(test_data)
	test_data = (test_data - means) / stds
	m1 = model.predict(np.array([test_data]))[0][0]
	param = random.uniform(0,1)
	#print(m1,param)
	if param < m1:
		m1="up"
	else:
		m1="down"
	game.step(p1_move=m1,p2_move=m2)

def repeat_trainings(num_train):
	global m1, m2
	count=0
	while count < num_train:
		print("start training num: ",count)
		count+=1
		# PLay games & get data play_5k_games():
		print("collecting data")
		play_5k_games_w_AI()
		# Save data
		# OK

		# Use gathered data and train model.
		print("running training")
		parse_data(save=False)
		run_training(plot = False)

		# Save model
		save_model()

		# run tests and print scores
		print("running tests")
		obtain_vars()
		result = to_run()
		all_results.append(result)

def play_5k_games_w_AI():
	all_logs=[]
	score=0
	total_games=0
	while total_games<1000:
		g_log=[[],[]]
		g=Game()
		total_games+=1
		while g.state  == "ongoing":
			#get_params
			params = get_parameters(g)
			g_log[0].append(params)

			#m1 decide
			m1 = None
			p1_decide(params)

			#m2 decide
			m2 = None
			m2 = random.choice(("up","down"))

			#move 
			g.step(p1_move=m1,p2_move=m2)

			#score
			update_scores()

			# label data
			positive_reinf()

		print(score,total_games)

	pickle_save(Save_file,all_logs)

def positive_reinf():
	if g.event =="p1":
		num_data=10
		if len(g_log[0]) > num_data:
			recent_relevent_logs = g_log[0][-num_data:]
			recent_relevent_acts = g_log[1][-num_data:]
			if g.event == "victory":
				recent_relevent_acts = [(0+(.5*(1/(i+1)))) if recent_relevent_acts[i]==1 else (1-(.5*(1/(i+1)))) for i in range(len(recent_relevent_acts))]
			else:
				recent_relevent_acts = [(0+(.5*(1/(1+i)))) if recent_relevent_acts[i]==0 else (1-(.5*(1/(1+i)))) for i in range(len(recent_relevent_acts))]
			all_logs.append([recent_relevent_logs,recent_relevent_acts])
			count+=1
		g_log=[[],[]]

def p1_decide(params):

	test_data = params.copy()
	test_data = np.array(test_data)
	test_data = (test_data - means) / stds
	m1 = model.predict(np.array([test_data]))[0][0]
	param=random.uniform(0,1)
	if param < m1:
		m1="up"
		g_log[1].append(1)
	else:
		m1="down"
		g_log[1].append(0)

def update_scores():
	global g, score
	if g.state == "victory":
		score-=1
	if g.state == "defeat":
		score +=1
	
repeat_trainings(20)