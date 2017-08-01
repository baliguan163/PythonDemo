#coding=utf-8
import turtle

#创建一个实例
t=turtle.Turtle()

# #向前走 单位像素
# t.forward(100)
# #单位是角度
# t.right(90)
# t.forward(100)
# #单位是角度
# t.right(90)
# t.forward(100)
# #单位是角度
# t.right(90)
# t.forward(100)
# #单位是角度
# t.right(90)

# t.penup()
# t.goto(-100,-100)
# t.pendown()

t.pencolor('red')
t.begin_fill('green')
for i in range(4):
	t.forward(100)
	t.right(90)
	t.forward(150)
	t.right(90)
t.end_fill()


#
# def setpen(color):
# 	t.pencolor(color)
# 	t.fillcolor(color)
#     #t.hideturtle()
#
# def setpen(x,y):
# 	t.penup()
# 	t.goto(x,y)
# 	t.pendown()
# 	t.setheading(0)
#
# def rect(x,y,w,h,color):
# 	t.setcolor(color)
# 	t.setpen(x,y)
# 	t.begin_fill()
# 	for i in range(2):
# 		t.forward(h)
# 		t.right(90)
# 		t.forward(w)
# 		t.right(90)
#         t.end_fill()
# 	t.end_fill()
#
#
# temps = [16,17,22,30,21,27,24]
# def line_chart(x,y,color,temps, pixl,space):
# 	t.setpen(x,y)
# 	t.setcolor(color)
# 	for i,j in enumerate(temps)
# 		x1 = x + (x + 1) * space
# 		y1 = y + j*pixl
# 		#t.goto(x1,y1)
#         dot(x,y)
#
# def dot(x,y):
# 	t.pencolor('blcak')
# 	t.pensize(2)
# 	t.goto(x,y)
# 	t.begin_fill()
# 	t.circle(4)
# 	t.end_fill()

#line_chart(0,0,'red',temps,10,30)

#def bar_chart(x,y,temps,)



turtle.done()