import turtle

screen = turtle.Screen()
screen.setup(600, 600)
screen.bgcolor("white")

t = turtle.Turtle()
t.speed(0)
turtle.tracer(0)
t.penup()
t.hideturtle()

size = 10

bob_colors = {
    0: "white",
    1: "#000000",
    2: "#b60005",
    3: "#697ef4",
    4: "#fded47",
    5: "#e6e2b1",
    6: "#8d5d35",
    7: "#febbad"
}

pl_colors = {
    0: "white",
    1: "black",
    2: "#69b6bd",
    3: "#fcfdb2",
    4: "#c54c53",
    5: "#406e6e"
}

g_colors = {
    0: "white",
    1: "black",
    2: "#a2d1eb",
    3: "#fcb6b6",
    4: "#e0f87e",
    5: "#c64e52",
    6: "#9280ef"
}

def load_matrix(filename):
    matrix = []
    with open(filename, "r") as file:
        for line in file:
            row = list(map(int, line.split()))
            matrix.append(row)
    return matrix

garry = load_matrix("garry.txt")

def draw_pixel(x, y, color):
    t.goto(x, y)
    t.pendown()
    t.fillcolor(color)
    t.begin_fill()
    for _ in range(4):
        t.forward(size)
        t.right(90)
    t.end_fill()
    t.penup()


def draw(what, color, x, y):
    for i in range(len(what)):
        for j in range(len(what[i])):
            draw_pixel(x + j * size, y - i * size, color[what[i][j]])


x0 = - (len(garry[0]) * size) // 2
y0 = (len(garry) * size) // 2 

'''x1 =  180 - (len(sponge_bob[0]) * size) // 2
y1 = (len(sponge_bob) * size) // 2 

x2 = (len(plankton[0]) * size) // 2 - 300
y2 = (len(plankton) * size) // 2 

draw(plankton, g_colors, x2, y2)
draw(sponge_bob, bob_colors, x1, y1)'''
draw(garry, pl_colors, x0, y0)



turtle.done()
