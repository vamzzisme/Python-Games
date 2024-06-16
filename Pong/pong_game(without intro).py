import turtle as t
import winsound as ws

screen = t.Screen()
screen.title("Tennis pong") 
screen.bgcolor("white")
screen.setup(width = 800, height = 600)
screen.tracer(0)
screen.title("Ping-Pong Game")

# Score
score_a = 0
score_b = 0

# pad left
paddle_left = t.Turtle()
paddle_left.speed(0)
paddle_left.shape("square")                      # by default 20x20
paddle_left.color("red")
paddle_left.shapesize(stretch_wid = 5, stretch_len = 1)
paddle_left.penup()
paddle_left.goto(-350, 0)

# pad right
paddle_right = t.Turtle()
paddle_right.speed(0)
paddle_right.shape("square")                      # by default 20x20
paddle_right.color("blue")
paddle_right.shapesize(stretch_wid = 5, stretch_len = 1)
paddle_right.penup()
paddle_right.goto(350, 0)

# ball
ball = t.Turtle()
ball.speed(0)
ball.shape("circle")                      # by default 20x20
ball.color("white")
ball.penup()
ball.goto(0, 0)
ball.dx = 0.8                 # move by 0.2 pixels in x
ball.dy = -0.8        # move by 0.2 pixels in y

# write
pen = t.Turtle()
pen.speed(0)
pen.color("white")
pen.penup()
pen.hideturtle()   # hide the pen icon
pen.goto(0, 260)
pen.write("Player A: 0  Player B: 0", align = "center", font = ("Courier", 24, "normal"))

# movements
def paddle_left_up():
	y = paddle_left.ycor()         # get the current y-coordinate
	y += 20                      # increase the ycor by 20
	paddle_left.sety(y)      # setting ycor() to new cor
			
screen.listen()                                 # catches events
screen.onkeypress(paddle_left_up, "w")          # if pressed 'w' call paddle_left_up	
	
def paddle_right_up():
	y = paddle_right.ycor()         # get the current y-coordinate
	y += 20                      # increase the ycor by 20
	paddle_right.sety(y)      # setting ycor() to new cor
		
screen.listen()                                 # catches events
screen.onkeypress(paddle_right_up, "Up")          # if pressed 'w' call paddle_left_up

def paddle_left_down():
	y = paddle_left.ycor()         # get the current y-coordinate
	y -= 20                      # increse the ycor by 20
	paddle_left.sety(y)      # setting ycor() to new cor

screen.listen()                                 # catches events
screen.onkeypress(paddle_left_down, "s")          # if pressed 'w' call paddle_left_up

def paddle_right_down():
	y = paddle_right.ycor()         # get the current y-coordinate
	y -= 20                      # increse the ycor by 20
	paddle_right.sety(y)      # setting ycor() to new cor
	
screen.listen()                                 # catches events
screen.onkeypress(paddle_right_down, "Down")          # if pressed 'w' call paddle_left_up

def pause():
	screen.delay(6000)
	
# gameLoop
game_run = True
while game_run:
	
	screen.update() 
	screen.bgpic("bg.png")
	# movement of ball
	ball.setx(ball.xcor() + ball.dx)
	ball.sety(ball.ycor() + ball.dy)
	
	# boundary of the ball
	if ball.ycor() > 290:     # check if top is crossed
		ball.sety(290)     # keep at that place
		ball.dy *= -1   # reverse the direction
		
	if ball.ycor() < -290:     # check if bottom is crossed
		ball.sety(-290)     # keep at that place
		ball.dy *= -1   # reverse the direction

	if ball.xcor() > 390:     # check if right is crossed
		ball.goto(0, 0)     # goto centre
		ball.dx *= -1   # reverse the direction
		score_a += 1
		pen.clear()  # clears the before one before printing new score
		pen.write("Player A: {}  Player B: {}".format(score_a, score_b), align = "center", font = ("Courier", 24, "normal"))
			
	if ball.xcor() < -390:     # check if left is crossed
		ball.goto(0, 0)     # goto centre
		ball.dx *= -1   # reverse the direction
		score_b += 1
		pen.clear()    # clears the before one before printing new score
		pen.write("Player A: {}  Player B: {}".format(score_a, score_b), align = "center", font = ("Courier", 24, "normal"))
		
	# collision?
	if ball.xcor() > 330 and ball.xcor() < 340 and ball.ycor() < paddle_right.ycor() + 70 and ball.ycor() > paddle_right.ycor() - 70:
		ball.setx(330)
		ball.dx *= -1
		ws.PlaySound("bounce.wav", ws.SND_ASYNC)      # -->A_SYNC to play in background		
		
	if ball.xcor() < -330 and ball.xcor() > -340 and ball.ycor() < paddle_left.ycor() + 70 and ball.ycor() > paddle_left.ycor() - 70:
		ball.setx(-330)
		ball.dx *= -1
		ws.PlaySound("bounce.wav", ws.SND_ASYNC)      # -->A_SYNC to play in background
