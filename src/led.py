import threading


class Led(threading.Thread):

    def __init__(self, queue):
        # init threading
        threading.Thread.__init__(self)
        # queue
        self.queue = queue

    def run(self):
        print "Starting queue thread"
        self.get_led_data()
        print "Exiting queue thread"

    def get_led_data(self):
        while True:
            print self.queue.get()