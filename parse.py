from request import *

floors = ["B4", "B3", "B2", "B1", "F1", "F2", "F3", "F4", "F5", "F6", "F7"]


def parse_time(time):
    time = time.strip().split(".")
    first = int(time[0])
    second = int(time[1] + (4 - len(time[1])) * '0')
    return first * 10000 + second


def parse_floor(floor):
    return floors.index(floor)


def parse_move(ins):
    time = parse_time(ins[0])
    person = ins[1]
    start = parse_floor(ins[5])
    end = parse_floor(ins[7])
    return Request("MOVE", time, person, None, start, end, None, None)


def parse_sche(ins):
    time = parse_time(ins[0])
    elevator = ins[2]
    speed = parse_time(ins[3])
    floor = parse_floor(ins[4])
    return Request("SCHE", time, None, floor, None, None, elevator, speed)


def parse_arrive(ins):
    time = parse_time(ins[0])
    floor = parse_floor(ins[2])
    elevator = ins[3]
    return Request("ARRIVE", time, None, floor, None, None, elevator, None)


def parse_open(ins):
    time = parse_time(ins[0])
    floor = parse_floor(ins[2])
    elevator = ins[3]
    return Request("OPEN", time, None, floor, None, None, elevator, None)


def parse_close(ins):
    time = parse_time(ins[0])
    floor = parse_floor(ins[2])
    elevator = ins[3]
    return Request("CLOSE", time, None, floor, None, None, elevator, None)


def parse_in(ins):
    time = parse_time(ins[0])
    person = ins[2]
    floor = parse_floor(ins[3])
    elevator = ins[4]
    return Request("IN", time, person, floor, None, None, elevator, None)


def parse_out_s(ins):
    time = parse_time(ins[0])
    person = ins[3]
    floor = parse_floor(ins[4])
    elevator = ins[5]
    return Request("OUT_S", time, person, floor, None, None, elevator, None)


def parse_out_f(ins):
    time = parse_time(ins[0])
    person = ins[3]
    floor = parse_floor(ins[4])
    elevator = ins[5]
    return Request("OUT_F", time, person, floor, None, None, elevator, None)


def parse_sche_accept(ins):
    time = parse_time(ins[0])
    elevator = ins[3]
    speed = parse_time(ins[4])
    floor = parse_floor(ins[5])
    return Request("SCHE_ACCEPT", time, None, floor, None, None, elevator, speed)


def parse_sche_begin(ins):
    time = parse_time(ins[0])
    elevator = ins[3]
    return Request("SCHE_BEGIN", time, None, None, None, None, elevator, None)


def parse_sche_end(ins):
    time = parse_time(ins[0])
    elevator = ins[3]
    return Request("SCHE_END", time, None, None, None, None, elevator, None)


def parse_receive(ins):
    time = parse_time(ins[0])
    person = ins[2]
    elevator = ins[3]
    return Request("RECEIVE", time, person, None, None, None, elevator, None)


def parse(ins):
    ins = ins.strip().replace("[", "").replace("]", "-").split("-")
    if "SCHE" in ins:
        if "ACCEPT" in ins:
            return parse_sche_accept(ins)
        elif "BEGIN" in ins:
            return parse_sche_begin(ins)
        elif "END" in ins:
            return parse_sche_end(ins)
        else:
            return parse_sche(ins)
    elif "OUT" in ins:
        if "S" in ins:
            return parse_out_s(ins)
        elif "F" in ins:
            return parse_out_f(ins)
    elif "ARRIVE" in ins:
        return parse_arrive(ins)
    elif "IN" in ins:
        return parse_in(ins)
    elif "OPEN" in ins:
        return parse_open(ins)
    elif "CLOSE" in ins:
        return parse_close(ins)
    elif "RECEIVE" in ins:
        return parse_receive(ins)
    elif "PRI" in ins:
        return parse_move(ins)
