import tatc
import argparse

def build_example_tradespace_search():
    """ Builds an example TradespaceSearch based on SLI mission."""
    mission = tatc.MissionConcept(
        name="Sustainable Land Imaging - Landsat 8",
        acronym="SLI-Landsat8",
        agency=tatc.Agency(tatc.AgencyType.GOVERNMENT),
        start="2017-08-01T00:00:00Z",
        duration="P0Y0M90D",
        target=tatc.Region(
            latitude=tatc.QuantitativeValue(35, 45),
            longitude=tatc.QuantitativeValue(-115,-100)
        )
    )
    designSpace = tatc.DesignSpace(
        constellations=[
            tatc.Constellation(
                constellationType="DELTA_HOMOGENOUS",
                numberSatellites=[1,2],
                numberPlanes=[1,2],
                orbit=tatc.Orbit(
                    orbitType=tatc.OrbitType.SUN_SYNCHRONOUS,
                    altitude=705
                )
            )
        ],
        satellites=[
            tatc.Satellite(
                name="Landsat 8",
                mass=2750,
                volume=43.2,
                power=1550,
                commBand=[tatc.CommunicationBand.X],
                payload=tatc.Instrument(
                    name="Operational Land Imager/Thermal Infrared Sensor",
                    acronym="OLI/TIRS",
                    agency=tatc.Agency(tatc.AgencyType.GOVERNMENT),
                    mass=657,
                    volume=10.016,
                    power=319,
                    fieldOfView=15
                )
            )
        ],
        launchers=[
            tatc.LaunchVehicle(
                name="AtlasV",
                dryMass=2316,
                propellantMass=20830,
                specificImpulse=450.5,
                massToLEO=9800,
                reliability=1,
                cost=130,
                meanTimeBetweenLaunches="P0Y0M133D"
            ),
            tatc.LaunchVehicle(
                name="Vega",
                dryMass=147,
                propellantMass=550,
                specificImpulse=315.5,
                massToLEO=1450,
                reliability=1,
                cost=37,
                meanTimeBetweenLaunches="P0Y0M221D"
            )
        ],
        groundNetworks=[
            tatc.GroundNetwork(numberStations=1)
        ],
        groundStations=[
            tatc.GroundStation(
                latitude=40.5974791834978,
                longitude=-104.83875274658203,
                elevation=1570,
                commBand=[tatc.CommunicationBand.X]
            )
        ]
    )
    settings = tatc.AnalysisSettings(includePropulsion=False)
    search = tatc.TradespaceSearch(
        mission=mission,
        designSpace=designSpace,
        settings=settings
    )
    return search

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Writes an example tradespace search file')
    parser.add_argument(
        'outfile',
        nargs = '?',
        type = argparse.FileType('w'),
        default = 'landsat8.json',
        help = "Tradespace search output file"
    )
    args = parser.parse_args()
    build_example_tradespace_search().to_json(args.outfile, indent=2)
