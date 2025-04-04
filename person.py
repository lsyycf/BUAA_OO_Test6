class Person:
    def __init__(self, request):
        self.id = request.person
        self.floor = request.start
        self.target = request.end
        self.state = "unreceived"  # in wait unreceived finish
        self.elevator = 0

    def in_person(self, request):
        err = ''
        if self.state == "unreceived":
            err += "Person is unreceived!"
        if self.state == "in":
            err += "Person is already in!"
        if self.floor != request.floor:
            err += "Incorrect floor!"
        if self.elevator == 0:
            err += "No elevator serve!"
        if self.elevator != request.elevator:
            err += "Incorrect elevator!"
        self.state = "in"
        return "True" if len(err) == 0 else err

    def out_s_person(self, request):
        err = ''
        if self.state == "wait":
            err += "Person isn't in!"
        if self.target != request.floor:
            err += "Person is already arrive!"
        if self.elevator != request.elevator:
            err += "Incorrect elevator!"
        self.floor = request.floor
        self.state = "finish"
        self.elevator = 0
        return "True" if len(err) == 0 else err

    def out_f_person(self, request):
        err = ''
        if self.state == "wait":
            err += "Person isn't in!"
        if self.state == "unreceived":
            err += "Person is unreceived!"
        if self.target == request.floor:
            err += "Person has not already arrived yet!"
        if self.elevator != request.elevator:
            err += "Incorrect elevator!"
        self.state = "unreceived"
        self.floor = request.floor
        self.elevator = 0
        return "True" if len(err) == 0 else err

    def schedule_begin(self, request):
        if self.elevator == request.elevator and self.state == "wait":
            self.elevator = 0
            self.state = "unreceived"
        return "True"

    def receive_request(self, request):
        err = ''
        if self.state != "unreceived":
            err += "Person is already received!"
        self.elevator = request.elevator
        self.state = "wait"
        return "True" if len(err) == 0 else err

    def execute(self, request):
        if request.tp == "IN":
            return self.in_person(request)
        elif request.tp == "OUT_S":
            return self.out_s_person(request)
        elif request.tp == "OUT_F":
            return self.out_f_person(request)
        elif request.tp == "RECEIVE":
            return self.receive_request(request)
        elif request.tp == "SCHE_BEGIN":
            return self.schedule_begin(request)
