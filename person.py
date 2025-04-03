class Person:
    def __init__(self, request):
        self.id = request.person
        self.floor = request.start
        self.target = request.end
        self.state = "out"  # in out
        self.elevator = 0

    def in_person(self, request):
        if self.state == "in":
            return "Person is already in!"
        if self.floor != request.floor:
            return "Incorrect floor!"
        if self.elevator == 0:
            return "No elevator serve!"
        if self.elevator != request.elevator:
            return "Incorrect elevator!"
        self.state = "in"
        return "True"

    def out_s_person(self, request):
        if self.state == "out":
            return "Person is already out!"
        if self.target != request.floor:
            return "Person is already arrive!"
        if self.elevator != request.elevator:
            return "Incorrect elevator!"
        self.floor = request.floor
        self.state = "out"
        self.elevator = 0
        return "True"

    def out_f_person(self, request):
        if self.state == "out":
            return "Person is already out!"
        if self.target == request.floor:
            return "Person has not already arrived yet!"
        if self.elevator != request.elevator:
            return "Incorrect elevator!"
        self.state = "out"
        self.floor = request.floor
        self.elevator = 0
        return "True"

    def receive_request(self, request):
        if self.state == "in":
            return "Person is already in!"
        self.elevator = request.elevator
        return "True"

    def execute(self, request):
        if request.tp == "IN":
            return self.in_person(request)
        elif request.tp == "OUT_S":
            return self.out_s_person(request)
        elif request.tp == "OUT_F":
            return self.out_f_person(request)
        elif request.tp == "RECEIVE":
            return self.receive_request(request)
