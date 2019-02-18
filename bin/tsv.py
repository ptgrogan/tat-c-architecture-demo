from tatc import Architecture
from tatc import TradespaceSearch
import argparse
import os
import json

def execute(search_file, out_file):
    """Executes the tradespace search validator."""
    search = TradespaceSearch.from_json(search_file)
    search.to_json(out_file, indent=2)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Run tradespace search validator'
    )
    parser.add_argument(
        'search',
        type = argparse.FileType('r'),
        help = "Tradespace search input JSON file"
    )
    parser.add_argument(
        'outfile',
        type = argparse.FileType('w'),
        help = "Validated tradespace search JSON file"
    )
    args = parser.parse_args()
    execute(args.search, args.outfile)
