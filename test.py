from elevator import *
from parse import *
from person import *

out = []


def parse_all(path):
    res = []
    with open(f'{path}.txt', 'r') as f:
        data = f.readlines()
    for line in data:
        res.append(parse(line))
    return res


def filter_in():
    data = {}
    stdin = parse_all('stdin')
    for ele in stdin:
        if ele.person is not None:
            data[ele.person] = ele
    return data


def judge_output_valid():
    err = ''
    global out
    out = parse_all("stdout")
    elevators = [] * 6
    for i in range(6):
        elevators.append(Elevator(i))
    for request in out:
        res = elevators[request.elevator - 1].execute(request)
        if res != "True":
            err += f"While executing {str(request)}\n" + res + '\n'
    for ele in elevators:
        if len(ele.persons) != 0:
            err += f"{ele.id + 1}: Someone is trapped in elevator!\n"
        if len(ele.receive) != 0:
            err += f"{ele.id + 1}: Some requests is not finished!\n"
        if ele.door_state == 'open':
            err += f"{ele.id + 1}: Door is not closed finally!\n"
        if ele.elevator_state != 'unscheduled':
            err += f"{ele.id + 1}: Elevator scheduled not finish!\n"
    return err


def filter_out():
    data = {}
    for request in out:
        if request.person is not None:
            if request.person in data:
                data[request.person].append(request)
            else:
                data[request.person] = [request]
    return data


def judge_person_request():
    stdin = filter_in()
    stdout = filter_out()
    err = ''
    for ele in stdin.keys():
        if ele not in stdout:
            err += f"{stdin[ele]}: Some requests is not be served!\n"
        else:
            instructions = stdout[ele]
            p = Person(stdin[ele])
            for ins in instructions:
                res = p.execute(ins)
                if res != "True":
                    err += f"While serving {ele}\n" + res + '\n'
    return err


if __name__ == '__main__':
    print(judge_output_valid() + judge_person_request())
