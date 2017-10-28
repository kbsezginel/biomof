"""
Generates RASPA input file for given cif file and simulation parameters to calculate adsorption.
"""
# RASPA 2 input file generation for adsorption simulations
# Author: Kutay B. Sezginel
# Date: July 2017


def write_raspa_file(input_file, framework_name, adsorbate='N2', uc=[1, 1, 1], T=298.0, P=100, vf=None,
                     forcefield='UFF', charge=False, movies=None, init_cycles=5000, sim_cycles=10000,
                     cutoff=12.0, definition='Drugs', print_every=1000):
    """
    Writes RASPA input file for simulating gas adsorption.
    Arguments:
        - input_file (str)     : path to input file.
        - framework_name (str) : name of the cif file

    Optional arguments:
        - adsorbate (str)      : adsorbate molecule name
        - uc (list)            : unit cell packing
        - T (float)            : external temperature (K)
        - P (float)            : external pressure (bar)
        - vf (float / None)    : void fraction of the framework
        - forcefield (str)     : forcefield file to use
        - charge (bool)        : use charges in simulation
        - movies (int / None)  : write movies every 'movies' frame
        - init_cycles (int)    : number of initialization cycles
        - sim_cycles (int)     : number of simulation cycles
        - cutoff (float)       : cut-off radius (Angstroem)
        - definition (str)     : molecule definition
        - print_every (int)    : print every 'print_every' frames
    """
    external_pressure = float(P) * 100000  # bar -> torr

    with open(input_file, "w") as raspa_input_file:
        raspa_input_file.write(
            "SimulationType                 MonteCarlo\n" +
            "NumberOfCycles                 %s\n" % (sim_cycles) +
            "NumberOfInitializationCycles   %s\n" % (init_cycles) +
            "PrintEvery                     %i\n" % (print_every) +
            "RestartFile                    no\n" +
            "\n" +
            "Forcefield                     %s\n" % (forcefield) +
            "CutOff                         %.2f\n" % (cutoff) +
            "\n" +
            "Framework                      0\n" +
            "FrameworkName                  %s\n" % (framework_name) +
            "UnitCells                      %i %i %i\n" % (uc[0], uc[1], uc[2]) +
            "ExternalTemperature            %.1f\n" % T +
            "ExternalPressure               %.1f\n" % external_pressure +
            "\n"
        )
        if charge is True:
            raspa_input_file.write(
                "Charge Method                  Ewald\n" +
                "Ewald Precision                1e-6\n" +
                "UseChargesFromCIFFile          yes\n"
            )

        if vf is not None:
            raspa_input_file.write("HeliumVoidFraction             %s\n" % str(vf))
        if movies is not None:
            raspa_input_file.write(
                "\n" +
                "Movies                         yes\n" +
                "WriteMoviesEvery               %i\n" % movies
            )
        raspa_input_file.write(
            "\n" +
            "Component 0 MoleculeName               %s\n" % adsorbate +
            "            MoleculeDefinition         %s\n" % definition +
            "            TranslationProbability     1.0\n" +
            "            RotationProbability        1.0\n" +
            "            ReinsertionProbability     1.0\n" +
            "            SwapProbability            1.0\n" +
            "            CreateNumberOfMolecules    0\n"
        )
