from tatc import Architecture
from tatc import TradespaceSearch
import argparse
import os
import csv

def execute(search_file, arch_dir, arch_file=None):
    """Executes the orbital analysis proxy."""
    search = TradespaceSearch.from_json(search_file)
    if arch_file is None:
        arch_path = os.path.join(arch_dir, '{0}.json'.format(arch_dir))
        with open(arch_path) as arch_file:
            arch = Architecture.from_json(arch_file)
    else:
        arch = Architecture.from_json(arch_file)
    with open(os.path.join(arch_dir, 'access.csv'), 'w', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(['Lat[deg]', 'Long[deg]', 'Access From [s]', 'Access To [s]'])
    with open(os.path.join(arch_dir, 'gbl.csv'), 'w', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(["Time [s]", "", "TimeToCoverage [s]", "", "", "AccessTime [s]", "", "", "RevisitTime [s]", "", "", "Coverage", "NumOfPOIpasses", "", "", "Data Latency [s]", "", "", "NumGSpassesPD", "TotalDownlinkTimePD [s]", "DownlinkTimePerPass [s]", "", "", "CrossSwath[km]", "", "", "AlongSwath [km]", "", "", "SpatialResolution [m]", ""])
        writer.writerow(["t0", "t1", "TCavg", "TCmin", "TCmax", "ATavg", "ATmin", "ATmax", "RTavg", "RTmin", "RTmax", "% Grid Covered", "PASavg", "PASmin", "PASmax", "DLavg", "DLmin", "DLmax", "PassesPerDay", "DLTimePerDay", "DLTavg", "DLTmin", "DLTmax", "CSavg", "CSmin", "CSmax", "ASavg", "ASmin", "ASmax", "SRmin", "SRmax"])
    with open(os.path.join(arch_dir, 'lcl.csv'), 'w', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(["Time [s]", "", "POI", "[deg]", "[deg]", "[km]", "AccessTime [s]", "", "", "RevisitTime [s]", "", "", "TimeToCoverage [s]", "Number of Passes"])
        writer.writerow(["t0", "t1", "POI", "lat", "lon", "alt", "ATavg", "ATmin", "ATmax", "RvTavg", "RvTmin", "RvTmax", "TCcov", "numPass"])

class readable_dir(argparse.Action):
    """Defines a custom argparse Action to identify a readable directory."""
    def __call__(self, parser, namespace, values, option_string=None):
        prospective_dir = values
        if not os.path.isdir(prospective_dir):
            raise argparse.ArgumentTypeError(
                '{0} is not a valid path'.format(prospective_dir)
            )
        if os.access(prospective_dir, os.R_OK):
            setattr(namespace,self.dest,prospective_dir)
        else:
            raise argparse.ArgumentTypeError(
                '{0} is not a readable dir'.format(prospective_dir)
            )

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Run orbital analysis (proxy)'
    )
    parser.add_argument(
        'search',
        type = argparse.FileType('r'),
        help = "Tradespace search input JSON file"
    )
    parser.add_argument(
        'archdir',
        action = readable_dir,
        help = "Architecture directory to write outputs"
    )
    parser.add_argument(
        'archfile',
        nargs = '?',
        type = argparse.FileType('r'),
        help = "Architecture input JSON file"
    )
    args = parser.parse_args()
    execute(args.search, args.archdir, args.archfile)
