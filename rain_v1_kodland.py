import turtle
import time
import random


window=turtle.Screen()
window.tracer(0)
t=turtle.Turtle()
window.bgcolor("black")
drops=[]
for i in range(100):
    drops.append([random.randint(0-window.window_width()/2,window.window_width()/2),window.window_height()/2])



while True:
    t.clear()
    for i in drops[:]:
        if i[1] <= 0-window.window_height()/2:
            drops.pop(drops.index(i))
            drops.append([random.randint(0-window.window_width()/2,window.window_width()/2),window.window_height()/2])
        else:
            i[1] -= random.randint(1,2)
            i[0] += random.randint(-1,0)
            t.penup()
            t.setposition(i[0],i[1])
            t.pendown()
            t.dot(3,"lightblue")
    window.update()
    time.sleep(0.01)
