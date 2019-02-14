from tatc import Architecture
from tatc import TradespaceSearch
import argparse
import os
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

    with open(os.path.join(arch_dir, 'CostRisk_output.json'), 'w', newline='') as outfile:
        json.dump({
        	"groundCost" : { "estimate" : 0, "fiscalYear" : 0, "standardError" : 0 },
        	"hardwareCost" : { "estimate" : 0, "fiscalYear" : 0, "standardError" : 0 },
        	"iatCost" : { "estimate" : 0, "fiscalYear" : 0, "standardError" : 0 },
        	"launchCost" : { "estimate" : 0, "fiscalYear" : 0, "standardError" : 0 },
        	"lifecycleCost" : { "estimate" : 0, "fiscalYear" : 0, "standardError" : 0 },
            "nonRecurringCost" : { "estimate" : 0, "fiscalYear" : 0, "standardError" : 0 },
            "operationsCost" : { "estimate" : 0, "fiscalYear" : 0, "standardError" : 0 },
            "programCost" : { "estimate" : 0, "fiscalYear" : 0, "standardError" : 0 },
            "recurringCost" : { "estimate" : 0, "fiscalYear" : 0, "standardError" : 0 },
        	# "spacecraftRank" : [ { "fiscalYear" : 2019, "rank" : 0, "spacecraftIndex" : 0, "totalCost" : 0 } ],
        	"systemRisk" : [
                 { "category" : "Configuration Risks", "consequence" : 0, "likelihood" : 0, "risk" : "Risk of unforseen risk arising due to lack of flight heritage" },
                 { "category" : "Configuration Risks", "consequence" : 0, "likelihood" : 0, "risk" : "Risk of 'infant mortality' significantly reducing science return (due to extended on orbit checkouts, assuming a catastrophic failure does not occur)" },
                 { "category" : "Configuration Risks", "consequence" : 0, "likelihood" : 0, "risk" : "Risk that constellation does not observe intended coverage area following loss of one or more spacecraft" },
                 { "category" : "Configuration Risks", "consequence" : 0, "likelihood" : 0, "risk" : "Risk of collision with orbital debris" },
                 { "category" : "Configuration Risks", "consequence" : 0, "likelihood" : 0, "risk" : "Risk of interrupted installation" },
                 { "category" : "Configuration Risks", "consequence" : 0, "likelihood" : 0, "risk" : "Risk of constellation formation change due to atmospheric drag" },
                 { "category" : "Configuration Risks", "consequence" : 0, "likelihood" : 0, "risk" : "Risk of improper spacing between adjacent spacecraft due to atmospheric drag" },
                 { "category" : "Satellite Performance Risks", "consequence" : 0, "likelihood" : 0, "risk" : "Risk of instrument design flaw" },
                 { "category" : "Satellite Performance Risks", "consequence" : 0, "likelihood" : 0, "risk" : "Risk of instrument deployment failure" },
                 { "category" : "Satellite Performance Risks", "consequence" : 0, "likelihood" : 0, "risk" : "Risk of premature instrument failure" },
                 { "category" : "Spacecraft Risks", "consequence" : 0, "likelihood" : 0, "risk" : "Risk of radiation damage to spacecraft instrumentation" },
                 { "category" : "Power Subsystem Risks", "consequence" : 0, "likelihood" : 0, "risk" : "Risk of excessive power subsystem degradation over lifetime" },
                 { "category" : "Attitude Determination and Control Subsystem Risks", "consequence" : 0, "likelihood" : 0, "risk" : "Risk of improper attitude alignment" },
                 { "category" : "Propulsion Subsystem Risks", "consequence" : 0, "likelihood" : 0, "risk" : "Risk of fuel related accident (e.g. propellant tank rupture, propulsion subsystem failure)" },
                 { "category" : "Thermal Subsystem Risks", "consequence" : 0, "likelihood" : 0, "risk" : "Risk of thermal subsystem failure" }
             ]
         }, outfile, indent=2)

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
        description='Run cost and risk analysis (proxy)'
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
