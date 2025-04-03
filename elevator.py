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
        self.target = 4

    def in_person(self, request):
        if self.floor != request.floor:
            return "Elevator position error!"
        if self.elevator_state == 'scheduled':
            return "Elevator can't enter!"
        if request.person not in self.receive:
            return "Person not received!"
        if len(self.persons) >= self.capacity:
            return "OverLoad!"
        if self.door_state == 'close':
            return "Door is Closed!"
        self.persons.append(request.person)
        self.receive.remove(request.person)
        return "True"

    def out_person(self, request):
        if self.floor != request.floor:
            return "Elevator position error!"
        if request.person not in self.persons:
            return "Person does not exist!"
        if self.door_state == 'scheduled' and self.floor != request.floor:
            return "Elevator is scheduled!"
        if self.door_state == 'close':
            return "Door is Closed!"
        self.persons.remove(request.person)
        return "True"

    def arrive(self, request):
        if abs(self.floor - request.floor) > 1:
            return "Elevator move error!"
        if self.door_state == 'open':
            return "Elevator open while moving!"
        if self.elevator_state == 'before':
            self.arrive_before_schedule += 1
            if self.arrive_before_schedule > 2:
                return "Elevator move too much before schedule!"
        if self.arrive_time != 0 and self.time - self.arrive_time < self.speed:
            return "Elevator move too fast!"
        self.floor = request.floor
        return "True"

    def receive_request(self, request):
        if self.elevator_state == 'scheduled':
            return "Elevator can't receive request!"
        self.receive.append(request.person)
        return "True"

    def schedule_accept(self, request):
        self.schedule_receive_time = self.time
        self.elevator_state = 'before'
        self.target = request.floor
        self.speed = request.speed
        return "True"

    def schedule_begin(self, request):
        if self.elevator_state == 'scheduled':
            return "Elevator schedule multiply!"
        if self.door_state == 'open':
            return "Schedule begin while opening!"
        self.elevator_state = 'scheduled'
        self.arrive_before_schedule = 0
        self.receive = []
        return "True"

    def schedule_end(self, request):
        if self.elevator_state != 'scheduled':
            return "Elevator schedule while not scheduled!"
        if self.time - self.schedule_receive_time > 60000:
            return "Scheduled too slow!"
        if self.door_state == 'open':
            return "Schedule end while opening!"
        if self.target != self.floor:
            return "Elevator schedule not correct!"
        self.elevator_state = 'unscheduled'
        self.target = 4
        self.speed = 4000
        return "True"

    def open(self, request):
        if self.floor != request.floor:
            return "Elevator position error!"
        if self.door_state == 'open':
            return "Door is already open!"
        self.door_state = 'open'
        if self.elevator_state == 'scheduled':
            if self.floor != self.target:
                return "Elevator can't open while scheduled!"
            self.schedule_time = self.time
        self.open_time = self.time
        return "True"

    def close(self, request):
        if self.floor != request.floor:
            return "Elevator position error!"
        if self.door_state == 'close':
            return "Door is already closed!"
        if self.elevator_state == 'scheduled':
            if self.target != self.floor:
                return "Elevator can't close while scheduled!"
            if self.time - self.schedule_time < 10000:
                return "Scheduled too fast!"
        if self.time - self.open_time < 4000:
            return "Elevator close too fast!"
        self.door_state = 'close'
        return "True"

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
            return self.schedule_begin(request)
        elif request.tp == "SCHE_END":
            return self.schedule_end(request)
        elif request.tp == "OPEN":
            return self.open(request)
        elif request.tp == "CLOSE":
            return self.close(request)
        elif request.tp == "RECEIVE":
            return self.receive_request(request)
