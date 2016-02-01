import threading
import time
import requests
import json
import datetime


class Monitor(threading.Thread):

    def __init__(self, queue, base_url, testing_key, production_key, name, rbl, time_from, time_to, *args):
        # init threading
        threading.Thread.__init__(self)
        # exit flag
        self.exit_flag = False
        # init params
        self.queue = queue
        self.base_url = base_url
        self.testing_key = testing_key
        self.production_key = production_key
        self.name = name
        self.rbl = rbl
        self.time_from = time_from
        self.time_to = time_to
        self.args = args
        self.old_departure_time = -1

    def run(self):
        print "Starting thread for " + self.name + "\n"
        self.get_monitor_data(self.name, 5)
        print "Exiting thread for " + self.name + "\n"

    def get_monitor_data(self, name, delay):
        skips = 0
        while True:
            if self.exit_flag:
                break
            if skips > 10:
                now = datetime.datetime.now().time()
                now = datetime.datetime.strptime(str(now), "%H:%M:%S.%f").time()

                if not self._time_in_range(self.time_from, self.time_to, now):
                    diff = self.time_from.hour - now.hour
                    if diff < 0:
                        diff += 24
                    print "Line " + name + " out of order. Going to nap for a while."
                    time.sleep(3600*diff)
                    skips = 0

            # call API
            try:
                params = {"rbl": self.rbl, "sender": self.production_key}
                res = requests.get(url=self.base_url, params=params)
                data = json.loads(res.text)
            except:
                print "Could not reach server. Sleep for one minute, then retry."
                time.sleep(60)

            # validate
            if data["data"].get("monitors") is None:
                print "No monitors found in data"
                continue

            for monitor in data["data"]["monitors"]:

                # validate
                if monitor.get("lines") is None:
                    print "No lines found in monitor"
                    break

                for line in monitor["lines"]:

                    # validate and get departure time
                    if line.get("name") is not None and line["name"] == name:
                        departure = line["departures"]["departure"][0]
                        departure_time = departure["departureTime"]["countdown"]
                        # set old departure time
                        if departure_time != self.old_departure_time:
                            # queue information
                            info = {
                                "info": {
                                    "name": name,
                                    "time": departure_time
                                }
                            }
                            self.queue.put(info)
                            self.old_departure_time = departure_time
                            break
                    else:
                        skips += 1
                        continue

            # sleep 10 seconds until next call
            time.sleep(delay)

    @staticmethod
    def _time_in_range(start, end, t):
        if start <= end:
            return start <= t <= end
        else:
            return start <= t or time <= end
