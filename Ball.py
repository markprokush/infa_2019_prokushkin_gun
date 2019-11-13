from random import choice
import math
import tkinter as tk
from Gun import Gun

root = tk.Tk()
canv = tk.Canvas(root, bg='white')
balls = []


class Ball:

    def __init__(self, x=40):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.x = x
        self.y = Gun.y1
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = choice(['blue', 'green', 'red', 'brown'])
        self.id = canv.create_oval(
            self.x - self.r,
            self.y - self.r,
            self.x + self.r,
            self.y + self.r,
            fill=self.color
        )
        self.live = 30

    def set_coords(self):
        canv.coords(
            self.id,
            self.x - self.r,
            self.y - self.r,
            self.x + self.r,
            self.y + self.r
        )

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        self.vy -= 1  # ускорение
        # проверка столкновения со стенками:
        if ((canv.coords(self.id)[2] + self.vx >= 800) and (self.vx > 0)) \
                or ((canv.coords(self.id)[0] + self.vx <= 0) and (self.vx < 0)):
            self.vx = -self.vx
            self.vx *= 0.5  # шарик теряет горизонт. скорость после удара о стенку
        # проверка столкновения с полом и потолком
        if ((canv.coords(self.id)[3] - self.vy >= 600) and (self.vy < 0)) \
                or ((canv.coords(self.id)[1] - self.vy <= 0) and (self.vy > 0)):
            self.vy *= 0.5  # шарик теряет обе компоненты скорости после удара о потолок или пол
            self.vx *= 0.5
            self.vy = -self.vy

        if self.vx ** 2 < 1:
            self.vx = 0
            self.vy = 0
            self.y = 580

        self.x += self.vx
        self.y -= self.vy
        self.set_coords()
        if self.vx ** 2 + self.vy ** 2 == 0:
            canv.coords(self.id, -10, -10, -10, -10)

        if math.sqrt(self.vx ** 2 + self.vy ** 2) < 1:  # удаляет шар из списка шаров, если модуль его скорости меньше 1
            balls.remove(self)

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        # проверяет, меньше ли расстояние между центрами шарика и мишени суммы их радиусов
        if (self.x - 0.5 * (canv.coords(obj.id)[0] + canv.coords(obj.id)[2])) ** 2 + \
                (self.y - 0.5 * (canv.coords(obj.id)[1] + canv.coords(obj.id)[3])) ** 2 < \
                (self.r + 1 / 2 * (abs(canv.coords(obj.id)[0] - canv.coords(obj.id)[2]))) ** 2:
            return True
        else:
            return False
