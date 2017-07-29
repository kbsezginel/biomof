import os
import glob
import shutil
import argparse
from ccdc import io
from ccdc import conformer
from ccdc.descriptors import MolecularDescriptors
from raspa_molecule import write_raspa_molecule
from raspa_input import write_raspa_file
from replace_lines import replace_lines
from write_soap import write_soap


parser = argparse.ArgumentParser(
    description="""
-------------------------------------------------
Molecular conformer search using CSD Python API.

Available formats file formats:
| mol | mol2 | cif | pdb | sdf |
-------------------------------------------------
    """,
    epilog="""
Example:
python conformer_search.py my_molecule.pdb 10

would generate maximum of 10 conformers of the given molecule
and save them to /my_molecule-conformers in 'mol' format.
    """,
    formatter_class=argparse.RawDescriptionHelpFormatter)

# Positional arguments
parser.add_argument('molecule', type=str, help='Molecule file to create conformers')
parser.add_argument('conformers', type=int, help='Number of conformers')

# Optional arguments
parser.add_argument('--format', '-f', default='mol', type=str, metavar='',
                    help="File format used to save molecule files (default: mol)")
parser.add_argument('--raspa', '-r', action='store_true', default=False,
                    help="create .def files for RASPA (default: False)")
parser.add_argument('--initialize', '-i', action='store_true', default=False,
                    help="Initialize files for a RASPA simulation (default: False)")
parser.add_argument('--unitcell', '-uc', metavar='', nargs=3,  default=[1, 1, 1], type=int,
                    help="Unit cell packing for RASPA (default: 1 1 1)")
parser.add_argument('--source', '-s', metavar='', type=str, default=r'source',
                    help="Source files directory for RASPA (default: ./source)")
parser.add_argument('--soap', action='store_true', default=False,
                    help="create xyz files for SOAP (default: False)")
parser.add_argument('--nominimise', '-nm', action='store_true', default=False,
                    help="Don't run minimisation on conformers (default: False)")
parser.add_argument('--nocleanup', '-nc', action='store_true', default=False,
                    help="Don't remove conformer search logs (default: False)")

args = parser.parse_args()

# Read molecule ------------------------------------------------------------------------------------
print('%s\nReading molecule: %s\n' % ('-' * 40, args.molecule))
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
----------------------------------------
Conformers generated: %i
Conformer sampling limit reached: %s
Rotamers sampled: %i / %i
----------------------------------------
""" % (len(conformers), conformers.sampling_limit_reached,
       conformers.n_rotamers_sampled, conformers.n_rotamers_in_molecule))

# Minimise conformers and save ---------------------------------------------------------------------
conformers_dir = '%s-conformers' % mol_name
if not os.path.isdir(conformers_dir):
    os.makedirs(conformers_dir)

if args.nominimise:
    print('Skiping minimisation...')
    for conf_idx, conf in enumerate(conformers):
        conf_path = os.path.join(conformers_dir, '%s-%i.%s' % (mol_name, conf_idx + 1, args.format))
        with io.MoleculeWriter(conf_path) as molecule_writer:
            molecule_writer.write(conf.molecule)
    conformers_mol = [c.molecule for c in conformers]
else:
    # Run minimisation
    print('Minimising molecular geometry using Tripos force field...')
    molecule_minimiser = conformer.MoleculeMinimiser()                   # Uses Tripos force field
    min_conformers = []
    for conf_idx, conf in enumerate(conformers):
        score, rmsd = conf.normalised_score, conf.rmsd()                 # Conformer score and RMSD
        min_conf = molecule_minimiser.minimise(conf.molecule)            # Minimise conformer
        min_conformers.append(min_conf)                                  # Add to list
        min_rmsd = round(MolecularDescriptors.rmsd(mol, min_conf), 3)    # Minimized RMSD (!!this method gives different results compared to conf.rmsd())

        conf_path = os.path.join(conformers_dir, '%s-%i.%s' % (mol_name, conf_idx + 1, args.format))
        with io.MoleculeWriter(conf_path) as molecule_writer:
            molecule_writer.write(min_conf)
    conformers_mol = min_conformers

print('Conformers saved in %s | format: %s\n' % (conformers_dir, args.format))

# Generate RASPA molecule definition files ---------------------------------------------------------
if args.raspa:
    # Create .def files
    print('Creating molecule definition files for RASPA...')
    raspa_dir = '%s-conformers-RASPA' % mol_name
    if not os.path.isdir(raspa_dir):
        os.makedirs(raspa_dir)
    if args.initialize:
        source_dir = args.source
        source_files = [os.path.join(source_dir, f) for f in os.listdir(source_dir)]
        cif_name = [os.path.splitext(os.path.basename(f))[0] for f in source_files if '.cif' in f][0]
        print('Initializing RASPA simulation files from: %s' % args.source)
    for conf_idx, conf in enumerate(conformers_mol):
        mol = conf
        molecule = {'elements': [str(atom.atomic_symbol) for atom in mol.atoms],
                    'coordinates': [list(atom.coordinates) for atom in mol.atoms],
                    'bonds': [[bond.atoms[0].index, bond.atoms[1].index] for bond in mol.bonds]}
        conf_name = '%s-%i' % (mol_name, conf_idx + 1)

        if args.initialize:
            raspa_conf_dir = os.path.join(raspa_dir, conf_name)
            if not os.path.isdir(raspa_conf_dir):
                os.makedirs(raspa_conf_dir)
            write_raspa_molecule(molecule, save=raspa_conf_dir, name=conf_name)
            input_file = os.path.join(raspa_conf_dir, 'simulation.input')
            write_raspa_file(input_file, cif_name, adsorbate=conf_name, uc=args.unitcell)
            for f in source_files:
                shutil.copy(f, raspa_conf_dir)
            job_name = ['#PBS -N %s-%s\n' % (cif_name, conf_name)]
            qsub_file = glob.glob(os.path.join(raspa_conf_dir, '*qsub*'))[0]  # Find qsub file
            replace_lines(qsub_file, [3], job_name)                       # Replace job name lines
        else:
            write_raspa_molecule(molecule, save=raspa_dir, name=conf_name)

    print('Done!\n')

if args.soap:
    write_soap(conformers_mol, mol_name, soap='soap.xyz', sort_key='header')

# Cleanup log and warn files -----------------------------------------------------------------------
if args.nocleanup:
    print('Skipping cleanup...\n')
else:
    print('Removing warn and log files...\n')
    cleanup_files = ['conformer_generator.log', 'conformer_generator.warn']
    for f in cleanup_files:
        if os.path.exists(f):
            os.remove(f)

print('Finished!\n' + '-' * 40)
