import ConfigParser
from ConfigParser import SafeConfigParser
import monitor


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
            print ">> Something missing in API config: " + e.message
            return
    else:
        print ">> API section missing in config"
        return

    # loop over config and pass oeffis to workers
    parser = SafeConfigParser()
    parser.read('../config/oeffis.ini')
    for section_name in parser.sections():
        # must be in config
        try:
            name = parser.get(section_name, "name")
            rbl = parser.get(section_name, "rbl")
        except ConfigParser.NoOptionError as e:
            print ">> Something missing in " + section_name + " config:" + e.message
            return

        # start worker
        print base_url
        print testing_key
        print production_key
        print name
        print rbl


if __name__ == '__main__':
    main()