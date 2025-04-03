import random
from parse import *

floors = ["B4", "B3", "B2", "B1", "F1", "F2", "F3", "F4", "F5", "F6", "F7"]
last_time = [10000] * 6
id_list = set()


def generate_time(start):
    return random.choice(range(start, 100001, 1))


def print_time(time):
    time = str(time)
    return time[:-4] + '.' + time[-4]


def generate_person():
    p = random.choice(list(id_list))
    id_list.remove(p)
    return p


def generate_priority():
    return random.choice(range(1, 101, 1))


def generate_path():
    return random.sample(floors, 2)


def generate_floor():
    return random.choice(floors)


def generate_elevator():
    return random.choice(range(1, 7, 1))


def generate_speed():
    return random.choice(['0.2', '0.3', '0.4', '0.5'])


def generate_move():
    time = generate_time(10000)
    person = generate_person()
    priority = generate_priority()
    path = generate_path()
    return f"[{print_time(time)}]{person}-PRI-{priority}-FROM-{path[0]}-TO-{path[1]}\n"


def generate_schedule():
    floor = random.choice(floors[2:9:1])
    elevator = generate_elevator()
    temp = last_time[elevator - 1]
    start = 10000 if temp == 10000 else temp + 60000
    if start <= 100000:
        time = generate_time(start)
        last_time[elevator - 1] = time
        speed = generate_speed()
        return f"[{print_time(time)}]SCHE-{elevator}-{speed}-{floor}\n"
    return None


def generate():
    res = generate_schedule()
    return res if res is not None else generate_move()


def make(number):
    for i in range(100, 1000, 1):
        id_list.add(i)
    data = [generate() for _ in range(number)]

    def get_time(_):
        start = _.find('[') + 1
        end = _.find(']')
        return parse_time(_[start:end])

    sorted_data = sorted(data, key=get_time)
    with open("stdin.txt", "w") as f:
        f.writelines(sorted_data)


if __name__ == "__main__":
    make(100)
