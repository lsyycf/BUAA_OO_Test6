class Elevator:
    def __init__(self, idx):
        self.speed = 4000
        self.floor = 4
        self.door_state = 'close'  # close open
        self.elevator_state = 'unscheduled'  # unscheduled scheduled before
        self.receive = []
        self.persons = []
        self.capacity = 6
        self.id = idx
        self.time = 0  # 收到当前指令的时间
        self.open_time = 0  # 上次开门的时间
        self.arrive_time = 0  # 上次到达的时间
        self.arrive_before_schedule = 0  # 收到人工调度请求到接受调度请求之间的到达次数
        self.schedule_receive_time = 0  # 收到人工调度请求的时间
        self.schedule_time = 0  # 调度开门时间
        self.receive_time = 0  # 接受请求时间
        self.target = 4
        self.speed_temp = 4000

    def in_person(self, request):
        err = ''
        if self.floor != request.floor:
            err += "Elevator position error!"
        if self.elevator_state == 'scheduled':
            err += "Elevator can't enter!"
        if request.person not in self.receive:
            err += "Person not received!"
        if len(self.persons) >= self.capacity:
            err += "OverLoad!"
        if self.door_state == 'close':
            err += "Door is Closed!"
        self.persons.append(request.person)
        self.receive.remove(request.person)
        return "True" if len(err) == 0 else err

    def out_person(self, request):
        err = ''
        if self.floor != request.floor:
            err += "Elevator position error!"
        if request.person not in self.persons:
            err += "Person does not exist!"
        if self.door_state == 'scheduled' and self.floor != request.floor:
            err += "Elevator is scheduled!"
        if self.door_state == 'close':
            err += "Door is Closed!"
        self.persons.remove(request.person)
        return "True" if len(err) == 0 else err

    def arrive(self, request):
        err = ''
        if abs(self.floor - request.floor) > 1:
            err += "Elevator move error!"
        if self.door_state == 'open':
            err += "Elevator open while moving!"
        if self.elevator_state == 'before':
            self.arrive_before_schedule += 1
            if self.arrive_before_schedule > 2:
                err += "Elevator move too much before schedule!"
        if self.arrive_time != 0 and self.time - self.arrive_time < self.speed:
            err += "Elevator move too fast!"
        if self.elevator_state != 'scheduled' and len(self.persons) == 0 and len(self.receive) == 0:
            err += "Elevator move unscheduled!"
        if len(self.persons) == 0 and len(self.receive) != 0:
            if self.receive_time != 0 and self.time - self.receive_time < self.speed:
                err += "Elevator move too early!"
        self.floor = request.floor
        self.arrive_time = self.time
        return "True" if len(err) == 0 else err

    def receive_request(self, request):
        err = ''
        if self.elevator_state == 'scheduled':
            err += "Elevator can't receive request!"
        self.receive.append(request.person)
        if len(self.receive) == 0:
            self.receive_time = self.time
        return "True" if len(err) == 0 else err

    def schedule_accept(self, request):
        self.schedule_receive_time = self.time
        self.elevator_state = 'before'
        self.target = request.floor
        self.speed_temp = request.speed
        return "True"

    def schedule_begin(self):
        err = ''
        if self.elevator_state == 'scheduled':
            err += "Elevator schedule multiply!"
        if self.door_state == 'open':
            err += "Schedule begin while opening!"
        self.elevator_state = 'scheduled'
        self.arrive_before_schedule = 0
        self.receive = []
        self.speed = self.speed_temp
        return "True" if len(err) == 0 else err

    def schedule_end(self):
        err = ''
        if self.elevator_state != 'scheduled':
            err += "Elevator schedule while not scheduled!"
        if self.time - self.schedule_receive_time > 60000:
            err += "Scheduled too slow!"
        if self.door_state == 'open':
            err += "Schedule end while opening!"
        if self.target != self.floor:
            err += "Elevator schedule not correct!"
        self.elevator_state = 'unscheduled'
        self.target = 4
        self.speed = 4000
        return "True" if len(err) == 0 else err

    def open(self, request):
        err = ''
        if self.floor != request.floor:
            err += "Elevator position error!"
        if self.door_state == 'open':
            err += "Door is already open!"
        self.door_state = 'open'
        if self.elevator_state == 'scheduled':
            if self.floor != self.target:
                err += "Elevator can't open while scheduled!"
            self.schedule_time = self.time
        self.open_time = self.time
        return "True" if len(err) == 0 else err

    def close(self, request):
        err = ''
        if self.floor != request.floor:
            err += "Elevator position error!"
        if self.door_state == 'close':
            err += "Door is already closed!"
        if self.elevator_state == 'scheduled':
            if self.target != self.floor:
                err += "Elevator can't close while scheduled!"
            if self.time - self.schedule_time < 10000:
                err += "Scheduled too fast!"
        if self.time - self.open_time < 4000:
            err += "Elevator close too fast!"
        self.door_state = 'close'
        return "True" if len(err) == 0 else err

    def execute(self, request):
        self.time = request.time
        if request.tp == "IN":
            return self.in_person(request)
        elif request.tp == "OUT_S" or request.tp == "OUT_F":
            return self.out_person(request)
        elif request.tp == "ARRIVE":
            return self.arrive(request)
        elif request.tp == "SCHE_ACCEPT":
            return self.schedule_accept(request)
        elif request.tp == "SCHE_BEGIN":
            return self.schedule_begin()
        elif request.tp == "SCHE_END":
            return self.schedule_end()
        elif request.tp == "OPEN":
            return self.open(request)
        elif request.tp == "CLOSE":
            return self.close(request)
        elif request.tp == "RECEIVE":
            return self.receive_request(request)
