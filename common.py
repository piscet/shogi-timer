class Prob:
    def __init__(self, number, max_time = -1):
        self.max_time = max_time
        self.timeout = (self.max_time > 0)
        self.number = number
        self.isSolve = ""
        self.time_m = 0
        self.time_s = 0
        self.time = None


    def add_time(self, _time):
        if not self.timeout or _time < self.max_time:
            self.isSolve = ''
        else:
            self.isSolve = 'T'
        
        self.time_m, self.time_s = _time // 60, _time % 60
        self.time = _time
    
    def add_result(self, isSolve):
        if self.time is None:
            raise Exception("時間を入力してください")
        if not isSolve:
            self.isSolve = 'x'

    def isSolve_int(self):
        return self.isSolve == ''

    def __str__(self):
        return "{:2} - {:2}:{:0>2}".format(
            self.number,
            self.time_m,
            self.time_s
        ) + (
            " " + self.isSolve if self.isSolve != "o" else ""
        )