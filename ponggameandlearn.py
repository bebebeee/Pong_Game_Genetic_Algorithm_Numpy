print('k')
import turtle
import random
import numpy as np
window = turtle.Screen()
window.setup(width=800, height=600)
window.tracer(0)
class aipaddleright(turtle.Turtle): #this will make a ai paddle
    def __init__(self,*args,**kwargs):
        super(aipaddleright,self).__init__(*args,**kwargs)
        self.speed(0)
        self.shape("square")
        self.color("green")
        self.shapesize(stretch_wid=5, stretch_len=1)
        self.penup()
        self.goto(350,0) #defalut place starting
        self.offlineq =False
        self.fitness=0
        self.speed(speed=0)
        #my neral networkk
        self.array1as = 2*np.random.random((5,7))-1
        self.array3as = 2*np.random.random((7,3))-1
    def dissappear(self):
        self.hideturtle()
        self.offlineq=True
    def usebraintomove(self,ballpos): #ballpos will give [[xspeed,yspeed],[x2,y2]]
        inputlayer = np.array([ballpos[0][0]*1.5,ballpos[0][1]*1.5,ballpos[1][0]/400,ballpos[1][1]/300,self.ycor()/300])
        after1stlayer = self.sigmoid(np.dot(inputlayer,self.array1as))
        finalresults = np.dot(after1stlayer,self.array3as)
        finalresults = self.softmax(finalresults)
        return finalresults

    def sigmoid(self,x):

        return np.maximum(0,x)


    def softmax(self,x):
        return np.exp(x) / np.sum(np.exp(x), axis=0)


    def upkey(self):
        y=self.ycor()
        y=y+10
        self.sety(y)
        if self.ycor()>300:
            self.sety(y-10)

    def downkey(self):
        y=self.ycor()
        y=y-10
        self.sety(y)
        if self.ycor()<-300:
            self.sety(y+10)

#robott paddle
leftpaddle = turtle.Turtle()
leftpaddle.speed(0)
leftpaddle.shape("square")
leftpaddle.color("green")
leftpaddle.shapesize(stretch_wid=200, stretch_len=1)
leftpaddle.penup()
leftpaddle.goto(-365,0)
#funcitons to move this
def godownleft():
    leftpaddle.sety(leftpaddle.ycor()-40)
def goupleft():
    leftpaddle.sety(leftpaddle.ycor()+40)

#the ball
ball = turtle.Turtle()
ball.speed(0)
ball.shape("circle")
ball.color("red")
ball.penup()
ball.goto(200,0)
ballxdirection=random.uniform(-0.6,-1.4)
if (random.randint(0,10000) % 2):
    ballydirection=random.uniform(-0.6,-1.4)
else:
    ballydirection=random.uniform(0.6,1.4)


#generate ais
aidictionary = {}
neuralnetworksforeach = {}
for ai in range(100):
    aidictionary[ai]=aipaddleright()


aidictionary[0].upkey()
aidictionary[2].downkey()
#scores
player_1_score = 0
player_2_score = 0
#Pen for the scores
pen = turtle.Turtle()
pen.speed(0)
pen.color("black")
pen.penup()
pen.hideturtle()
pen.goto(0,260)
pen.write("Player 1: 0 Player 2: 0, largest fitness is: 0", align = "center", font = ("Courier", 24, "normal"))


savedthisturnkilled = []

def findclosestperson(listofpeople,ballycor):
    closestpy = 100000
    closestperson = None
    for person in listofpeople:
        if np.absolute(ballycor-person.ycor())<closestpy:
            closestpy = np.absolute(ballycor-person.ycor())
            closestperson = person

    return closestperson

def ontonextround():
    print('ss')

multiplyratio = 7

window.listen()
window.onkey(goupleft,'w')
window.onkey(godownleft,'s')
while True: #main game loop
    #move ball

    ball.sety(multiplyratio*ballydirection+ball.ycor())
    ball.setx(multiplyratio*ballxdirection+ball.xcor())
    #hit top or bottom walls THIS SECTION IS DEALING WITH WHERE THE BALL HITS, LIKE LOSING OR BOUNCING
    if ball.ycor() > 290 or ball.ycor()<-290:
        ballydirection = 0-ballydirection
    #hit left me paddle, not ai
    if ((ball.ycor() > ((leftpaddle.ycor()-500)) and (ball.ycor() < (leftpaddle.ycor()+500)))  and  (ball.xcor()>(leftpaddle.xcor()-10) and (ball.xcor()<leftpaddle.xcor()+10))):
        ballxdirection = 0-ballxdirection
    #hit ai paddles loop
    savedxdirection = ballxdirection
    needtokill = []
    for playerkey in aidictionary:

        #actually moving
        probs = aidictionary[playerkey].usebraintomove([[ballxdirection,ballydirection],[ball.xcor(),ball.ycor()]])
        whatweget = random.uniform(0,1)
        if whatweget>=0 and whatweget<=probs[0]:
            aidictionary[playerkey].upkey()
        if whatweget>probs[0] and whatweget<=probs[1]:
            aidictionary[playerkey].downkey()

        #bouncing off paddles
        if ((ball.ycor() > ((aidictionary[playerkey].ycor()-50)) and (ball.ycor() < (aidictionary[playerkey].ycor()+50)))  and  (ball.xcor()>(aidictionary[playerkey].xcor()-10) and (ball.xcor()<aidictionary[playerkey].xcor()+10))):
            if ballxdirection == savedxdirection:
                if aidictionary[playerkey].offlineq == False:
                    ballxdirection = 0-ballxdirection
            aidictionary[playerkey].fitness += 1
            if aidictionary[playerkey].fitness >= 50: # if running for way to long
                needtokill.append(playerkey)
        else:
            if ball.xcor() >= 340:
                needtokill.append(playerkey)


    for kills in needtokill:
        savedthisturnkilled.append(aidictionary[kills])
        aidictionary[kills].dissappear()


        del aidictionary[kills]
        if len(aidictionary) == 0: #if everyone dies
            #leaderboard
            player_1_score = player_1_score+1
            pen.clear()
            pen.write("Player 1: {} Player 2: {}".format(player_1_score, player_2_score), align = "center", font = ("Courier", 24, "normal"))

            nearestpersontotarget = findclosestperson(savedthisturnkilled,ball.ycor())
            hisbrainsaved = [nearestpersontotarget.array1as,nearestpersontotarget.array3as]
            fitnessthis = nearestpersontotarget.fitness

            multiplyratio += 0

            for ai in range(150):#regenerate players
                aidictionary[ai]=aipaddleright()
                #mutatetion
                mutateRa=0.18 #mutation rate change to change

                if ai < 100:
                    mutaterRa = 0.08
                if ai < 25:
                    mutateRa=0.04 #mutation rate change to change

                if ai == 0:
                    mutateRa=0 #mutation rate change to change
                mutatefir = mutateRa*np.random.random((5,7))-mutateRa/2 #mutateing for new brains
                mutatemid = mutateRa*np.random.random((7,3))-mutateRa/2 #FIX FOR LATER -- when randomly mutate, only select
                #apply and run
                aidictionary[ai].array1as = np.add(hisbrainsaved[0],mutatefir)
                aidictionary[ai].array3as = np.add(hisbrainsaved[1],mutatemid)
            print(str(hisbrainsaved))
            ball.sety(0) #reset balls
            ball.setx(0)
            ballxdirection=random.uniform(-0.6,-1.4) #reset ball directions
            if (random.randint(0,10000) % 2):
                ballydirection=random.uniform(-0.6,-1.4)
            else:
                ballydirection=random.uniform(0.6,1.4)

            print('i lost but my fitness was: '+ str(fitnessthis))


    savedthisturnkilled = []



    #hit left side someone loses
    if (ball.xcor() < -399):
        ball.sety(0)
        ball.setx(0)
        player_2_score = player_2_score+1
        pen.clear()
        pen.write("Player 1: {} Player 2: {}".format(player_1_score, player_2_score), align = "center", font = ("Courier", 24, "normal"))
        ballxdirection=random.uniform(-0.6,-1.4) #reset ball directions
        if (random.randint(0,10000) % 2):
            ballydirection=random.uniform(-0.6,-1.4)
        else:
            ballydirection=random.uniform(0.6,1.4)
    #hit right side someone loses
    if (ball.xcor() > 350): #AI LOSE
        ball.sety(0)
        ball.setx(0)
        player_1_score = player_1_score+1
        pen.clear()
        pen.write("Player 1: {} Player 2: {}".format(player_1_score, player_2_score), align = "center", font = ("Courier", 24, "normal"))
        ballxdirection=random.uniform(-0.6,-1.4) #reset ball direction so it is fun
        if (random.randint(0,10000) % 2):
            ballydirection=random.uniform(-0.6,-1.4)
        else:
            ballydirection=random.uniform(0.6,1.4)


    #let players move
    #left paddle robot just follow
    #if ball.ycor() > leftpaddle.ycor():
    #    goupleft()
    #if ball.ycor() < leftpaddle.ycor():
    #    godownleft()

    #last ball where
    window.update()
window.mainloop()
