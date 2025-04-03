class Request:
    def __init__(self, tp, time, person, floor, start, end, elevator, speed):
        self.tp = tp
        self.time = int(time) if time is not None else None
        self.person = int(person) if person is not None else None
        self.floor = int(floor) if floor is not None else None
        self.start = int(start) if start is not None else None
        self.end = int(end) if end is not None else None
        self.elevator = int(elevator) if elevator is not None else None
        self.speed = int(speed) if speed is not None else None

    def __str__(self):
        return type(self).__name__ + ": " + str(self.__dict__)
