import threading
import time
import requests
import json
import pprint
from pydash import py_


class Monitor(threading.Thread):

    def __init__(self, base_url, testing_key, production_key, name, rbl, *args):
        # init threading
        threading.Thread.__init__(self)
        # exit flag
        self.exit_flag = False
        # init params
        self.base_url = base_url
        self.testing_key = testing_key
        self.production_key = production_key
        self.name = name
        self.rbl = rbl
        self.args = args

    def run(self):
        print "Starting thread for " + self.name
        self.get_monitor_data(self.name, 5)
        print "Exiting thread for " + self.name

    def get_monitor_data(self, name, delay):
        while True:
            if self.exit_flag:
                break

            # call API
            params = {"rbl": self.rbl, "sender": self.testing_key}
            res = requests.get(url=self.base_url, params=params)
            data = json.loads(res.text)

            # pretty print
            pp = pprint.PrettyPrinter(indent=4)
            # pp.pprint(data)

            for monitor in data["data"]["monitors"]:
                for line in monitor["lines"]:
                    if line["name"] == name:
                        departure = line["departures"]["departure"][0]
                        departure_time = departure["departureTime"]["countdown"]
                        print departure_time

            time.sleep(10)
            # self.exit_flag = True
