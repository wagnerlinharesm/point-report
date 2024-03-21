class Point:
    def __init__(self, situation, date, work_time, periods=None):
        if periods is None:
            periods = []

        self.situation = situation
        self.date = date
        self.work_time = work_time
        self.periods = periods

    def add_period(self, period):
        self.periods.append(period)

