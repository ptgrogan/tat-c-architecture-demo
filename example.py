from tatc import *

def main():
    mission = MissionConcept(
        name="Sustainable Land Imaging - Landsat 8",
        acronym="SLI-Landsat8",
        agency=Agency(AgencyType.GOVERNMENT),
        start="2017-08-01T00:00:00Z",
        duration="P0Y0M90D",
        target=Region(
            latitude=QuantitativeValue(35, 45),
            longitude=QuantitativeValue(-115,-100)
        ),
        objects=["SUN"]
    )
    designSpace = DesignSpace(
        constellations=[
            Constellation(
                constellationType="DELTA_HOMOGENOUS",
                numberSatellites=[1,2],
                numberPlanes=[1,2],
                orbit=Orbit(orbitType=OrbitType.SUN_SYNCHRONOUS, altitude=705),
            )
        ],
        satellites=[
            Satellite(
                name="Landsat 8",
                mass=2750,
                volume=43.2,
                power=1550,
                commBand=[CommunicationBand.X],
                payload=Instrument(
                    name="Operational Land Imager/Thermal Infrared Sensor",
                    acronym="OLI/TIRS",
                    agency=Agency(AgencyType.GOVERNMENT),
                    mass=657,
                    volume=10.016,
                    power=319,
                    operatingWavelength=[443,482,561,655,865,1609,2201,590,1373,10900,12000],
                    pixelBitDepth=12,
                    fieldOfView=7.5,
                    numberPixels=6250,
                    solarConditions="SUNLIT"
                )
            )
        ],
        launchers=[
            LaunchVehicle(
                name="AtlasV",
                dryMass=2316,
                propellantMass=20830,
                specificImpulse=450.5,
                massToLEO=9800,
                reliability=1,
                cost=130,
                meanTimeBetweenLaunches="P0Y0M133D"
            ),
            LaunchVehicle(
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
            GroundNetwork(numberStations=1)
        ],
        groundStations=[
            GroundStation(
                latitude=40.5974791834978,
                longitude=-104.83875274658203,
                elevation=1570,
                commBand=[CommunicationBand.X]
            )
        ]
    )
    settings = AnalysisSettings(propagationFidelity=0, includePropulsion=False)
    search = TradespaceSearch(mission=mission, designSpace=designSpace, settings=settings)
    with open('landsat8.json', 'w') as outfile:
        search.to_json(outfile, indent=2)
    for i, architecture in enumerate(designSpace.generate_architectures()):
        with open('landsat8-{:05d}.json'.format(i), 'w') as outfile:
            architecture.to_json(outfile, indent=2)

if __name__ == "__main__":
    main()
