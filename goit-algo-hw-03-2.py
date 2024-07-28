import turtle
import colorama
from colorama import Fore, Style

colorama.init()

def koch_snowflake(t, order, size):
    if order == 0:
        t.forward(size)
    else:
        for angle in [60, -120, 60, 0]:
            koch_snowflake(t, order - 1, size / 3)
            t.left(angle)

def main():
    screen = turtle.Screen()
    screen.title("Сніжинка Коха")

    t = turtle.Turtle()
    t.speed(0)

    # Запит у користувача на введення рівня рекурсії через термінал
    try:
        order = int(input("Введіть рівень рекурсії (дійсне число, більше за 0): "))
    except ValueError:
        print(Fore.RED + "Будь ласка, введіть дійсне число." + Style.RESET_ALL)
        turtle.bye()
        return

    if order < 0:
        print(Fore.RED + "Рівень рекурсії не може бути від'ємним." + Style.RESET_ALL)
        turtle.bye()
        return

    length = 200

    t.penup()
    t.goto(-length / 2, length / 3)  # Перемістити початкову позицію вгору
    t.pendown()

    for _ in range(3):
        koch_snowflake(t, order, length)
        t.right(120)

    screen.mainloop()

if __name__ == "__main__":
    main()
