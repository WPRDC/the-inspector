import sys, csv
from datetime import datetime, timedelta
from dateutil import parser

from pprint import pprint

# Currently this script just provides enough code to take a CSV file (and
# the field name that identifies a date in each recource) and check 
# whether there is at least one record on each day in the range from the
# earliest date in the field to the latest date. Temporal gaps are
# identified and reported on through console output.

# This simple check could be applied as a data validator to 
# any tabular data (and CKAN datastore tables in particular)
# as one of a toolbox of assertions to check to evaluate 
# data quality.

def find_gaps(filepath,field_name=None):
    # Find the gaps in date-stamped records for the CSV file at filepath.
    with open(filepath) as f:
        dates = []
        if field_name is not None:
            list_of_ds = csv.DictReader(f) 
            pprint(list_of_ds)
            for d in list_of_ds:
                datestring = d[field_name]
                dates.append(parser.parse(datestring))

    sorted_dates = sorted(list(set(dates)))

    k = 0
    count = 0
    total_days = timedelta(days = 0)
    while k < len(sorted_dates) - 1:
        gap = sorted_dates[k+1] - sorted_dates[k]
        if gap != timedelta(days=1):
            print("The gap between {} and {} is {}.".format(sorted_dates[k+1], sorted_dates[k], gap))
            count += 1
            total_days += gap
        k += 1

    print("{} distinct gaps were found, totalling {} days.".format(count,total_days))

    
def main():
    # Load CSV file (from sys.argv) and field name
    if len(sys.argv) == 1:
        raise ValueError("Please specify at least the CSV filepath (and optionally the field name corresponding to the date field to check).")
    filepath = sys.argv[1]
    field_name = None
    if len(sys.argv) > 2:
        field_name = sys.argv[2]
    find_gaps(filepath,field_name)

main()
