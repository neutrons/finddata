#!/usr/bin/env python3
import json
import logging
import os
import sys

from urllib3 import PoolManager

from finddata import __version__

BASE_URL = "https://oncat.ornl.gov/"
FAILURE = "Failed to find data for {} {}"

# basic configuration of logging
LOGLEVELS = ["DEBUG", "INFO", "WARNING"]
lower_logs = [level.lower() for level in LOGLEVELS]
LOGLEVELS.extend(lower_logs)
del lower_logs
logging.basicConfig(format="%(levelname)s:%(message)s")

########################################################################


def parseInt(number):
    try:
        return int(number)
    except ValueError as e:
        logging.info("Invalid run numbers: %s" % str(e))

    return 0


def procNumbers(numbers):
    # simply see if it is an integer
    try:
        return [int(numbers)]
    except ValueError:
        pass

    # split on commas
    result = []
    for item in numbers.split(","):
        # if there is a dash then it is a range
        if "-" in item:
            item = [parseInt(i) for i in item.split("-")]
            item.sort()
            if item[0]:
                result.extend(range(item[0], item[1] + 1))
        else:
            item = parseInt(item)
            if item:
                result.append(item)

    return result


def getJson(endpoint):
    # make a request
    url = BASE_URL + endpoint
    http = PoolManager()
    req = http.request("GET", url, headers={"User-Agent": f"Finddata/{__version__}"})
    if req.status != 200:
        raise RuntimeError(f"{url} returned code={req.status}")

    # convert the result into json
    doc = req.data.decode()
    logging.debug("DOC:" + doc)
    return json.loads(doc)


def getInstruments(facility, withLower=False):
    """
    Hit ONCat to find out the list of instruments at the facility.
    """
    endpoint = f"api/instruments?facility={facility}"
    doc = getJson(endpoint)
    if len(doc) == 0:
        url = BASE_URL + endpoint
        raise RuntimeError(f"Failed to find instruments from {url}")

    # convert to actual instruments
    instr_str = [instrument["id"] for instrument in doc]
    logging.debug("converted %d locations to strings" % len(instr_str))

    if withLower:
        lower_instr = [instr.lower() for instr in instr_str]
        instr_str.extend(lower_instr)

    return instr_str


def getProposal(facility, instrument, run):
    """
    Get the proposal for a given run.
    """
    endpoint = (
        "api/datafiles"
        "?facility=%s"
        "&instrument=%s"
        "&ranges_q=indexed.run_number:%s"
        "&sort_by=ingested"
        "&sort_direction=DESCENDING"
        "&projection=experiment"
    )
    doc = getJson(endpoint % (facility, instrument, run))
    if not doc:
        return "Failed to find proposal"

    return doc[0]["experiment"]


def getRunsInProp(facility, instrument, proposal):
    endpoint = "api/experiments/%s?facility=%s&instrument=%s&projection=indexed"
    doc = getJson(endpoint % (proposal, facility, instrument))

    return doc["indexed"]["run_number"]["ranges"]


def getFileLoc(facility, instrument, runs):
    """
    Ping ONCat for the locations that the file might be at and convert them
    into usable paths.

    @return The first path that works (as suggested by ONCat) or None.
    """
    logging.info(f"Looking for {facility}/{instrument} runs {runs}")
    endpoint = (
        "api/datafiles"
        "?facility={}"
        "&instrument={}"
        "&ranges_q=indexed.run_number:{}"
        "&sort_by=ingested"
        "&tags=type/raw"
        "&sort_order=DESCENDING"
        "&projection=location"
        "&projection=indexed"
    )

    rundescr = ",".join([str(runid) for runid in runs])
    doc = getJson(endpoint.format(facility, instrument, rundescr))
    if len(doc) == 0:
        return [None]

    # convert result a list of tuples for files that exist
    result = [
        (str(record["location"]), record["indexed"]["run_number"])
        for record in doc
        if os.path.exists(record["location"])
    ]

    # convert the list into dict(run number, file location)
    locations = {}
    for location, runid in result:
        locations[runid] = location
    logging.debug(f"ONCAT returned locations (that exist): {locations}")

    # put together a list of what was found
    result = []
    for runid in runs:
        if runid in locations:
            result.append(locations[runid])
        else:
            result.append(FAILURE.format(instrument, runid))

    return result


########################################################################


def main():
    FACILITY = {}
    for facility in ["HFIR", "SNS"]:
        instruments = getInstruments(facility, withLower=True)
        for instrument in instruments:
            FACILITY[instrument] = facility

    # set up optparse
    import argparse  # for command line options

    try:
        import argcomplete  # for bash completion
    except ImportError:
        argcomplete = None
    parser = argparse.ArgumentParser(description="Find data files using ICAT")

    parser.add_argument("inst", nargs="?", help="Specify the instrument name", choices=FACILITY.keys())
    parser.add_argument("runs", nargs="*", help="Specify the run numbers")
    parser.add_argument(
        "-l",
        "--loglevel",
        dest="loglevel",
        default="WARNING",
        choices=LOGLEVELS,
        help="Specify the log level (default=%(default)s)",
    )
    parser.add_argument(
        "-v", "--version", dest="version", action="store_true", help="Print the version information and exit"
    )
    parser.add_argument("--getproposal", dest="getproposal", action="store_true", help="Show the proposal for the run")
    parser.add_argument("--listruns", dest="listruns", help="List all of the runs in a proposal")

    # set up bash completion
    if argcomplete:
        argcomplete.autocomplete(parser)
    # parse the command line
    options = parser.parse_args()

    # reset logging to correct level
    options.loglevel = options.loglevel.upper()
    options.loglevel = getattr(logging, options.loglevel.upper(), logging.WARNING)
    logging.getLogger().setLevel(options.loglevel)

    # log the options and arguments
    logging.debug("options " + str(options))

    # if they want the version just give it back and exit
    if options.version:
        print("finddata version " + __version__)
        sys.exit(0)

    if not options.inst:
        parser.error("Failed to specify an instrument")
    options.inst = options.inst.upper()
    options.facility = FACILITY[options.inst]

    # convert the run numbers into a list of integers
    runnumbers = []
    for arg in options.runs:
        runnumbers.extend(procNumbers(arg))

    if options.listruns:
        # is actual the proposal number
        print(getRunsInProp(options.facility, options.inst, options.listruns))
        sys.exit(0)

    if len(runnumbers) <= 0:
        parser.error("Failed to specify any runs")

    # do the actual searching
    if options.getproposal:
        multiRun = len(runnumbers) > 1
        for run in runnumbers:
            result = getProposal(options.facility, options.inst, run)
            if multiRun:
                print(
                    run,
                )
            print(result)
    else:
        runnumbers = list(set(runnumbers))  # get rid of duplicates
        runnumbers.sort()  # and put them in order

        for location in getFileLoc(options.facility, options.inst, runnumbers):
            print(location)


if __name__ == "__main__":
    main()
