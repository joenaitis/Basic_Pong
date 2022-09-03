# Joe's version of 2-player Pong, done as a project for the online course
# "An Introduction to Interactive Programming in Python"

# To play the game, hit the run button
# Player 1 should use 'w' and 's' to move the left paddle up and down
# Player 2 should use 'up arrow' and 'down arrow' to move the right paddle up and down
# One point is awarded to a player if the opposing player misses
# Select 'Reset' to reset the game

import simpleguitk as simplegui
import random

# initialize globals - pos and vel, encode vertical info for paddles
WIDTH = 600
HEIGHT = 400
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
paddle1_pos = HEIGHT / 2
paddle2_pos = HEIGHT / 2
paddle1_vel = 0
paddle2_vel = 0

# initialize ball_pos and ball_vel for new bal in middle of table
ball_pos = [WIDTH / 2, HEIGHT / 2]
ball_vel = [1, 1]


# spawns new ball randomly choosing to go left or right
def spawn_ball():
    global ball_pos, ball_vel  # global variables that are vectors stored as lists
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    ball_vel = [-1, 1]

    # create random horizonal and vertical velocities
    horizontal_random = random.randrange(0, 2)
    vertical_random = random.randrange(0, 2)
    if horizontal_random == 0:
        ball_vel[0] = random.randrange(120, 240) / 60
    else:
        ball_vel[0] = -random.randrange(120, 240) / 60
    if vertical_random == 0:
        ball_vel[1] = random.randrange(60, 180) / 60
    else:
        ball_vel[1] = -random.randrange(60, 180) / 60


# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2
    score1 = 0
    score2 = 0
    spawn_ball()


# draws all components of canvas once every 60 seconds
def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel, paddle1_vel, paddle2_vel

    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0], [WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0], [PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0], [WIDTH - PAD_WIDTH, HEIGHT], 1, "White")

    # update ball position
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]

    # reflect off vertical walls
    if (ball_pos[1] <= BALL_RADIUS) or (ball_pos[1] >= (HEIGHT - BALL_RADIUS)):
        ball_vel[1] = -ball_vel[1]

    # test if ball touches gutter.  If yes, respawn ball
    if (ball_pos[0] <= (BALL_RADIUS + PAD_WIDTH)):
        if (ball_pos[1] <= (paddle1_pos + PAD_HEIGHT / 2)) and (ball_pos[1] >= (paddle1_pos - PAD_HEIGHT / 2)):
            ball_vel[0] = -ball_vel[0] * 1.1
        else:
            score2 += 1
            spawn_ball()

    if (ball_pos[0] >= (WIDTH - (BALL_RADIUS + PAD_WIDTH))):
        if (ball_pos[1] <= (paddle2_pos + PAD_HEIGHT / 2)) and (ball_pos[1] >= (paddle2_pos - PAD_HEIGHT / 2)):
            ball_vel[0] = -ball_vel[0] * 1.1
        else:
            score1 += 1
            spawn_ball()

    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 3.25, "White", "White")

    # update paddle's vertical position, keep paddle on the screen
    if ((paddle1_pos + paddle1_vel + PAD_HEIGHT / 2) > HEIGHT) or ((paddle1_pos + paddle1_vel - PAD_HEIGHT / 2) < 0):
        paddle1_pos = paddle1_pos
    else:
        paddle1_pos += paddle1_vel

    if ((paddle2_pos + paddle2_vel + PAD_HEIGHT / 2) > HEIGHT) or ((paddle2_pos + paddle2_vel - PAD_HEIGHT / 2) < 0):
        paddle2_pos = paddle2_pos
    else:
        paddle2_pos += paddle2_vel

    # draw paddles
    canvas.draw_polygon([[0, paddle1_pos - PAD_HEIGHT / 2], [PAD_WIDTH, paddle1_pos - PAD_HEIGHT / 2],
                         [PAD_WIDTH, paddle1_pos + PAD_HEIGHT / 2], [0, paddle1_pos + PAD_HEIGHT / 2]], 10, "White")
    canvas.draw_polygon([[WIDTH - PAD_WIDTH, paddle2_pos - PAD_HEIGHT / 2], [WIDTH, paddle2_pos - PAD_HEIGHT / 2],
                         [WIDTH, paddle2_pos + PAD_HEIGHT / 2], [WIDTH - PAD_WIDTH, paddle2_pos + PAD_HEIGHT / 2]], 10,
                        "White")

    # determine whether paddle and ball collide

    # draw scores
    canvas.draw_text(("Player 1"), (WIDTH / 2 - 73, 33), 13, "Teal")
    canvas.draw_text(("Score: " + str(score1)), (WIDTH / 2 - 73, 52), 13, "Teal")
    canvas.draw_text(("Player 2"), (WIDTH / 2 + 13, 33), 13, "Teal")
    canvas.draw_text(("Score: " + str(score2)), (WIDTH / 2 + 13, 52), 13, "Teal")


# actions that occur when a key is pressed
def keydown(key):
    global paddle1_vel, paddle2_vel
    if simplegui.KEY_MAP["w"] == key:
        paddle1_vel = -7.5
    if simplegui.KEY_MAP["s"] == key:
        paddle1_vel = 7.5
    if simplegui.KEY_MAP["up"] == key:
        paddle2_vel = -7.5
    if simplegui.KEY_MAP["down"] == key:
        paddle2_vel = 7.5


# actions that occur when a key is no longer pressed
def keyup(key):
    global paddle1_vel, paddle2_vel
    if simplegui.KEY_MAP["w"] == key:
        paddle1_vel = 0
    if simplegui.KEY_MAP["s"] == key:
        paddle1_vel = 0
    if simplegui.KEY_MAP["up"] == key:
        paddle2_vel = 0
    if simplegui.KEY_MAP["down"] == key:
        paddle2_vel = 0


# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
# set draw handler
frame.set_draw_handler(draw)
# set key handlers
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
# create button
button1 = frame.add_button("Restart Game", new_game)

# start frame
new_game()
frame.start()