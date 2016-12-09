#!/usr/bin/env python
import json
import os

CONFIG_FILE = '/etc/autoreduce/post_processing.conf'

class Configuration(object):
    """
    Read and process configuration file and provide an easy way to create a configured Client object
    """
    def __init__(self, config_file):
        if os.access(config_file, os.R_OK) == False:
            raise RuntimeError, "Configuration file doesn't exist or is not readable: %s" % config_file
        cfg = open(config_file, 'r')
        json_encoded = cfg.read()
        config = json.loads(json_encoded)

        # Keep a record of which config file we are using
        self.config_file = config_file

        # plot publishing
        self.publish_url = config['publish_url_template'] if 'publish_url_template' in config else ''
        self.publisher_username = config['publisher_username'] if 'publisher_username' in config else ''
        self.publisher_password = config['publisher_password'] if 'publisher_password' in config else ''

def read_configuration(config_file=None):
    """
    Returns a new configuration object for a given
    configuration file
    @param config_file: configuration file to process
    """
    if config_file is None:
        # Make sure we have a configuration file to read
        config_file = CONFIG_FILE
        if os.access(config_file, os.R_OK) == False:
            raise RuntimeError("Configuration file doesn't exist or is not readable: %s" % CONFIG_FILE)

    return Configuration(config_file)

def loadDiv(filename):
    if not os.path.exists(filename):
        raise RuntimeError('\'%s\' does not exist' % filename)
    print 'loading \'%s\'' % filename
    with file(filename, 'r') as handle:
        div = handle.read()
    return div

def _getURL(url_template, instrument, run_number):
    import string
    url_template=string.Template(url_template)
    url = url_template.substitute(instrument=instrument,
                                  run_number=str(run_number))
    return url

def publish_plot(instrument, run_number, files, config=None):
    if config is None:
        config = read_configuration()

    run_number = str(run_number)
    url = _getURL(config.publish_url, instrument, run_number)
    print 'posting to \'%s\'' % url

    # these next 2 lines are explicity bad - and doesn't seem
    # to do ANYTHING
    # https://urllib3.readthedocs.org/en/latest/security.html
    import urllib3
    urllib3.disable_warnings()

    import requests
    request = requests.post(url, data={'username': config.publisher_username,
                                       'password': config.publisher_password},
                            files=files, verify=False)
    return request

if __name__ == '__main__':
    import sys
    div = loadDiv(sys.argv[1])
    name  = os.path.split(sys.argv[1])[-1]
    (instr, runnumber) = name.split('_')[:2]
    #print '**********'
    #print div

    config = read_configuration('post_processing.conf')
    request = publish_plot(instr, runnumber, {'file':div}, config)
    print 'request returned', request.status_code
