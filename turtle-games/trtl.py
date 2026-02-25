import turtle
import random

window = turtle.Screen()
window.bgcolor('green')
window.setup(600, 600)
window.title("Отскоки шариков")
window.tracer(0)

box = turtle.Turtle()
box.hideturtle()
box.pensize(20)
box.penup()
box.color('white')
box.goto(-200, 200)
box.pendown()
box.speed(0)

for i in range(4):
    box.fd(400)
    box.right(90)

balls = []

for i in range(2):
    ball = turtle.Turtle('circle')
    ball.turtlesize(2)
    ball.color('black')
    ball.penup()
    ball.speed(1)
    x = random.randint(-175, 175)
    y = random.randint(-175, 175)
    ball.goto(x, y)
    dx = random.choice([-1, 1]) * 1.3
    dy = random.choice([-1, 1]) * 2.3
    balls.append([ball, x, y, dx, dy])

while True:
    for i in range(len(balls)):
        ball, x, y, dx, dy = balls[i]
        x += dx
        y += dy
        ball.goto(x, y)
        if x < -175 or x > 175:
            dx *= -1
        if y < -175 or y > 175:
            dy *= -1

        balls[i][1] = x
        balls[i][2] = y
        balls[i][3] = dx
        balls[i][4] = dy

    window.update()