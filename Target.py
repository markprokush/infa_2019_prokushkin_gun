from random import randrange as rnd
import tkinter as tk

root = tk.Tk()
canv = tk.Canvas(root, bg='white')

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
