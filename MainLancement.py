from turtle import Turtle, Screen

def draw_square(some_turtle):
    for _ in range(4):
        some_turtle.forward(200)
        some_turtle.right(90)

def draw_art():
    # Turtle Brad
    brad = Turtle(shape="turtle")
    brad.color("yellow")
    brad.pensize(2)
    brad.speed("fastest")
    for _ in range(36):
        draw_square(brad)
        brad.right(10)

    # Turtle Angie
    angie = Turtle(shape="turtle")
    angie.color("blue")
    angie.pensize(2)
    angie.speed("fastest")
    angie.penup()
    angie.goto(0, -100)
    angie.pendown()
    angie.circle(100)

    # Ajout du texte "Discord"
    text_pen = Turtle()
    text_pen.penup()
    text_pen.color("white")
    text_pen.goto(0, 200)
    

window = Screen()
window.bgcolor("black")

draw_art()

window.exitonclick()