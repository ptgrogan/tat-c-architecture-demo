import argparse
import os, errno

import orbits_proxy
import cost_risk_proxy
import instrument_proxy
import launch_proxy

def execute(in_file, out_dir):
    """Executes the architecture evaluator."""
    orbits_proxy.execute(in_file, out_dir)
    instrument_proxy.execute(in_file, out_dir)
    cost_risk_proxy.execute(in_file, out_dir)
    launch_proxy.execute(in_file, out_dir)

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
        description='Run architecture evaluator'
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
