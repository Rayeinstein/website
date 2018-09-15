import numpy as np
import random
import time
from pynput import keyboard
from os import system


def sign(n):
    n=float(n)
    if n >= 0.0:
        return 1.0
    else:
        return -1.0

class Obj():
    def __init__(self,pos,length):
        self.move=[]
        self.r=pos[0]
        self.c=pos[1]
        self.len=length
class Ball(Obj):
    def __init__(self,pos,length,vel):
        super().__init__(pos,length)
        self.vr=vel[0]
        self.vc=vel[1]
class Game():
    def __init__(self,p1_pos=None,p2_pos=None,p_len=3,rows=16,cols=100,b_pos=None,b_vel=None,state="ongoing"):
        # make players and balls
        if b_vel==None:
            b_vel=[float(random.choice((-1,1))*(.3+random.uniform(1,2))),float(random.choice((-1,1))*(.5+random.uniform(1,3)))]
        if b_pos==None:
            u=2
            v=20
            b_pos= [float(random.randint(u,rows-u)),float(random.randint(v,cols-v))]
            
        if p1_pos==None:
            wd=3;ht=5
            p1_pos=[ht,wd]
            p2_pos=[ht,cols-wd]
        self.p1=Obj(p1_pos,p_len)
        self.p2=Obj(p2_pos,p_len)
        self.ball =Ball(b_pos,1,b_vel)
        self.state = state
        self.rows  = rows
        self.cols  = cols
        self.event = None
        self.update_board()
        #self.board = board



    def step(self,p1_move=None,p2_move=None):
        self.event = None
        if self.state != "ongoing":
            return None
        self.p1.move=p1_move
        self.p2.move=p2_move
        
        ## ball moves ##
        next_r = self.ball.r + self.ball.vr
        next_c = self.ball.c + self.ball.vc

        ## player moves and calc collisions
        for player in (self.p1,self.p2):
            if player.move == "up" and player.r != 0:
                player.r-=1
            elif player.move == "down" and player.r != (self.rows-player.len):
                player.r+=1
            else:
                pass

            collision_y = (float(self.ball.vr)/float(self.ball.vc))*(player.c-self.ball.c)
            collision_y+=self.ball.r
            D_b2p=player.c-self.ball.c#X Distance_ball_to_player
            if sign(D_b2p)==sign(self.ball.vc) and abs(self.ball.vc) >= abs(D_b2p):

                if player.r+player.len >= collision_y and collision_y >= player.r:

                    self.ball.vc = - self.ball.vc
                    next_c=player.c + sign(self.ball.vc)
                    ## accelerate ball:
                    if player.move=="up":
                        self.ball.vr -=1
                    elif player.move=="down":
                        self.ball.vr +=1
                    ## set event ##
                    if player == self.p1:
                        self.event = "p1" 
                    elif player == self.p2:
                        self.event = "p2"



        ##### BALLS Wall collisions ##
        next_r=round(next_r)
        next_c=round(next_c)

        if next_r <=0:
            self.ball.vr=-self.ball.vr
            next_r=0.0
        if next_r >= self.rows:
            self.ball.vr=-self.ball.vr
            next_r=self.rows-1

        # CHECK VICTORY
        # keep in bounds  
        if next_c <= 0:
            self.ball.vc=-self.ball.vc
            next_c=0.0
            self.state="victory"
            self.event = "victory"
        if next_c >= self.cols:
            self.ball.vc=-self.ball.vc
            next_c=self.cols-1
            self.state= "defeat"
            self.event = "defeat"
        ## BAll Next pos
        self.ball.r = next_r
        self.ball.c = next_c

        self.update_board()

    def update_board(self):
        if self.state != "ongoing":
            return None
        else:
            board=[[0]*(self.cols+1) for i in range(self.rows)]
            # plpace players in their place
            for r in range(0,self.p1.len):
                board[self.p1.r + r][self.p1.c] = "|"
                board[self.p2.r + r][self.p2.c] = "|"
            # place ball
            board[round(self.ball.r)][round(self.ball.c)] = "O"
            self.board=board

    def __str__(self):

        result="0"*(self.cols+3)+"\n"
        for i in self.board:
            result+="|"
            for ind in i:
                if ind == 0:
                    result+=" "
                else:
                    result += str(ind)

            result += "|\n"
        result +="0"*(self.cols+3)+"\n"
        if self.state== "victory":
            result += "victory"
        elif self.state=="defeat":
            result += "defeat"
        return result
'''
# reliable random vs algorythm
g=Game()
while True:
    m1=random.choice(("up","down"));m2=None
    m2=input("P2_move: ")
    if m2 == "new game":
        g=Game()
    else:
        if m2== "u":
            m2= "up"
        elif m2== "d":
            m2 = "down"
        g.step(p1_move=m1,p2_move=m2)
        print(g)
        print(g.ball.r,g.ball.c,g.ball.vr,g.ball.vc)
'''
'''
# algorythym vs random
g=Game()
count=0
total_games=0
while total_games<1000:
    #m2 move
    m2=random.choice(("up","down"))
    #m1 move
    ## use position
    ball_pos=g.ball.r
    p1_pos=g.p1.r
    if p1_pos < ball_pos:
        m1=random.choice(("up","down","down","down"))
    else:
        m1=random.choice(("up","up","up","down"))
    ## use vel
    ball_vel=g.ball.vr
    if ball_vel > 0:
        m1=random.choice(("up","down","down","down"))
    else:
        m1=random.choice(("up","up","up","down"))
    ## input #
    #input("press to step")
    if g.state != "ongoing":
        total_games+=1
        if g.state == "victory":
            count -=1
        else:
            count +=1
        g=Game()
    else:
        g.step(p1_move=m1,p2_move=m2)
        #print(g.ball.r,g.ball.c,g.ball.vr,g.ball.vc)
        #print("P1 score: ", count)
        #print(g)
print(count,total_games)'''



'''
## keyboard ##
Listener(on_press=on_press)
def on_press(key):
    global m1, m2

    #m1=random.choice(("up","down"));m2=None

    if key == keyboard.Key.up:
        m2="up"
    elif key == keyboard.Key.down:
        m2="down"
    elif key == keyboard.Key.w:
        m1="up"
    elif key == keyboard.Key.s:
        m1="down"

def on_release(key):
    if key == keyboard.Key.esc:
        # Stop listener
        return False
g=Game()
lis=keyboard.Listener(
        on_press=on_press,
        on_release=on_release)
while True:
    
    m1=None;m2=None
    lis=keyboard.Listener(
        on_press=on_press,
        on_release=on_release)
    lis.start()
    time.sleep(.1)
    lis.stop()
    g.step(p1_move=m1,p2_move=m2)
    system('cls')
    print(g)
'''


'''

# Collect events until released
kb=keyboard.Controller()
with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()'''





'''
X=input
X=np.dot(W1,X) # compute hidden layer neuron activations
X=relu(X)   # ReLU nonlinearity: threshold at zero
X=np.dot(W2,X)
p=sigmoid(X)
def sigmoid(arg):
    return 1.0/(1.0+np.exp(-arg))

'''