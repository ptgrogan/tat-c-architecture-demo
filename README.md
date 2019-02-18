TAT-C Architecture Demo
=======================

This project contains an architectural interface specification for the TAT-C project. It is organized in two pieces:
 1. TAT-C interface library (`tatc/`)
 2. Python executables (`bin/`)

The interface library contains Python classes to read/write to JSON files and perform basic validation including assigning default values.

The executables include proxy scripts to simulate module-specific behavior and generate output files representative of module outputs.

## Installation

This project was designed for Python 3.7 but should also be compatible with Python 2.7. It requires the following non-standard (to Anaconda) packages:
 - `isodate`
 - `enum34` (for Python 2.X)

To make the `tatc` library visible to the Python interpreter, from the project root directory (containing `setup.py`), run:
```shell
pip install -e .
```
where the trailing period (`.`) indicates to install from the current directory.

## Testing

This project includes unit tests with substantial (though not complete) coverage of the interface specification. To run using `nosetests` module, run from the command line:

```shell
python -m nose
```

## Usage

Executable scripts are provided in the `bin/` directory.

### Generate Landsat 8

Generates a tradespace search file based on the Landsat 8 validation case:
```shell
python bin/gen_landsat8.py [outfile]
```
where `outfile` defaults to `landsat8.json`.

Example usage:
```shell
mkdir example
python bin/gen_landsat8.py example/landsat8.json
```
Outputs:
```
|-- bin/
|-- example/
    |-- landsat8.json
|-- tatc/
```

### Tradespace Search Executive (TSE)

Executes a full-factorial tradespace search including enumeration (generating architectures) and evaluation (generating outputs for each architecture):
```shell
python bin/tse.py infile [outdir]
```
where `infile` specifies the tradespace search input JSON file and `outdir` specifies the output directory to write architectures (defaults to `.`).

Example usage:
```shell
python bin/tse.py example/landsat8.json example/
```
Outputs:
```
|-- bin/
|-- example/
    |-- landsat8.json
    |-- arch-0/
        |-- arch.json
        |-- ...(outputs)...
    |-- arch-1/
        |-- arch.json
        |-- ...(outputs)...
    |-- arch-2/
        |-- arch.json
        |-- ...(outputs)...
|-- tatc/
```

### Architecture Evaluator

Evaluates an architecture by orchestrating all analysis modules:
```shell
python bin/arch_eval.py infile archdir
```
where `infile` specifies the tradespace search input JSON file, `archdir` specifies the architecture directory to read the architecture input JSON file (`arch.json`) and write analysis outputs.

Example usage:
```shell
python bin/arch_eval.py example/landsat8.json example/arch-1
```
Outputs:
```
|-- bin/
|-- example/
    |-- landsat8.json
    |-- arch-0/
    |-- arch-1/
        |-- arch.json
        |-- ...(outputs)...
    |-- arch-2/
|-- tatc/
```

### Analysis Proxy

Executes a proxy version of an analysis module (orbits, launch, instrument, or cost and risk):
```shell
python bin/orbits_proxy.py infile archdir
python bin/launch_proxy.py infile archdir
python bin/instrument_proxy.py infile archdir
python bin/cost_risk_proxy.py infile archdir
```
where `infile` specifies the tradespace search input JSON file, `archdir` specifies the architecture directory to read the architecture input JSON file (`arch.json`) and any other dependent files and write analysis outputs.

Example usage:
```shell
python bin/orbits_proxy.py example/landsat8.json example/arch-1
```
Outputs:
```
|-- bin/
|-- example/
    |-- landsat8.json
    |-- arch-0/
    |-- arch-1/
        |-- arch.json
        |-- ...(outputs)...
    |-- arch-2/
|-- tatc/
```

### Tradespace Search Validator (TSV)

Performs routine validation of a tradespace search document by reading JSON into Python, assigning any default values and removing unknown keys, and writing JSON back to file:
```shell
python bin/tsv.py infile outfile
```
where `infile` specifies the tradespace search input JSON file and `outdir` specifies the output directory to write architectures (defaults to `.`).

Example usage:
```shell
echo {} > example/blank.json
python bin/tsv.py example/blank.json example/default.json
```
Outputs:
```
|-- bin/
|-- example/
    |-- blank.json
    |-- default.json
|-- tatc/
```
