#!/usr/bin/env python
import json
import logging
import os

try:
    from postprocessing.Configuration import Configuration, CONFIG_FILE, CONFIG_FILE_ALTERNATE
except ImportError:
    CONFIG_FILE = '/etc/autoreduce/post_processing.conf'
    CONFIG_FILE_ALTERNATE = 'post_processing.conf'

    class Configuration(object):
        """
        Read and process configuration file and provide an easy
        way to hold the various options for a client. This is a
        heavily abridged version of what is found in postprocessing.
        """
        def __init__(self, config_file):
            if os.access(config_file, os.R_OK) == False:
                raise RuntimeError, "Configuration file doesn't exist or is not readable: %s" % config_file
            with open(config_file, 'r') as cfg:
                json_encoded = cfg.read()
            config = json.loads(json_encoded)

            # Keep a record of which config file we are using
            self.config_file = config_file

            # plot publishing
            self.publish_url = config['publish_url_template'] if 'publish_url_template' in config else ''
            self.publisher_username = config['publisher_username'] if 'publisher_username' in config else ''
            self.publisher_password = config['publisher_password'] if 'publisher_password' in config else ''

def _determine_config_file(config_file):
    # put together the list of all choices
    choices = [config_file, CONFIG_FILE, CONFIG_FILE_ALTERNATE]

    # filter out bad choices
    choices = [name for name in choices
               if not name is None]
    choices = [name for name in choices
               if len(name) > 0]
    choices = [name for name in choices
               if os.access(name, os.R_OK)]

    # first one is a winner
    if len(choices) > 0:
        return choices[0]
    else:
        return None

def read_configuration(config_file=None):
    """
    Returns a new configuration object for a given
    configuration file
    @param config_file: configuration file to process
    """
    config_file = _determine_config_file(config_file)
    if config_file is None:
        raise RuntimeError('Failed to find Configuration file')

    logging.info('Loading configuration \'%s\'' % config_file)
    return Configuration(config_file)

def _loadDiv(filename):
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
    # read the configuration if one isn't provided
    if config is None:
        config = read_configuration()
    # verify that it has an attribute that matters
    try:
        config.publish_url
    except AttributeError: # assume that it is a filename
        config = read_configuration(config)

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
    div = _loadDiv(sys.argv[1])
    #print '**********'
    #print div

    # run information is generated from the filename
    name  = os.path.split(sys.argv[1])[-1]
    (instr, runnumber) = name.split('_')[:2]

    config = read_configuration('post_processing.conf')
    #config = read_configuration('post_processing_full.conf')
    request = publish_plot(instr, runnumber, {'file':div}, config)
    print 'request returned', request.status_code
