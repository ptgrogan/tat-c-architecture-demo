from tatc import Architecture
from tatc import TradespaceSearch
import argparse
import os
import csv
import json

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
        writer.writerow([
            'eventIdx', 'POI index', 'Lat[deg]', 'Long[deg]',
            'Access From [s]', 'Access To [s]'
        ])
    with open(os.path.join(arch_dir, 'gbl.json'), 'w', newline='') as outfile:
        json.dump({
            "Time" : {"min" : 0, "max" : 0},
            "TimeToCoverage" : {"min": 0, "max": 0, "avg": 0},
            "AccessTime" : {"min": 0, "max": 0, "avg": 0},
            "RevisitTime" : {"min": 0, "max": 0, "avg": 0},
            "ResponseTime" : {"min": 0, "max": 0, "avg": 0},
            "Coverage" : 0,
            "NumOfPOIpasses" : {"min": 0, "max": 0, "avg": 0},
            "DataLatency" : {"min": 0, "max": 0, "avg": 0},
            "NumGSpassesPD" : 0,
            "TotalDownlinkTimePD" : 0,
            "DownlinkTimePerPass" : {"min": 0, "max": 0, "avg": 0}
        }, outfile, indent=2)
    with open(os.path.join(arch_dir, 'lcl.csv'), 'w', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerow([
            "Time [s]", "", "POI", "[deg]", "[deg]", "[km]",
            "AccessTime [s]", "", "", "RevisitTime [s]", "", "", "ResponseTime [s]", "", "",
            "TimeToCoverage [s]", "Number of Passes"
        ])
        writer.writerow([
            "t0", "t1", "POI", "lat", "lon", "alt", "ATavg", "ATmin", "ATmax",
            "RvTavg", "RvTmin", "RvTmax", "RpTavg", "RpTmin", "RpTmax", "TCcov", "numPass"
        ])
    for i, satellite in enumerate(arch.constellation[0].satellites):
        with open(os.path.join(arch_dir, 'obs-{:d}.csv'.format(i)), 'w', newline='') as outfile:
            writer = csv.writer(outfile)
            writer.writerow([
                "Time[s]", "Ecc[deg]", "Inc[deg]", "SMA[km]", "AOP[deg]",
                "RAAN[deg]", "MA[deg]", "Lat[deg]", "Lon[deg]", "Alt[km]"
            ])
        with open(os.path.join(arch_dir, 'satellite_states-{:d}.csv'.format(i)), 'w', newline='') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(["Time[s]", "x[km]", "y[km]", "z[km]", "vx[km/s]", "vy[km/s]", "vz[km/s]"])

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
