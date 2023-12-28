import time
from IO import Writer


class Timer:

    intervals = {}

    def start_timer(self, process_name):

        interval = [time.time()]
        self.intervals[process_name] = interval

    def stop_timer(self, process_name):

        self.intervals[process_name].append(time.time())

    def get_intervals(self):

        time_intervals = {}
        # return self.intervals
        for key, value in self.intervals.items():
            time_intervals[key] = value[1] - value[0]

        return time_intervals
