import threading
import time


exitFlag = False


class Monitor(threading.Thread):

    def __init__(self, base_url, testing_key, production_key, name, rbl, *args):
        # init threading
        threading.Thread.__init__(self)
        # init params
        self.base_url = base_url
        self.testing_key = testing_key
        self.production_key = production_key
        self.name = name
        self.rbl = rbl
        self.args = args

    def run(self):
        print "Starting thread for " + self.name
        self.get_monitor_data(self.name, 3)
        print "Exiting thread for " + self.name

    @staticmethod
    def get_monitor_data(thread_name, delay):
        while True:
            if exitFlag:
                thread_name.exit()
            time.sleep(delay)
            print "Calling API " + thread_name