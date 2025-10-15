import turtle
import random
import time

# ---------- GLOBAL CONFIG ----------
WIDTH, HEIGHT = 900, 500
TOP_MARGIN = 70
BOTTOM_MARGIN = 60
LEFT_MARGIN = 120
RIGHT_MARGIN = 120
STEP_MIN, STEP_MAX = 1, 4     # smaller steps = slower race
SLEEP_DELAY = 0.02            # frame delay

DEFAULT_NAMES = ["Ruby", "Bluey", "Leafy", "Violet", "Sunny", "Cobalt"]
COLOR_PALETTE = [
    "red", "blue", "green", "purple", "orange", "gold",
    "pink", "brown", "cyan", "magenta", "navy", "darkgreen"
]

# ---------- HELPERS ----------


def get_racer_names_from_console():
    raw = input(
        "Enter racer names, separated by commas (or press Enter for defaults): ").strip()
    if not raw:
        return DEFAULT_NAMES[:]  # copy
    names = [n.strip().title() for n in raw.split(",") if n.strip()]
    return names if names else DEFAULT_NAMES[:]


def assign_colors(num_racers):
    return [COLOR_PALETTE[i % len(COLOR_PALETTE)] for i in range(num_racers)]


def setup_screen():
    screen = turtle.Screen()
    screen.setup(WIDTH, HEIGHT)
    screen.setworldcoordinates(0, HEIGHT, WIDTH, 0)  # top-left origin
    screen.title("Turtle Race (Dynamic Racers)")
    screen.bgcolor("lightblue")
    screen.tracer(0)
    # force screen to appear
    rootwindow = screen._root
    rootwindow.lift()
    rootwindow.attributes('-topmost', True)
    rootwindow.after_idle(rootwindow.attributes, '-topmost', False)
    return screen


def compute_layout(num_lanes):
    start_x = LEFT_MARGIN
    finish_x = WIDTH - RIGHT_MARGIN
    usable_h = HEIGHT - TOP_MARGIN - BOTTOM_MARGIN
    spacing = usable_h // (num_lanes + 1)
    lane_ys = [TOP_MARGIN + (i + 1) * spacing for i in range(num_lanes)]
    return start_x, finish_x, lane_ys


def draw_vertical_line(x, label, color="white"):
    pen = turtle.Turtle(visible=False)
    pen.hideturtle()
    pen.speed(0)
    pen.penup()
    pen.color(color)
    pen.pensize(3)
    pen.goto(x, TOP_MARGIN - 30)
    pen.pendown()
    pen.goto(x, HEIGHT - BOTTOM_MARGIN + 20)
    pen.penup()
    pen.goto(x, TOP_MARGIN - 40)
    pen.write(label, align="center", font=("Arial", 14, "bold"))


def draw_lane_lines(lane_ys, start_x, finish_x):
    pen = turtle.Turtle(visible=False)
    pen.hideturtle()
    pen.speed(0)
    pen.color("#d0eef7")
    pen.pensize(1)
    for y in lane_ys:
        pen.penup()
        pen.goto(start_x - 15, y + 18)
        pen.pendown()
        pen.goto(finish_x + 15, y + 18)


def create_racers(names, colors, lane_ys, start_x):
    racers, dist_labels, name_labels = [], [], []
    for i, y in enumerate(lane_ys):
        r = turtle.Turtle(shape="turtle")
        r.color(colors[i])
        r.penup()
        r.goto(start_x, y)
        r.setheading(0)
        r.pendown()
        racers.append(r)

        d_lbl = turtle.Turtle(visible=False)
        d_lbl.hideturtle()
        d_lbl.penup()
        d_lbl.color("black")
        d_lbl.goto(start_x, y + 22)
        d_lbl.write("0", align="center", font=("Arial", 12, "bold"))
        dist_labels.append(d_lbl)

        n_lbl = turtle.Turtle(visible=False)
        n_lbl.hideturtle()
        n_lbl.penup()
        n_lbl.color("black")
        n_lbl.goto(start_x, y - 26)  # above (remember: up is -Y)
        n_lbl.write(names[i], align="center", font=("Arial", 12, "bold"))
        name_labels.append(n_lbl)
    return racers, dist_labels, name_labels


def run_race(screen, racers, names, dist_labels, name_labels, lane_ys, start_x, finish_x):
    winner_index = None
    running = True
    while running:
        for i, r in enumerate(racers):
            step = random.randint(STEP_MIN, STEP_MAX)
            r.forward(step)

            # Follow the racer with labels
            x_now = r.xcor()
            y_lane = lane_ys[i]
            dist = max(0, int(x_now - start_x))

            dist_labels[i].clear()
            dist_labels[i].goto(x_now, y_lane + 22)
            dist_labels[i].write(str(dist), align="center",
                                 font=("Arial", 12, "bold"))

            name_labels[i].clear()
            name_labels[i].goto(x_now, y_lane - 26)
            name_labels[i].write(names[i], align="center",
                                 font=("Arial", 12, "bold"))

            if x_now >= finish_x:
                winner_index = i
                running = False
                break
        screen.update()
        time.sleep(SLEEP_DELAY)
    return winner_index


def show_winner(name):
    banner = turtle.Turtle(visible=False)
    banner.hideturtle()
    banner.penup()
    banner.color("black")
    banner.goto(WIDTH // 2, TOP_MARGIN // 2)
    banner.write(f"{name} wins!", align="center", font=("Arial", 20, "bold"))

# ---------- MAIN ----------


def main():
    names = get_racer_names_from_console()
    colors = assign_colors(len(names))
    screen = setup_screen()

    start_x, finish_x, lane_ys = compute_layout(len(names))
    draw_vertical_line(start_x, "START")
    draw_vertical_line(finish_x, "FINISH")
    draw_lane_lines(lane_ys, start_x, finish_x)
    screen.update()

    racers, dist_labels, name_labels = create_racers(
        names, colors, lane_ys, start_x)
    screen.update()

    winner_index = run_race(
        screen, racers, names, dist_labels, name_labels, lane_ys, start_x, finish_x
    )
    show_winner(names[winner_index])
    screen.update()

    turtle.done()


# ---------- ENTRY POINT ----------
if __name__ == "__main__":
    main()
