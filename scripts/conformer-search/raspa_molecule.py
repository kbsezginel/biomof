"""
Generates molecule definition files for RASPA.
"""
# Author: Kutay B. Sezginel
# Date: July 2017
import os


def write_raspa_molecule(molecule, name='molecule', code='drg', save=None, properties=None):
    """
    Write RASPA molecule definition file (rigid molecule):
    - Molecule: dictionary of elements, coordinates and bonds:
        - coordinates: list of atomic positions -> [[x1, y1, z1], [x2, y2, z2], ...]
        - elements: list of atom names          -> ['C', 'O', ...]
        - bonds: list of bonds                  -> [[0, 1], [0, 2], [1, 5], ...]

    Optional arguments:
    - name: name of the .def file         -> 'molecule'
    - code: force field code for RASPA    -> 'drg'
    - save: save directory                -> os.getcwd()
    - properties: molecule properties as  -> [critical_temperature, critical_pressure, accentric_factor]
    """
    if properties is None:
        t_critical = 550
        p_critical = 2600000.0
        acentric_factor = 0.38
    else:
        t_critical, p_critical, acentric_factor = properties

    if save is None:
        save = os.getcwd()

    elements, coordinates, bonds = molecule['elements'], molecule['coordinates'], molecule['bonds']
    raspa_molecule_path = os.path.join(save, '%s.def' % name)
    with open(raspa_molecule_path, 'w') as rm:
        rm.write(
            "# critical constants: Temperature [T], Pressure [Pa], and Acentric factor [-]\n" +
            "%.4f\n%.1f\n%.4f\n" % (t_critical, p_critical, acentric_factor) +
            "# Number of Atoms\n%i\n" % len(elements) +
            "# Number of Groups\n1\n# %s-group\nrigid\n" % name +
            "# Number of Atoms\n%i\n# Atomic Positions\n" % len(elements)
        )
        for i, (atom, coor) in enumerate(zip(elements, coordinates)):
            rm.write('%2i %2s_%3s % 5.4f % 5.4f % 5.4f\n' % (i, atom, code, coor[0], coor[1], coor[2]))

        rm.write(
            "# Chiral centers Bond  BondDipoles Bend  UrayBradley InvBend  Torsion Imp." +
            " Torsion Bond/Bond Stretch/Bend Bend/Bend Bend/Torsion IntraVDW IntraCoulomb\n" +
            "               0  %3i            0    0            0       0            0" % len(bonds) +
            "             0            0         0         0       0        0            0\n" +
            "# Bond stretch: atom n1-n2, type, parameters\n"
        )
        # Write bonds
        for b in bonds:
            rm.write("%2i %2i RIGID_BOND\n" % (b[0], b[1]))
        rm.write("# Number of config moves\n0\n")
