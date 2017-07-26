import os
import sys
import argparse
from ccdc import io
from ccdc import conformer
from ccdc.descriptors import MolecularDescriptors
from raspa_molecule import write_raspa_molecule
from raspa_input import write_raspa_file


parser = argparse.ArgumentParser(
    description="""
-------------------------------------------------
Molecular conformer search using CSD Python API.

Available formats file formats:
| cif | pdb | mol | mol2 | sdf |
-------------------------------------------------
    """,
    epilog="""
Example:
python conformer_search.py my_molecule.pdb 10

would generate maximum of 10 conformers of the given molecule
and save them to /my_molecule-conformers in pdb format.
    """,
    formatter_class=argparse.RawDescriptionHelpFormatter)

# Positional arguments
parser.add_argument('molecule', type=str, help='Molecule file to create conformers')
parser.add_argument('conformers', type=int, help='Number of conformers')

# Optional arguments
parser.add_argument('--format', '-f', default='pdb', type=str, metavar='',
                    help='File format used to save molecule files (default: pdb)')
parser.add_argument('--minimise', '-m', action='store_true', default=True,
                    help='Run basic optimization on conformers (default: True)')
parser.add_argument('--raspa', '-r', action='store_true', default=False,
                    help='create .def files for RASPA (default: False)')
parser.add_argument('--initialize', '-i', action='store_true', default=False,
                    help='Initialize files for a RASPA simulation (default: False)')

args = parser.parse_args()

# Read molecule ------------------------------------------------------------------------------------
print('Reading molecule: %s' % args.molecule)
mol_path = args.molecule
mol_name = os.path.splitext(os.path.basename(mol_path))[0]
mol_reader = io.MoleculeReader(mol_path)
mol = mol_reader[0]
mol_reader.close()

# Generate conformers ------------------------------------------------------------------------------
print('Generating %i conformers...' % args.conformers)
conformer_generator = conformer.ConformerGenerator()            # Initialize conformer generator
conformer_generator.settings.max_conformers = args.conformers   # Set max number of conformers
conformers = conformer_generator.generate(mol)                  # Run conformer generator

print("""
---------------------------------------
Conformers generated: %i
Conformer sampling limit reached: %s
Rotamers sampled: %i / %i
---------------------------------------
""" % (len(conformers), conformers.sampling_limit_reached,
       conformers.n_rotamers_sampled, conformers.n_rotamers_in_molecule))

# Minimise conformers and save ---------------------------------------------------------------------
conformers_dir = '%s-conformers' % mol_name
if not os.path.isdir(conformers_dir):
    os.makedirs(conformers_dir)

if args.minimise:
    # Run minimisation
    print('Minimising molecular geometry using Tripos force field...')
    molecule_minimiser = conformer.MoleculeMinimiser()                   # Uses Tripos force field
    min_conformers = []
    for conf_idx, conf in enumerate(conformers):
        score, rmsd = conf.normalised_score, conf.rmsd()                 # Conformer score and RMSD
        min_conf = molecule_minimiser.minimise(conf.molecule)            # Minimise conformer
        min_conformers.append(min_conf)                                  # Add to list
        min_rmsd = round(MolecularDescriptors.rmsd(mol, min_conf), 3)    # Minimized RMSD (!!this method gives different results compared to conf.rmsd())

        conf_path = os.path.join(conformers_dir, '%s-%i.mol2' % (mol_name, conf_idx + 1))
        with io.MoleculeWriter(conf_path) as molecule_writer:
            molecule_writer.write(min_conf)
else:
    print('Skiping minimisation...')
    for conf_idx, conf in enumerate(conformers):
        conf_path = os.path.join(conformers_dir, '%s-%i.mol2' % (mol_name, conf_idx + 1))
        with io.MoleculeWriter(conf_path) as molecule_writer:
            molecule_writer.write(conf.molecule)

print('Conformers saved in %s\n' % conformers_dir)

# Generate RASPA molecule definition files ---------------------------------------------------------
if args.raspa:
    # Create .def files
    print('Creating molecule definition files for RASPA...')
    raspa_conf_dir = '%s-conformers-def' % mol_name
    if not os.path.isdir(raspa_conf_dir):
        os.makedirs(raspa_conf_dir)
    for conf_idx, conf in enumerate(conformers):
        mol = conf.molecule
        molecule = {'elements': [str(atom.atomic_symbol) for atom in mol.atoms],
                    'coordinates': [list(atom.coordinates) for atom in mol.atoms],
                    'bonds': [[bond.atoms[0].index, bond.atoms[1].index] for bond in mol.bonds]}
        # mol2_path = os.path.join(conformers_dir, conf)
        # mol2_conf = read_mol2(mol2_path)
        write_raspa_molecule(molecule, save=raspa_conf_dir, name='%s-%i' % (mol_name, conf_idx + 1))
    print('Done!\n')

# Generate RASPA simulation files ------------------------------------------------------------------
if args.initialize:
    # Initialize RASPA files
    print('Initializing RASPA simulation files...')
    raspa_sim_dir = '%s-RASPA' % mol_name
    if not os.path.isdir(raspa_sim_dir):
        os.makedirs(raspa_sim_dir)
    source_dir = 'source'
    for conf_idx, conf in enumerate(conformers):
        conf_name = '%s-%i' % (mol_name, conf_idx + 1)
        raspa_sim_conf_dir = os.path.join(raspa_sim_dir, conf_name)
        if not os.path.isdir(raspa_sim_conf_dir):
            os.makedirs(raspa_sim_conf_dir)
        mol = conf.molecule
        molecule = {'elements': [str(atom.atomic_symbol) for atom in mol.atoms],
                    'coordinates': [list(atom.coordinates) for atom in mol.atoms],
                    'bonds': [[bond.atoms[0].index, bond.atoms[1].index] for bond in mol.bonds]}

        input_file = os.path.join(raspa_sim_conf_dir, 'simulation.input')
        write_raspa_file(input_file,
                         'RUFMUA01',
                         adsorbate=conf_name,
                         uc=[4, 3, 3],
                         movies=1000)
print('Finished!')
