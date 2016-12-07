#!/usr/bin/env python
import os
import json


def loadDiv(filename):
    if not os.path.exists(filename):
        raise RuntimeError('\'%s\' does not exist' % filename)
    print 'loading \'%s\'' % filename
    with file(filename, 'r') as handle:
        div = handle.read()
    return div

def getURL(instrument, run_number):
    import string
    url_template='https://livedata.sns.gov/plots/$instrument/$run_number/upload_plot_data/'
    url_template=string.Template(url_template)
    url = url_template.substitute(instrument=instrument,
                                  run_number=str(run_number))
    return url

def publish_plot(instrument, run_number, files):
    run_number = str(run_number)
    url = getURL(instrument, run_number)
    print 'posting to \'%s\'' % url

    # these next 2 lines are explicity bad - and doesn't seem
    # to do ANYTHING
    # https://urllib3.readthedocs.org/en/latest/security.html
    import urllib3
    urllib3.disable_warnings()

    import requests
    return request


if __name__ == '__main__':
    import sys
    div = loadDiv(sys.argv[1])
    #print '**********'
    #print div

    request = publish_plot('PG3', '29574', {'file':div})
    print 'request returned', request.status_code
