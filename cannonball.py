from random import randrange as rnd, choice
import tkinter as tk
import math
import time

print(dir(math))

root = tk.Tk()
fr = tk.Frame(root)
root.geometry('800x600')
canv = tk.Canvas(root, bg='white')
canv.pack(fill=tk.BOTH, expand=1)

result_bar = canv.create_text(400, 300, text='', font='28')
level_bar = canv.create_text(400, 30, text='', font='28')
level = 1
number_of_targets = 5

targets = []


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


gun = Gun()


def new_game(event=''):
    global balls, bullet, level

    for i in range(number_of_targets):
        target = Target()
        targets.append(target)

    canv.itemconfig(level_bar, text='Level:' + str(level))
    level += 1
    bullet = 0
    balls = []
    canv.bind('<Button-1>', gun.fire2_start)
    canv.bind('<ButtonRelease-1>', gun.fire2_end)
    canv.bind('<Motion>', gun.targetting)
    z = 0.03
    life = number_of_targets  # счетчик уничтоженных мишеней
    for target in targets:
        target.live = 1
    while life > 0 or balls:  # работает, пока не все мишени уничтожены или остаются шарики
        for b in balls:
            b.move()
            for target in targets:
                if b.hittest(target) and target.live:  # проверяет попадание шарика в мишень
                    target.hit()
                    target.live = 0
                    life -= 1
            if life == 0:  # когда мишеней не остается, отображает результат
                canv.bind('<Button-1>', '')
                canv.bind('<ButtonRelease-1>', '')
                canv.itemconfig(result_bar, text='Вы уничтожили цели за ' + str(bullet) + ' выстрелов')

        canv.update()
        time.sleep(z)
        gun.targetting()
        gun.power_up()
        for target in targets:
            target.move_target()

    canv.itemconfig(result_bar, text='')

    canv.delete(Gun)
    root.after(750, new_game)


new_game()
root.mainloop()
