import ConfigParser
from ConfigParser import SafeConfigParser
from monitor import Monitor
import datetime


def main():
    # init parser
    parser = SafeConfigParser()
    parser.read('../config/api.ini')

    # get API entry
    if parser.has_section('API'):
        try:
            base_url = parser.get('API', 'base_url')
            testing_key = parser.get('API', 'testing_key')
            production_key = parser.get('API', 'production_key')
        except ConfigParser.NoOptionError as e:
            print "Something missing in API config: " + e.message
            return
    else:
        print "API section missing in config"
        return

    # loop over config and pass oeffis to workers
    parser = SafeConfigParser()
    parser.read('../config/oeffis.ini')
    threads = []
    for section_name in parser.sections():
        # must be in config
        try:
            name = parser.get(section_name, "name")
            rbl = parser.get(section_name, "rbl")
            time_from = parser.get(section_name, "time_from")
            time_to = parser.get(section_name, "time_to")
            # time conversion
            time_from = datetime.datetime.strptime(time_from, "%H:%M:%S.%f").time()
            time_to = datetime.datetime.strptime(time_to, "%H:%M:%S.%f").time()
        except ConfigParser.NoOptionError as e:
            print "Something missing in " + section_name + " config:" + e.message
            continue

        # threading
        thread = Monitor(base_url, testing_key, production_key, name, rbl, time_from, time_to)
        thread.start()
        threads.append(thread)

    # join threads
    for t in threads:
        t.join()

    print "Exiting rando. All threads stopped."


if __name__ == '__main__':
    main()