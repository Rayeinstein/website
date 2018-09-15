import pickle 
import random
from Learn_Pong import Game,Obj,Ball,sign
#Desktop="/Users/QTD0277/Desktop/"
Desktop=""
Save_file="Pong_logs/g_logs_1.pkl"

def pickle_save(filename,item):
	"saves data to a pickle file located on the desktop"
	with open(Desktop+filename,'wb') as f:  # Python 3: open(..., 'rb')
	    pickle.dump(item, f)# Save a dictionary into a pickle file.
	    print("data saved to ",filename)
def pickle_load(filename):
	"loads data from a desktop pickle file. returns the data"
	with open(Desktop+filename,'rb') as f:  # Python 3: open(..., 'rb')
	    loaded = pickle.load(f)
	    print("loaded data from: ",filename)
	return loaded

def get_parameters(game):
	m1=game.p1.move;m2=game.p2.move;
	p1_prev_move=1 if m1=="up" else -1 if m1=="down" else 0
	p2_prev_move=1 if m2=="up" else -1 if m2=="down" else 0
	ballc=int(game.ball.c);ballr=int(game.ball.r);ballvr=int(game.ball.vr);ballvc=int(game.ball.vc)
	p1_pos=int(game.p1.r);p2_pos=int(game.p2.r)
	return [p1_prev_move,p2_prev_move,ballc,ballr,ballvr,ballvc,p1_pos,p2_pos]



all_logs=[]
count=0

while count < 50000:
	g_log=[[],[]]
	g=Game()
	while g.state == "ongoing":

		g_log[0].append(get_parameters(g))
		## ALGORITHYM
		ball_pos=g.ball.r
		ball_vel=g.ball.vr
		p1_pos=g.p1.r
		if ball_vel > 0:
			m1 = random.choice(("up","down","down","down"))
		else:
			m1 = random.choice(("down","up", "up","up"))

		'''## Random Choice
		m1=random.choice(("up","down"))'''
		#Algorythym

		m2=random.choice(("up","down"))
		g.step(p1_move=m1,p2_move=m2)
		if m1=="up":
			m1=1
		else:
			m1=0
		g_log[1].append(m1)

		## if notable eevnt happens, update g_log and reset 
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

pickle_save(Save_file,all_logs)

