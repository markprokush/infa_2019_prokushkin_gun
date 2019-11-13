from random import randrange as rnd
import math
import tkinter as tk
from Ball import Ball

root = tk.Tk()
canv = tk.Canvas(root, bg='white')


class Gun:
    y1 = rnd(100, 500)

    def __init__(self):
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        y1 = self.y1
        self.id = canv.create_line(20, y1, 50, y1 - 30, width=7)

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        new_ball = Ball()
        new_ball.r += 5
        self.an = math.atan((event.y - new_ball.y) / (event.x - new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = - self.f2_power * math.sin(self.an)
        balls += [new_ball]
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event=0):
        """Прицеливание. Зависит от положения мыши"""
        if event:
            self.an = math.atan((event.y - self.y1) / (event.x - 20))
        if self.f2_on:
            canv.itemconfig(self.id, fill='orange')
        else:
            canv.itemconfig(self.id, fill='black')
        canv.coords(self.id, 20, self.y1,
                    20 + max(self.f2_power, 20) * math.cos(self.an),
                    self.y1 + max(self.f2_power, 20) * math.sin(self.an)
                    )

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            canv.itemconfig(self.id, fill='orange')
        else:
            canv.itemconfig(self.id, fill='black')


class Target:
    def __init__(self):
        self.points = 0
        self.live = 1
        self.id = canv.create_oval(0, 0, 0, 0)
        self.new_target()

    def new_target(self):
        """ Инициализация новой цели """
        x = self.x = rnd(600, 780)
        y = self.y = rnd(300, 550)
        r = self.r = rnd(2, 50)
        vx = self.vx = rnd(-10, 10)
        vy = self.vy = rnd(-10, 10)
        dx = self.dx = vx
        dy = self.dy = vy
        color = self.color = 'red'
        canv.coords(self.id, x - r, y - r, x + r, y + r)
        canv.itemconfig(self.id, fill=color)

    def hit(self, points=1):
        """Попадание шарика в цель"""
        canv.coords(self.id, -10, -10, -10, -10)

    def move_target(self):
        """Движение мишени"""
        self.x += self.dx
        self.y += self.dy
        # проверка столкновения со стенками (для мишеней существует стенка x=200, чтобы пушка могла нормально целиться):
        if ((canv.coords(self.id)[2] + self.dx >= 800) and self.dx > 0) \
                or ((canv.coords(self.id)[0] + self.dx <= 200) and (self.dx < 0)):
            self.dx = -self.dx
        # проверка столкновения с полом или потолком:
        if ((canv.coords(self.id)[3] + self.dy >= 600) and self.dy > 0) \
                or ((canv.coords(self.id)[1] + self.dy <= 10) and self.dy < 0):
            self.dy = -self.dy
        # зануляет скорость сбитых мишеней, которые отправили в точку (-10, -10)
        if canv.coords(self.id)[0] == -10:
            self.dx = 0
            self.dy = 0
        canv.move(self.id, self.dx, self.dy)