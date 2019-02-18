import tatc
import argparse
import os, errno

import orbits_proxy
import cost_risk_proxy
import instrument_proxy
import launch_proxy
import arch_eval

def execute(in_file, out_dir):
    """Executes the example tradespace search executive."""
    search = tatc.TradespaceSearch.from_json(in_file)
    for i, architecture in enumerate(search.designSpace.generate_architectures()):
        arch_label = 'arch-{:}'.format(i)
        arch_dir = os.path.join(out_dir, arch_label)
        try:
            # try to create directory (checking in advance exposes race condition)
            os.makedirs(arch_dir)
        except OSError as e:
            # ignore error if directory already exists
            if e.errno != errno.EEXIST:
                raise
        with open(os.path.join(arch_dir, 'arch.json'), 'w') as out_file:
            architecture.to_json(out_file, indent=2)
        with open(os.path.join(arch_dir, 'arch.json'), 'r') as arch_file:
            arch_eval.execute(in_file, arch_dir)

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
        description='Run tradespace search executive'
    )
    parser.add_argument(
        'infile',
        type = argparse.FileType('r'),
        help = "Tradespace search input JSON file"
    )
    parser.add_argument(
        'outdir',
        nargs = '?',
        action = readable_dir,
        default = '.',
        help = "Architecture output directory"
    )
    args = parser.parse_args()
    execute(args.infile, args.outdir)
