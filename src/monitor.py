import threading
import time
import requests
import json


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

    def get_monitor_data(self, thread_name, delay):
        while True:
            if self.exit_flag:
                break
            # call API
            r = requests.get('http://www.wienerlinien.at/ogd_realtime/monitor?rbl=1346&sender=Fpo1lsUW9i')
            data = json.dumps(r.text)
            print data
            time.sleep(delay)
            self.exit_flag = True