import tkinter as tk
import math
import time
from Target import Target
from Gun import Gun


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

gun = Gun()


def new_game(event=''):
    global balls, bullet, level

    for i in range(number_of_targets):
        target = Target()
        targets.append(target)

    canv.itemconfig(level_bar, text='Level:' + str(level))
    level += 1
    bullet = 0
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
