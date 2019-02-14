from tatc import Architecture
from tatc import TradespaceSearch
import argparse
import os
import csv
import json

def execute(search_file, arch_dir, arch_file=None):
    """Executes the instrument analysis proxy."""
    search = TradespaceSearch.from_json(search_file)
    if arch_file is None:
        arch_path = os.path.join(arch_dir, '{0}.json'.format(arch_dir))
        with open(arch_path) as arch_file:
            arch = Architecture.from_json(arch_file)
    else:
        arch = Architecture.from_json(arch_file)

    ## TODO read orbital outputs
    with open(os.path.join(arch_dir, 'coverage_and_data_metrics_basic_sensor.csv'), 'w', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerow([
            "Access From [s]", "Access To [s]", "Lat[deg]", "Lon[deg]",
            "POI index", "eventIdx", "Coverage [T/F]", "Incidence angle [deg]",
            "Look angle [deg]", "Observation Range [km]"
        ])

    with open(os.path.join(arch_dir, 'coverage_and_data_metrics_optical_scanner.csv'), 'w', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerow([
            "Access From [s]", "Access To [s]", "Lat[deg]", "Lon[deg]",
            "POI index", "eventIdx", "Coverage [T/F]", "Incidence angle [deg]",
            "Look angle [deg]", "Observation Range [km]"
        ])
    with open(os.path.join(arch_dir, 'gbl_basic_sensor.json'), 'w', newline='') as outfile:
        json.dump({
            "IncidenceAngle" : {"min" : 0, "max" : 0},
            "LookAngle" : {"min": 0, "max": 0, "avg": 0},
            "ObservationRange" : {"min": 0, "max": 0, "avg": 0}
        }, outfile, indent=2)
    with open(os.path.join(arch_dir, 'lcl_basic_sensor.csv'), 'w', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerow([
            "POI index", "[deg]", "[deg]", "Incidence angle [deg]", "", "",
            "Look angle [deg]", "", "", "Observation Range [km]", "", ""
        ])
        writer.writerow([
            "POI", "lat", "lon", "min", "max", "avg", "min", "max", "avg", "min", "max", "avg"
        ])
    with open(os.path.join(arch_dir, 'gbl_optical_scanner.json'), 'w', newline='') as outfile:
        json.dump({
            "NoiseEquivalentDeltaT" : {"min": 0, "max": 0, "avg": 0},
            "DynamicRange" : {"min": 0, "max": 0, "avg": 0},
            "SignalToNoiseRatio" : {"min": 0, "max": 0, "avg": 0}
        }, outfile, indent=2)
    with open(os.path.join(arch_dir, 'lcl_optical_scanner.csv'), 'w', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerow([
            "POI index", "[deg]", "[deg]", "NoiseEquivalentDeltaT", "", "",
            "DynamicRange", "", "", "SignalToNoiseRatio", "", ""
        ])
        writer.writerow([
            "POI", "lat", "lon", "min", "max", "avg", "min", "max", "avg",
            "min", "max", "avg"
        ])
    with open(os.path.join(arch_dir, 'gbl_synthetic_aperture_radar.json'), 'w', newline='') as outfile:
        json.dump({
            "NoiseEquivalentSigma0" : {"min": 0, "max": 0, "avg": 0},
            "AlongTrackResolution" : {"min": 0, "max": 0, "avg": 0},
            "CrossTrackResolution" : {"min": 0, "max": 0, "avg": 0},
            "SwathWidth" : {"min": 0, "max": 0, "avg": 0},
            "IncidenceAngle" : {"min": 0, "max": 0, "avg": 0}
        }, outfile, indent=2)
    with open(os.path.join(arch_dir, 'lcl_synthetic_aperture_radar.csv'), 'w', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerow([
            "POI index", "[deg]", "[deg]", "NoiseEquivalentSigma0", "", "",
            "AlongTrackResolution", "", "", "CrossTrackResolution", "", "",
            "SwathWidth", "", "", "IncidenceAngle", "", ""
        ])
        writer.writerow([
            "POI", "lat", "lon", "min", "max", "avg", "min", "max", "avg",
            "min", "max", "avg", "min", "max", "avg", "min", "max", "avg"
        ])

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
        description='Run instrument analysis (proxy)'
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
