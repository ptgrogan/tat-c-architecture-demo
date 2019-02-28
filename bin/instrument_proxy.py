import tatc
import argparse
import os
import csv
import json

"""
The instrument analysis proxy analyzes instrument performance for a given
architecture. It takes two arguments as inputs:
    in_file     A JSON formatted document containing the TradespaceSearch.
    arch_dir    A readable directory containing a JSON formatted document
                containing the Architecture (arch.json) and the location where
                all analysis outputs shall be written.

Instrument analysis writes the following files to the architecture directory:
    coverage_basic_sensor-#.csv  CSV-formatted list of coverage periods
                for a basic sensor-type instrument (1 file per satellite,
                sequential integer ids).
    gbl_basic_sensor.json JSON-formatted document of global performance measures
                for the constellation assuming basic sensor-type instruments.
    lcl_basic_sensor.csv CSV-formatted list of all performance measures local
                to a point of interest for the constellation assuming basic
                sensor-type instruments.
    coverage_optical_scanner-#.csv CSV-formatted list of coverage periods
                for an optical scanner-type instrument (1 file per satellite,
                sequential integer ids).
    gbl_optical_scanner.json JSON-formatted document of global performance
                measures for the constellation assuming optical scanner-type
                instruments.
    lcl_optical_scanner.csv CSV-formatted list of all performance measures local
                to a point of interest for the constellation assuming optical
                scanner-type instruments.
    coverage_synthetic_aperture_radar-#.csv CSV-formatted list of coverage
                periods for a synthetic aperture radar-type instrument (1 file
                per satellite, sequential integer ids).
    gbl_synthetic_aperture_radar.json JSON-formatted document of global
                performance measures for the constellation assuming synthetic
                aperture radar-type instruments.
    lcl_synthetic_aperture_radar.csv CSV-formatted list of all performance
                measures local to a point of interest for the constellation
                assuming synthetic aperture radar-type instruments.
"""

def execute(in_file, arch_dir):
    """Executes the instrument analysis proxy."""
    in_file.seek(0) # reset reading from start of file
    search = tatc.TradespaceSearch.from_json(in_file)
    arch_path = os.path.join(arch_dir, 'arch.json')
    with open(arch_path, 'r') as arch_file:
        arch = tatc.Architecture.from_json(arch_file)

    ## TODO read orbital outputs
    for i, satellite in enumerate(arch.constellation[0].satellites):
        with open(os.path.join(arch_dir, 'coverage_basic_sensor-{:d}.csv'.format(i)), 'w', newline='') as outfile:
            writer = csv.writer(outfile)
            writer.writerow([
                "Access From [s]", "Access To [s]", "Lat[deg]", "Lon[deg]",
                "POI index", "eventIdx", "Coverage [T/F]", "Incidence angle [deg]",
                "Look angle [deg]", "Observation Range [km]"
            ])
        with open(os.path.join(arch_dir, 'coverage_optical_scanner-{:d}.csv'.format(i)), 'w', newline='') as outfile:
            writer = csv.writer(outfile)
            writer.writerow([
                "Access From [s]", "Access To [s]", "Lat[deg]", "Lon[deg]",
                "POI index", "eventIdx", "Coverage [T/F]", "Noise-Equivalent Delta T",
                "DR", "SNR", "Ground Pixel Along-Track Resolution [m]",
                "Ground Pixel Cross-Track Resolution [m]"
            ])
        with open(os.path.join(arch_dir, 'coverage_synthetic_aperture_radar-{:d}.csv'.format(i)), 'w', newline='') as outfile:
            writer = csv.writer(outfile)
            writer.writerow([
                "Access From [s]", "Access To [s]", "Lat[deg]", "Lon[deg]",
                "POI index", "eventIdx", "Coverage [T/F]", "Noise-Equivalent Sigma Naught",
                "Ground Pixel Along-Track Resolution [m]",
                "Ground Pixel Cross-Track Resolution [m]", "Swath Width [m]",
                "Incidence angle [deg]"
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
            "AlongTrackResolution" : {"min": 0, "max": 0, "avg": 0},
            "CrossTrackResolution" : {"min": 0, "max": 0, "avg": 0},
            "DynamicRange" : {"min": 0, "max": 0, "avg": 0},
            "SignalToNoiseRatio" : {"min": 0, "max": 0, "avg": 0}
        }, outfile, indent=2)
    with open(os.path.join(arch_dir, 'lcl_optical_scanner.csv'), 'w', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerow([
            "POI index", "[deg]", "[deg]", "NoiseEquivalentDeltaT", "", "",
            "AlongTrackResolution", "", "", "CrossTrackResolution", "", "",
            "DynamicRange", "", "", "SignalToNoiseRatio", "", ""
        ])
        writer.writerow([
            "POI", "lat", "lon", "min", "max", "avg", "min", "max", "avg",
            "min", "max", "avg", "min", "max", "avg", "min", "max", "avg"
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
        'infile',
        type = argparse.FileType('r'),
        help = "Tradespace search input JSON file"
    )
    parser.add_argument(
        'archdir',
        action = readable_dir,
        help = "Architecture directory to read inputs/write outputs"
    )
    args = parser.parse_args()
    execute(args.infile, args.archdir)
