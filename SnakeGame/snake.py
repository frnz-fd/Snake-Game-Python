import turtle
import time
import random

# ⚙️ تنظیمات اولیه
delay = 0.1
score = 0
high_score = 0
colors = ["red", "orange", "yellow", "green", "blue", "purple"]

# 🖥️ صفحه بازی
wn = turtle.Screen()
wn.title("Snake Game with Visual Effects")
wn.bgcolor("black")
wn.setup(width=600, height=600)
wn.tracer(0)

# 🐍 سر مار
head = turtle.Turtle()
head.shape("square")
head.color("white")
head.penup()
head.goto(0, 0)
head.direction = "stop"

# 🍏 غذا
food = turtle.Turtle()
food.shape("circle")
food.color("red")
food.penup()
food.goto(0, 100)

segments = []

# 📊 امتیازدهی
pen = turtle.Turtle()
pen.speed(0)
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 260)
pen.write("Score: 0    High Score: 0", align="center", font=("Courier", 24, "normal"))

# 💥 تابع تولید افکت پارتیکل هنگام خوردن غذا
def create_particles(x, y):
    particles = []

    for _ in range(15):
        p = turtle.Turtle()
        p.shape("circle")
        p.color(random.choice(colors))
        p.penup()
        p.goto(x, y)
        p.shapesize(random.uniform(0.4, 1.0))
        dx = random.uniform(-30, 30)
        dy = random.uniform(-30, 30)
        particles.append((p, dx, dy))

    steps = 10
    def animate(step):
        if step <= steps:
            for p, dx, dy in particles:
                p.goto(p.xcor() + dx / steps, p.ycor() + dy / steps)
            wn.ontimer(lambda: animate(step + 1), 50)
        else:
            for p, _, _ in particles:
                p.hideturtle()
                p.goto(1000, 1000)
    animate(0)

# 🧭 حرکت دادن مار
def move():
    if head.direction == "up":
        head.sety(head.ycor() + 20)
    elif head.direction == "down":
        head.sety(head.ycor() - 20)
    elif head.direction == "left":
        head.setx(head.xcor() - 20)
    elif head.direction == "right":
        head.setx(head.xcor() + 20)

# 🎮 کنترل جهت حرکت
def go_up():
    if head.direction != "down":
        head.direction = "up"

def go_down():
    if head.direction != "up":
        head.direction = "down"

def go_left():
    if head.direction != "right":
        head.direction = "left"

def go_right():
    if head.direction != "left":
        head.direction = "right"

# ⌨️ تعریف کلیدها
wn.listen()
wn.onkeypress(go_up, "Up")
wn.onkeypress(go_down, "Down")
wn.onkeypress(go_left, "Left")
wn.onkeypress(go_right, "Right")

# 🔁 حلقه‌ی اصلی بازی
try:
    while True:
        wn.update()

        # 🚫 برخورد با دیواره‌ها
        if abs(head.xcor()) > 290 or abs(head.ycor()) > 290:
            time.sleep(0.5)
            head.goto(0, 0)
            head.direction = "stop"
            for segment in segments:
                segment.goto(1000, 1000)
            segments.clear()
            score = 0
            pen.clear()
            pen.write(f"Score: {score}    High Score: {high_score}", align="center", font=("Courier", 24, "normal"))

        # 🍽️ خوردن غذا
        if head.distance(food) < 20:
            x = random.randint(-280, 280)
            y = random.randint(-280, 280)
            food.goto(x, y)
            create_particles(x, y)

            new_segment = turtle.Turtle()
            new_segment.shape("square")
            new_segment.color("grey")
            new_segment.penup()
            segments.append(new_segment)

            score += 10
            if score > high_score:
                high_score = score

            pen.clear()
            pen.write(f"Score: {score}    High Score: {high_score}", align="center", font=("Courier", 24, "normal"))

        # 🐍 دنبال کردن مار
        for i in range(len(segments) - 1, 0, -1):
            segments[i].goto(segments[i - 1].xcor(), segments[i - 1].ycor())
        if segments:
            segments[0].goto(head.xcor(), head.ycor())

        move()

        # ⚠️ برخورد با خودش
        for segment in segments:
            if segment.distance(head) < 20:
                time.sleep(0.5)
                head.goto(0, 0)
                head.direction = "stop"
                for segment in segments:
                    segment.goto(1000, 1000)
                segments.clear()
                score = 0
                pen.clear()
                pen.write(f"Score: {score}    High Score: {high_score}", align="center", font=("Courier", 24, "normal"))

        time.sleep(delay)

except turtle.Terminator:
    print("🎮 بازی متوقف شد — پنجره بسته شده یا پایان یافت.")
